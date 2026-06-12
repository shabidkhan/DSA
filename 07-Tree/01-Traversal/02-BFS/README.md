# BFS on tree (level-order)

## Folder structure

```
02-BFS/
├── README.md
├── 01-Level-order/README.md
├── 02-Zigzag/README.md
└── 03-Right-side-view/README.md
```

## What is this

BFS on a tree is a level-by-level traversal that visits all nodes at depth `d` before any node at depth `d+1`. It uses a FIFO queue: pop the front node, push its children to the back, and repeat until the queue is empty.

Level-order is the natural way to answer "per-level" questions: averages per level, rightmost node per level, zigzag traversal, minimum depth, and so on.

## Why we use

- Produces nodes in depth order, which DFS does not.
- Finds shortest path from the root to a target in an unweighted tree.
- Lets you process each level as a batch (great for serialization, printing, level statistics).
- Avoids recursion-depth limits on very deep trees.

## How to implement

```text
function levelOrder(root):
    if not root: return []
    queue = [root]
    levels = []
    while queue:
        level = []
        next_queue = []
        for node in queue:
            level.append(node.val)
            if node.left: next_queue.append(node.left)
            if node.right: next_queue.append(node.right)
        levels.append(level)
        queue = next_queue
    return levels
```

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root: TreeNode) -> list[list[int]]:
    if not root:
        return []
    q = deque([root])
    levels = []
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(level)
    return levels
```

The invariant: at the start of each outer loop iteration, the queue contains exactly the nodes at the current level. Capturing `len(q)` before the inner loop locks the level boundary so children pushed during this iteration belong to the next level.

## Which problems this approach solves in the real world

- Rendering tree-structured UI (e.g., file explorer) level by level for progressive loading.
- Serializing/deserializing trees for network transfer (LeetCode 297 style).
- Computing organizational reporting hierarchies grouped by management level.
- Game-tree expansion to a fixed depth (iterative deepening's BFS layer).
- Network discovery: finding all devices reachable within `k` hops from a router.

## Pros and cons

**Pros**
- Iterative — no recursion depth concerns.
- Naturally groups output by level.
- Easy to add early termination once a target depth is reached.

**Cons**
- Uses `O(W)` memory where `W` is the maximum level width (can be `O(n/2)` for full trees).
- Cannot easily produce post/pre-order output without DFS.
- Queue operations have a small constant overhead vs recursive DFS.

## Limitations

- Not suitable when you need to process descendants before ancestors (use post-order DFS).
- For weighted trees / shortest-cost questions, BFS does not give the right answer.
- On extremely wide trees the queue can become large; consider streaming if memory is tight.
- The queue must support `O(1)` pop-front (use `collections.deque`, not `list`).

## One example

Problem: Given the root of a binary tree, return its level-order traversal as a list of lists, one list per level.

```
Input tree:
        3
       / \
      9  20
         / \
        15  7

Output: [[3], [9, 20], [15, 7]]
```

Constraints: number of nodes in the range `[0, 2000]`; `-1000 <= Node.val <= 1000`.

## Solution explanation

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    q = deque([root])
    res = []
    while q:
        size = len(q)
        level = []
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res
```

Walkthrough for the sample tree:

| Iter | size | Queue before | Level collected | Queue after |
|------|------|--------------|-----------------|-------------|
| 1 | 1 | [3] | [3] | [9, 20] |
| 2 | 2 | [9, 20] | [9, 20] | [15, 7] |
| 3 | 2 | [15, 7] | [15, 7] | [] |

Return `[[3], [9, 20], [15, 7]]`.

Time: `O(n)`, each node enqueued and dequeued once. Space: `O(W)` where `W` is the max level width.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Average of Levels in Binary Tree (LeetCode 637) | https://leetcode.com/problems/average-of-levels-in-binary-tree/ |
| Medium | Binary Tree Level Order Traversal (LeetCode 102) | https://leetcode.com/problems/binary-tree-level-order-traversal/ |
| Hard | Serialize and Deserialize Binary Tree (LeetCode 297) | https://leetcode.com/problems/serialize-and-deserialize-binary-tree/ |
