# Level-order traversal (BFS)

## What is this

Breadth-first traversal of a binary tree, visiting nodes **level by level** from the root downward. A FIFO queue holds the nodes for the current level (and is extended with their children for the next level). The output is typically a list of lists — one inner list per level — or a single flattened list.

The defining trick: at the start of each outer loop iteration, the queue's *current length* equals the number of nodes at the current level. Iterate exactly that many times to drain one level cleanly before touching the next.

## Why we use

- Yields nodes in order of increasing depth — the natural fit for problems like "shortest path from root", "minimum depth", "bottom-up view".
- Each node is visited exactly once → **O(n) time, O(width) space** where width is the maximum nodes at any single level.
- Avoids the recursion stack — useful for very deep or unbalanced trees where DFS could stack-overflow.
- The same loop adapts to many tree-view problems: right-side view, bottom-up output, zigzag, average-per-level.

## How to implement

```
queue = [root]              # FIFO
result = []
while queue is non-empty:
    size = len(queue)
    level = []
    for _ in 0..size-1:
        node = queue.popleft()
        level.append(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
    result.append(level)
return result
```

Python:

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right

def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    q = deque([root])
    out: list[list[int]] = []
    while q:
        size = len(q)
        level: list[int] = []
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
    return out
```

JavaScript:

```javascript
function levelOrder(root) {
  if (!root) return [];
  const q = [root];
  const out = [];
  while (q.length) {
    const size = q.length;
    const level = [];
    for (let i = 0; i < size; i++) {
      const node = q.shift();
      level.push(node.val);
      if (node.left)  q.push(node.left);
      if (node.right) q.push(node.right);
    }
    out.push(level);
  }
  return out;
}
```

Invariant: at the top of each outer iteration, the queue contains exactly the nodes of one level — and only those.

## Visual

```
        3
       / \
      9  20
         / \
        15  7
```
Levels: `[[3], [9, 20], [15, 7]]`.

## Which problems this approach solves in the real world

- **Network topology / hop count**: find machines reachable within K hops from a root server.
- **Game maps**: BFS layers correspond to "tiles N steps from spawn".
- **Filesystems / org charts**: list children depth-by-depth for paginated rendering.
- **UI rendering**: depth-banded layouts (e.g. mobile family-tree views).
- **Web crawling**: visit links breadth-first to maintain shallow site coverage before deep dives.
- **Decision tree printing**: pretty-print a tree level by level for debugging.

## Pros and cons

**Pros**
- Iterative — no stack overflow on deep trees.
- O(n) time, O(width) space.
- Easy to adapt to side-views, zigzag, averages, level-K problems.
- Reads naturally: "for each level, do something".

**Cons**
- Worst-case space O(n) for a complete tree's bottom level (n/2 nodes).
- Slightly more code than recursive DFS.
- Doesn't preserve subtree locality — siblings are next to each other rather than full subtrees.

## Limitations

- For path-based queries (sum along a root-to-leaf path), DFS is more natural.
- For *very* wide trees (millions of nodes per level), queue memory can blow up.
- Sequential by level — not trivially parallelisable across the whole tree, though each level can be processed in parallel.

## One example

**Problem**: Given the root of a binary tree, return the **level-order traversal** of its nodes' values — i.e. from left to right, level by level.
Constraints: `0 ≤ n ≤ 2000`, `-1000 ≤ Node.val ≤ 1000`.

**Input**:
```
    3
   / \
  9  20
     / \
    15  7
```
**Output**: `[[3], [9, 20], [15, 7]]`

## Solution explanation

```python
from collections import deque

def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    q = deque([root])
    out: list[list[int]] = []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
    return out
```

Walk-through on the tree above:

| iteration | queue start  | level output | queue end          |
|-----------|--------------|--------------|--------------------|
| 1         | [3]          | [3]          | [9, 20]            |
| 2         | [9, 20]      | [9, 20]      | [15, 7]            |
| 3         | [15, 7]      | [15, 7]      | []                 |

Final: `[[3], [9, 20], [15, 7]]`.

Correctness: by induction on level. At iteration 1, the queue holds level 0 (root). Children appended are exactly level 1. The `for _ in range(size)` consumes one full level before the next iteration, so the invariant "queue holds the current level" is preserved.

- **Time**: O(n) — each node enqueued once and dequeued once.
- **Space**: O(width) for the queue; worst case O(n) for the bottom of a complete tree.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Average of Levels in Binary Tree** — same loop; compute average per level. | https://leetcode.com/problems/average-of-levels-in-binary-tree/ |
| Medium | **Binary Tree Level Order Traversal** — the canonical problem above. | https://leetcode.com/problems/binary-tree-level-order-traversal/ |
| Hard | **Vertical Order Traversal of a Binary Tree** — BFS while tracking (column, row) for tie-breaking. | https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/ |
