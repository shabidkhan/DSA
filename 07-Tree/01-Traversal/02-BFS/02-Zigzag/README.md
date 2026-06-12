# Zigzag (spiral) level-order traversal

## What is this

A variant of BFS where the **direction alternates** per level: level 0 is left-to-right, level 1 is right-to-left, level 2 is left-to-right again, and so on. The output is a list of lists, each inner list ordered according to that level's direction.

Two natural implementations:

1. **Reverse-on-odd-level**: standard level-order BFS, but reverse the level list before appending it whenever the level index is odd.
2. **Deque-with-direction-flag**: use a deque and alternate between appending children left-to-right (when reading from front) and right-to-left (when reading from back). Slightly more efficient because no extra reversal pass.

## Why we use

- Some applications need data visually mirrored per level (e.g. visualisations, spiral printing of trees).
- Lets the same BFS scaffold serve multiple output patterns by toggling one flag.
- Demonstrates how to maintain auxiliary "direction" state during BFS — a useful pattern.

## How to implement

**Method 1 — Reverse on odd levels:**

```
queue = [root]
result = []
level_idx = 0
while queue is non-empty:
    size = len(queue)
    level = []
    for _ in 0..size-1:
        node = queue.popleft()
        level.append(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
    if level_idx is odd:
        level.reverse()
    result.append(level)
    level_idx += 1
return result
```

**Method 2 — Deque + flag:**

```
deque = [root]
left_to_right = True
while deque:
    size = len(deque)
    level = []
    for _ in 0..size-1:
        if left_to_right:
            node = deque.popleft()
            level.append(node.val)
            if node.left:  deque.append(node.left)
            if node.right: deque.append(node.right)
        else:
            node = deque.pop()
            level.append(node.val)
            if node.right: deque.appendleft(node.right)
            if node.left:  deque.appendleft(node.left)
    result.append(level)
    left_to_right = not left_to_right
```

Python — Method 1 (cleaner, idiomatic):

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None) -> None:
        self.val, self.left, self.right = val, left, right

def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    q = deque([root])
    out: list[list[int]] = []
    left_to_right = True
    while q:
        level: list[int] = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        if not left_to_right:
            level.reverse()
        out.append(level)
        left_to_right = not left_to_right
    return out
```

JavaScript — Method 1:

```javascript
function zigzagLevelOrder(root) {
  if (!root) return [];
  const q = [root];
  const out = [];
  let l2r = true;
  while (q.length) {
    const level = [];
    for (let i = q.length; i > 0; i--) {
      const node = q.shift();
      level.push(node.val);
      if (node.left)  q.push(node.left);
      if (node.right) q.push(node.right);
    }
    if (!l2r) level.reverse();
    out.push(level);
    l2r = !l2r;
  }
  return out;
}
```

Invariant: the queue still contains exactly the current level's nodes in *left-to-right insertion order*. We only flip the **printed order** by reversing the recorded list.

## Visual

```
        3
       / \
      9  20
         / \
        15  7
```
Level 0 (L→R): `[3]`. Level 1 (R→L): `[20, 9]`. Level 2 (L→R): `[15, 7]`.

Output: `[[3], [20, 9], [15, 7]]`.

## Which problems this approach solves in the real world

- **Spiral / boustrophedon printing** of org charts and decision trees in PDFs.
- **Visualisation tools** that need a snake-like reading order for compactness.
- **Memory-friendly column layouts** where every other row reads in reverse to minimise pointer jumps.
- **Game level rendering** for serpentine path patterns.
- **Test generation** — many BFS-derived algorithm tests use zigzag to verify "direction state" handling.

## Pros and cons

**Pros**
- Simple extension of level-order with a single flag.
- O(n) time, O(width) space.
- Method 1 is straightforward to teach and debug.
- Method 2 avoids the per-level reversal cost — useful if levels are huge.

**Cons**
- Reversing a level (Method 1) adds an extra pass per level — still O(n) total but doubles constants.
- Method 2's deque manipulation needs careful child-order handling; easy to flip the wrong direction.
- The toggling state can leak bugs if combined with early termination.

## Limitations

- Only meaningful for problems where direction conveys real information.
- Not a fit for streams — you need the whole level before knowing direction.
- Doesn't generalise to arbitrary tree views; for those, use vertical-order traversal or boundary traversal.

## One example

**Problem**: Given the root of a binary tree, return the **zigzag level order traversal** of its nodes' values: level 0 left-to-right, level 1 right-to-left, alternating.
Constraints: `0 ≤ n ≤ 2000`, `-100 ≤ Node.val ≤ 100`.

**Input**:
```
    3
   / \
  9  20
     / \
    15  7
```
**Output**: `[[3], [20, 9], [15, 7]]`

## Solution explanation

```python
from collections import deque

def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    q = deque([root])
    out = []
    left_to_right = True
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        if not left_to_right:
            level.reverse()
        out.append(level)
        left_to_right = not left_to_right
    return out
```

Walk-through:

| iter | queue start  | level (raw) | direction | level (output) | queue end |
|------|--------------|-------------|-----------|-----------------|-----------|
| 1    | [3]          | [3]         | L→R       | [3]             | [9, 20]   |
| 2    | [9, 20]      | [9, 20]     | R→L       | [20, 9]         | [15, 7]   |
| 3    | [15, 7]      | [15, 7]     | L→R       | [15, 7]         | []        |

Final: `[[3], [20, 9], [15, 7]]`.

Correctness: BFS already gives nodes in left-to-right order *of the underlying tree*. Reversing the level list flips the print order without altering the queue, so the children appended for the next level are still in the correct underlying left-to-right tree order. The toggle bit gives the right direction every time.

- **Time**: O(n) — each node touched once; the reversals total O(n) across all levels (each node reversed at most once).
- **Space**: O(width) for the queue; O(n) for the output.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Binary Tree Level Order Traversal** — base BFS that this builds on. | https://leetcode.com/problems/binary-tree-level-order-traversal/ |
| Medium | **Binary Tree Zigzag Level Order Traversal** — the canonical problem above. | https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/ |
| Hard | **Binary Tree Vertical Order Traversal** — generalise BFS to (column, row) coordinates with tie-breaking. | https://leetcode.com/problems/binary-tree-vertical-order-traversal/ |
