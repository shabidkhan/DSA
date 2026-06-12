# Right-side view of a binary tree

## What is this

The right-side view of a binary tree is the list of nodes you'd see if you stood to the right of the tree and looked left — i.e. the **rightmost node at every level**. Computed naturally with a level-order BFS that, at each level, records only the **last** node dequeued (or the first, if you process the queue right-to-left). A DFS variant also exists where you visit right-children first and record the first node encountered at each depth.

## Why we use

- Solves the "skyline" / "silhouette from the right" view in **O(n) time** with a single tree pass.
- Mirror logic gives the left-side view: record the **first** node of each level.
- Used in tree-visualisation, layout, and printing problems where only edges of the tree matter.
- DFS variant is recursive and shows a nice "depth determines recording" pattern.

## How to implement

**Method 1 — BFS level-order, record last per level:**

```
queue = [root]
view = []
while queue:
    size = len(queue)
    for i in 0..size-1:
        node = queue.popleft()
        if i == size - 1:                  # last node of this level
            view.append(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
return view
```

**Method 2 — DFS, visit right first, record first node seen at each depth:**

```
view = []
def dfs(node, depth):
    if node is None: return
    if depth == len(view):                 # first node seen at this depth
        view.append(node.val)
    dfs(node.right, depth + 1)
    dfs(node.left,  depth + 1)
dfs(root, 0)
return view
```

Python — BFS version:

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None) -> None:
        self.val, self.left, self.right = val, left, right

def right_side_view(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    q = deque([root])
    out: list[int] = []
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:
                out.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
    return out
```

JavaScript — DFS version:

```javascript
function rightSideView(root) {
  const view = [];
  function dfs(node, depth) {
    if (!node) return;
    if (depth === view.length) view.push(node.val);
    dfs(node.right, depth + 1);
    dfs(node.left,  depth + 1);
  }
  dfs(root, 0);
  return view;
}
```

Invariant (BFS): after each level, exactly one value has been appended — the rightmost. Invariant (DFS): when we visit a node, if its depth equals the current `len(view)`, we've never recorded a node at that depth; because we recurse right-first, this is the rightmost node at that depth.

## Visual

```
    1
   / \
  2   3
   \   \
    5   4
```
Right-side view: `[1, 3, 4]` — at depth 0 we see `1`, at depth 1 we see `3` (which blocks `2`), at depth 2 we see `4` (which blocks `5`).

## Which problems this approach solves in the real world

- **Tree visualisation**: render only the silhouette of a deeply nested folder structure.
- **DOM / layout systems**: identify the rightmost element on each visual row.
- **Game pathing**: find the right "outline" of a dungeon BFS region for collision against a wall.
- **Org chart printing**: rightmost report per management level.
- **Decision tree summaries**: extreme-branch nodes for explanation.

## Pros and cons

**Pros**
- O(n) single pass — every node visited exactly once.
- Two equally valid implementations (BFS vs DFS) — pick based on tree shape and stack depth tolerance.
- Mirror trick gives the left view for free.
- The DFS version is six lines.

**Cons**
- BFS uses O(width) memory — fine for balanced trees, possibly large for complete trees.
- DFS uses O(height) recursion stack — risky for unbalanced trees (linked-list-shaped).
- "Last in level" vs "first in level" can be confused if you swap BFS scanning direction.

## Limitations

- Returns one value per level — doesn't reveal interior nodes.
- For arbitrary "view from angle θ", BFS doesn't generalise; you'd need a coordinate-based traversal.
- The DFS version assumes "depth == len(view)" works — fine because we append exactly once per new depth.

## One example

**Problem**: Given the `root` of a binary tree, imagine yourself standing on the **right side** of it. Return the values of the nodes you can see, ordered from top to bottom.
Constraints: `0 ≤ n ≤ 100`, `-100 ≤ Node.val ≤ 100`.

**Input**:
```
    1
   / \
  2   3
   \   \
    5   4
```
**Output**: `[1, 3, 4]`

## Solution explanation

DFS, right-first:

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    view: list[int] = []
    def dfs(node: TreeNode | None, depth: int) -> None:
        if not node:
            return
        if depth == len(view):
            view.append(node.val)
        dfs(node.right, depth + 1)
        dfs(node.left,  depth + 1)
    dfs(root, 0)
    return view
```

Walk-through on the tree (depth in parens):

| call           | view before | append? | view after | recurse next         |
|----------------|-------------|---------|------------|----------------------|
| dfs(1, 0)      | []          | yes (0) | [1]        | dfs(3, 1), dfs(2, 1) |
| dfs(3, 1)      | [1]         | yes (1) | [1,3]      | dfs(4, 2), dfs(None) |
| dfs(4, 2)      | [1,3]       | yes (2) | [1,3,4]    | dfs(None), dfs(None) |
| dfs(None,3)    | —           | —       | —          | —                    |
| dfs(2, 1)      | [1,3,4]     | no (1≠3)| [1,3,4]    | dfs(5, 2), dfs(None) |
| dfs(5, 2)      | [1,3,4]     | no (2≠3)| [1,3,4]    | base cases           |

Final: `[1, 3, 4]`.

Correctness: at each depth, we record exactly one value — the first time we reach that depth in the traversal. Because we always recurse right before left, the first node encountered at each depth is the rightmost one. Subsequent visits to the same depth skip the append.

- **Time**: O(n) — every node is visited once.
- **Space**: O(h) recursion stack, where h is tree height.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Maximum Depth of Binary Tree** — basic recursion warm-up; computes the deepest level. | https://leetcode.com/problems/maximum-depth-of-binary-tree/ |
| Medium | **Binary Tree Right Side View** — the canonical problem above. | https://leetcode.com/problems/binary-tree-right-side-view/ |
| Hard | **Binary Tree Vertical Order Traversal** — generalises BFS to column/row coordinates with stable ordering. | https://leetcode.com/problems/binary-tree-vertical-order-traversal/ |
