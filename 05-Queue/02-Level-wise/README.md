# Level-wise queue processing

## What is this

Level-wise processing uses a FIFO queue but treats each "layer" as a unit — you record the queue size at the start of a level, then dequeue exactly that many items before moving on. This produces clean level boundaries for trees, grids, and graphs.

It is BFS with explicit awareness of depth, which lets you compute level sums, level orders, zigzag traversals, minimum-steps-to-target, and "rotten oranges" style spread.

## Why we use

- Separate output by depth without storing depth on each node.
- Compute statistics per level (sum, max, avg, count).
- Discover shortest-path distance in unweighted graphs (level index = distance).
- Express multi-source spread cleanly.

## How to implement

```
q = deque([root])
levels = []
while q:
    size = len(q)
    layer = []
    for _ in range(size):
        node = q.popleft()
        layer.append(node.val)
        for nb in neighbors(node):
            q.append(nb)
    levels.append(layer)
```

```python
from collections import deque

def level_order(root):
    if not root: return []
    out, q = [], deque([root])
    while q:
        layer = []
        for _ in range(len(q)):
            n = q.popleft()
            layer.append(n.val)
            if n.left:  q.append(n.left)
            if n.right: q.append(n.right)
        out.append(layer)
    return out
```

```python
def shortest_path_unweighted(adj, src, dst):
    q = deque([src])
    dist = {src: 0}
    while q:
        u = q.popleft()
        if u == dst: return dist[u]
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return -1
```

Capturing `len(q)` *before* the loop is the entire trick — newly enqueued items belong to the next level.

## Which problems this approach solves in the real world

- Computing minimum number of steps in a maze / grid.
- Spreading processes: rotting oranges, fire spread, infection waves.
- Organizational-chart traversal level by level.
- Web-crawler depth caps with depth-aware bookkeeping.
- Network broadcast: number of hops to reach all nodes.

## Pros and cons

**Pros**
- Clean per-level boundaries without storing depth.
- Optimal for unweighted shortest path.
- Trivially extended to multi-source by enqueueing all sources first.

**Cons**
- Memory holds the full frontier (entire widest level).
- Not optimal when edge weights vary (use Dijkstra).
- Reconstructing the path requires a parent map.

## Limitations

- Not suited for weighted shortest path.
- Storing the level snapshot forces O(width) extra space per pass.
- Cycle handling requires a separate "visited" set.

## One example

**Problem**: Given the root of a binary tree, return its level-order traversal as a list of lists.

**Input**: `root = [3, 9, 20, null, null, 15, 7]`
**Output**: `[[3], [9, 20], [15, 7]]`
**Constraints**: `0 <= nodes <= 2000`, `-1000 <= node.val <= 1000`.

## Solution explanation

```python
from collections import deque

def levelOrder(root):
    if not root: return []
    out, q = [], deque([root])
    while q:
        layer = []
        for _ in range(len(q)):
            n = q.popleft()
            layer.append(n.val)
            if n.left:  q.append(n.left)
            if n.right: q.append(n.right)
        out.append(layer)
    return out
```

Walkthrough on the input above:

| iter | q before | size | layer collected | q after |
|------|----------|------|-----------------|---------|
| 1    | [3]      | 1    | [3]             | [9, 20] |
| 2    | [9, 20]  | 2    | [9, 20]         | [15, 7] |
| 3    | [15, 7]  | 2    | [15, 7]         | []      |

Time: O(n). Space: O(width).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Average of Levels in Binary Tree (LeetCode 637) | https://leetcode.com/problems/average-of-levels-in-binary-tree/ |
| Medium | Binary Tree Level Order Traversal (LeetCode 102) | https://leetcode.com/problems/binary-tree-level-order-traversal/ |
| Hard | Word Ladder (LeetCode 127) | https://leetcode.com/problems/word-ladder/ |
