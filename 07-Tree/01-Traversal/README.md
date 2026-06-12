# Tree Traversal Patterns

## Folder structure

```
01-Traversal/
├── README.md
├── 01-DFS/
│   ├── 01-Preorder/README.md
│   ├── 02-Inorder/README.md
│   └── 03-Postorder/README.md
└── 02-BFS/
    ├── README.md
    ├── 01-Level-order/README.md
    ├── 02-Zigzag/README.md
    └── 03-Right-side-view/README.md
```

## What is this

Tree traversal is the act of visiting every node in a tree in some defined order. There are two top-level strategies: **depth-first search (DFS)**, which goes as deep as possible before backtracking and has three flavours (preorder = node, left, right; inorder = left, node, right; postorder = left, right, node), and **breadth-first search (BFS)**, which visits all nodes at depth `d` before any at depth `d+1` (the canonical level-order variant, plus zigzag and right-side-view).

Which traversal to use depends on the question: structure-only and clone problems want preorder, BST-sorted output wants inorder, aggregation from children wants postorder, level-based questions want BFS. Mastering the four traversals means almost every tree problem becomes a 5-10 line implementation.

## Why we use

- Each traversal directly fits a class of problems (sorted output, child-up aggregation, level info).
- DFS uses O(h) stack — usually much less than O(n) BFS queue memory.
- BFS gives shortest-path semantics on unweighted hierarchies.
- The four templates are short, memorable, and compose with other patterns.

## How to implement

```
DFS recursive:
    def dfs(node):
        if not node: return
        pre_visit(node)
        dfs(node.left)
        in_visit(node)
        dfs(node.right)
        post_visit(node)

DFS iterative (preorder):
    stack = [root]
    while stack:
        node = stack.pop()
        visit(node)
        if node.right: stack.append(node.right)
        if node.left:  stack.append(node.left)

BFS level-order:
    from collections import deque
    q = deque([root])
    while q:
        size = len(q)
        level = []
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
```

Subpatterns in this folder:

- **01-DFS** — preorder, inorder, postorder.
- **02-BFS** — level-order, zigzag, right-side-view.

## Which problems this approach solves in the real world

- File-system listing (DFS preorder for path generation).
- DOM rendering and event traversal (preorder).
- Expression evaluation (inorder of a parse tree gives the expression).
- Dependency build (postorder ensures children built before parents).
- Org-chart and breadth-limited views (BFS).
- Tree serialization formats (any traversal, deterministic).

## Pros and cons

**Pros**
- Each traversal matches a specific algorithmic shape — easy to choose.
- DFS recursive code is extremely short.
- BFS naturally gives shortest path on unweighted hierarchies.
- Iterative variants avoid stack overflow on deep trees.

**Cons**
- Recursive DFS blows the stack on skewed trees (Python's default is 1000 frames).
- Mixing return values with side effects creates subtle bugs.
- BFS uses O(width) queue memory — can be huge on broad trees.
- Inorder vs preorder vs postorder errors are easy to make under time pressure.

## Limitations

- DFS doesn't give shortest-path information on weighted trees.
- BFS doesn't preserve the recursive structure useful for aggregation.
- Threaded trees or persistent variants need custom traversal logic.
- Concurrent modification during traversal is undefined behaviour.
