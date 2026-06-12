# DFS Traversal

## Folder structure

```
01-DFS/
├── README.md
├── 01-Preorder/README.md
├── 02-Inorder/README.md
└── 03-Postorder/README.md
```

## What is this

Depth-first traversal walks a tree by going as deep as possible along one branch before backtracking to try another. On a binary tree the visit order is decided by *when* the current node is read relative to its left and right recursive calls: read it before descending (preorder), between left and right (inorder), or after both (postorder). The three orders use the same recursion skeleton — only the line that processes the node moves.

DFS is the natural shape of tree recursion. It uses the call stack as an implicit stack, so each path from root to leaf becomes a single sequence of frames. The choice between the three orders is not a stylistic one: each variant exposes a different invariant about when child results are available, which determines what kinds of problems they solve cleanly.

## Why we use

- Preorder is the order in which a tree is *built* or *serialized* — you write the parent first, then its subtrees.
- Inorder on a BST yields a sorted sequence, which makes BST validation and ordered traversal trivial.
- Postorder gives you both children's results before the parent, which is exactly what you need for bottom-up aggregations like height, diameter, and subtree sums.
- All three reuse the same recursion skeleton, so switching between them is a one-line move.

## How to implement

```text
function dfs(node):
    if node is null: return
    # PREORDER position: visit(node) here
    dfs(node.left)
    # INORDER position: visit(node) here
    dfs(node.right)
    # POSTORDER position: visit(node) here
```

Iterative versions use an explicit stack; postorder iterative needs either two stacks or a "visited" flag because the parent must be emitted after both children.

Subpatterns in this folder:

- `01-Preorder/` — root → left → right; serialization, copy, path enumeration.
- `02-Inorder/` — left → root → right; BST sorted output, kth smallest.
- `03-Postorder/` — left → right → root; subtree aggregates, deletion, expression evaluation.

## Which problems this approach solves in the real world

- Serializing and deserializing tree-shaped data (filesystems, scene graphs, JSON).
- Validating that a binary search tree's in-order sequence is sorted.
- Computing aggregates per directory (size, file count) where every child's value is needed before the parent's.
- Evaluating arithmetic expression trees, where operators are applied after both operand subtrees are reduced.
- Garbage-collection style "mark" passes where every descendant must be visited before reclaiming the parent.
- Rendering a UI component tree where parent layout depends on children's measured size (postorder measure, preorder layout).

## Pros and cons

**Pros**
- Uses the call stack — no extra data structure for typical depths.
- Code is short and mirrors the structural recursion of trees.
- Each order corresponds to a clear invariant about child availability.
- Easy to convert between recursive and iterative forms.

**Cons**
- Recursion depth equals tree height, which can blow the stack on skewed trees.
- Postorder iterative is awkward without a visited flag or two stacks.
- DFS visits do not yield level information without extra bookkeeping.
- Mutating the tree mid-traversal usually requires postorder to be safe.

## Limitations

- Not appropriate when you need shortest-path-in-edges semantics — that is BFS territory.
- Tail-recursion is not free in Python or JavaScript, so very deep trees risk `RecursionError`.
- Order-by-order conversions (e.g., reconstructing a tree from two orders) require both orders to be unambiguous.
- Pure DFS gives no concept of "level," "distance," or "frontier," which limits its use in BFS-shaped problems.
