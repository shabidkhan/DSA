# Inorder traversal

## What is this

Inorder traversal is a depth-first tree traversal that visits nodes in the sequence **left subtree → node → right subtree**. For a binary search tree (BST), inorder traversal yields the keys in ascending sorted order, which makes it the default tool for any "in-sorted-order" question on BSTs.

The recursive version is three lines; the iterative version uses an explicit stack and is the canonical "DFS without recursion" interview pattern.

## Why we use

- Yields the keys of a BST in ascending order — free sorted iteration.
- Lets you find the `k`-th smallest BST element by stopping early.
- Useful for validating that a tree is a BST (the inorder sequence must be strictly increasing).
- Iterative form avoids stack-overflow on deeply skewed trees.

## How to implement

```text
function inorder(node, out):
    if not node: return
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)

function inorderIter(root):
    stack = []
    out = []
    cur = root
    while cur or stack:
        while cur:
            stack.push(cur)
            cur = cur.left
        cur = stack.pop()
        out.append(cur.val)
        cur = cur.right
    return out
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_recursive(root: TreeNode) -> list[int]:
    out: list[int] = []
    def dfs(node: TreeNode | None) -> None:
        if not node:
            return
        dfs(node.left)
        out.append(node.val)
        dfs(node.right)
    dfs(root)
    return out
```

```python
def inorder_iterative(root: TreeNode) -> list[int]:
    stack, out = [], []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        out.append(cur.val)
        cur = cur.right
    return out
```

The invariant of the iterative version: the stack contains the chain of ancestors whose left subtrees we have entered but whose own values have not yet been emitted. Popping yields the next inorder value, after which we descend once into its right subtree.

## Which problems this approach solves in the real world

- Iterating a BST-backed in-memory index (e.g., `std::map`, Java `TreeMap`) in sorted order.
- Computing percentiles or the `k`-th smallest value in a BST data structure.
- Validating an imported binary tree is actually a BST before using it as one.
- Producing sorted output from a tree-based expression for canonicalization.
- Converting a BST into a sorted doubly-linked list (LeetCode 426).

## Pros and cons

**Pros**
- Yields sorted order on a BST without extra sorting.
- Iterative version uses `O(h)` memory and avoids recursion limits.
- Trivial to convert into a generator for lazy iteration.

**Cons**
- Order has meaning only for BSTs; for arbitrary trees it is just one of three DFS orders.
- Iterative form is bug-prone; the inner `while cur` loop must walk only left.
- Cannot compute aggregate values that need both children before the parent (use post-order).

## Limitations

- On extremely deep trees (`h ≈ n`), recursive form may hit Python's recursion limit (~1000) — use iterative.
- For `n`-ary trees, inorder is undefined; use pre/post-order instead.
- Cannot give "level number" alongside each node without extra bookkeeping.
- Mutating the tree during traversal corrupts the stack state.

## One example

Problem: Given the root of a binary tree, return the inorder traversal of its nodes' values.

```
Input tree:
    1
     \
      2
     /
    3

Output: [1, 3, 2]
```

Constraints: number of nodes in the range `[0, 100]`; `-100 <= Node.val <= 100`.

## Solution explanation

```python
def inorder_traversal(root):
    stack, out = [], []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        out.append(cur.val)
        cur = cur.right
    return out
```

Walkthrough for the sample tree `1 -> right 2 -> left 3`:

| Step | cur | stack | out | Action |
|------|-----|-------|-----|--------|
| 0 | 1 | [] | [] | start |
| 1 | None | [1] | [] | push 1, cur = 1.left = None |
| 2 | None | [] | [1] | pop 1, emit 1, cur = 1.right = 2 |
| 3 | None | [2, 3] | [1] | push 2, cur = 2.left = 3; push 3, cur = 3.left = None |
| 4 | None | [2] | [1, 3] | pop 3, emit 3, cur = 3.right = None |
| 5 | None | [] | [1, 3, 2] | pop 2, emit 2, cur = 2.right = None |
| 6 | None | [] | [1, 3, 2] | loop exits |

Time: `O(n)`. Space: `O(h)` for the stack, where `h` is the tree height.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Binary Tree Inorder Traversal (LeetCode 94) | https://leetcode.com/problems/binary-tree-inorder-traversal/ |
| Medium | Kth Smallest Element in a BST (LeetCode 230) | https://leetcode.com/problems/kth-smallest-element-in-a-bst/ |
| Hard | Recover Binary Search Tree (LeetCode 99) | https://leetcode.com/problems/recover-binary-search-tree/ |
