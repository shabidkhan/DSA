# Path sum

## What is this

Path-sum problems ask whether a tree contains a root-to-leaf path with a given total, or count / enumerate such paths, or find the *maximum* path sum that can bend through any node (not just root-to-leaf). The unifying technique is post-order DFS: each node receives the best "downward" sum from each child, decides whether to extend it upward, and updates a global answer that considers paths bending through itself.

The "bending through any node" variant uses two values per recursion: what to *return* upward (single arm) versus what to *update globally* (two arms combined through this node).

## Why we use

- Single O(n) DFS pass handles all path-sum variants.
- Separates "return upward" from "global candidate" — clean two-value recursion.
- Generalizes to weighted edges, target sums, and longest paths.
- Foundation for Diameter, Max-path-sum, and Path-sum-III problems.

## How to implement

```
has_path_sum(node, t):
    if node is None: return False
    if node.left is None and node.right is None: return node.val == t
    return has_path_sum(node.left, t - node.val) or has_path_sum(node.right, t - node.val)

max_path_sum(root):
    best = -inf
    def go(node):
        nonlocal best
        if node is None: return 0
        left  = max(0, go(node.left))    # ignore negative arms
        right = max(0, go(node.right))
        best = max(best, node.val + left + right)
        return node.val + max(left, right)
    go(root)
    return best
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def has_path_sum(root, target):
    if root is None: return False
    if root.left is None and root.right is None:
        return target == root.val
    return (has_path_sum(root.left,  target - root.val)
         or has_path_sum(root.right, target - root.val))
```

```python
def maxPathSum(root):
    best = float('-inf')
    def go(node):
        nonlocal best
        if node is None: return 0
        l = max(0, go(node.left))
        r = max(0, go(node.right))
        best = max(best, node.val + l + r)
        return node.val + max(l, r)
    go(root)
    return best
```

Clamping each arm to `max(0, ...)` lets the recursion choose to *skip* a negative arm.

## Which problems this approach solves in the real world

- Optimal flow from any leaf-source to any leaf-sink in a tree network.
- Routing the highest-yield trace through a tree-shaped dependency graph.
- Pruning decision trees by best-path sum criteria.
- Computing tree diameters in road / pipeline networks.
- Aggregating cost / weight along optimal paths.

## Pros and cons

**Pros**
- O(n) single DFS pass.
- Two-value recursion cleanly separates global vs upward contributions.
- Easily generalized to count, exists, list-of-paths.

**Cons**
- Recursion depth O(h) — stack overflow on degenerate trees.
- "Bend through node" twist trips up beginners.
- Hard to parallelize (tree shape matters).

## Limitations

- Cyclic graphs need a different approach (DFS with visited set + cycle handling).
- Streaming variants are awkward — the entire tree must be available.
- Multi-target sums need DP over (node, sum mod m) states.

## One example

**Problem**: Given the root of a binary tree, return the maximum path sum of any non-empty path. A path is any sequence of nodes joined by edges where each pair is adjacent; it does not need to pass through the root.

**Input**: `root = [-10, 9, 20, null, null, 15, 7]`
**Output**: `42`  (path 15 - 20 - 7)
**Constraints**: `1 <= nodes <= 3 * 10^4`, `-1000 <= node.val <= 1000`.

## Solution explanation

```python
def maxPathSum(root):
    best = float('-inf')
    def go(node):
        nonlocal best
        if node is None: return 0
        l = max(0, go(node.left))
        r = max(0, go(node.right))
        best = max(best, node.val + l + r)
        return node.val + max(l, r)
    go(root)
    return best
```

Walkthrough on `[-10, 9, 20, null, null, 15, 7]`:

| node | l | r | candidate (val + l + r) | best | returns upward |
|------|---|---|--------------------------|------|----------------|
| 9    | 0 | 0 | 9                        | 9    | 9              |
| 15   | 0 | 0 | 15                       | 15   | 15             |
| 7    | 0 | 0 | 7                        | 15   | 7              |
| 20   | 15| 7 | 42                       | 42   | 20 + 15 = 35   |
| -10  | 9 | 35| -10+9+35 = 34            | 42   | -10 + 35 = 25  |

Return 42. Time: O(n). Space: O(h).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Path Sum (LeetCode 112) | https://leetcode.com/problems/path-sum/ |
| Medium | Path Sum III (LeetCode 437) | https://leetcode.com/problems/path-sum-iii/ |
| Hard | Binary Tree Maximum Path Sum (LeetCode 124) | https://leetcode.com/problems/binary-tree-maximum-path-sum/ |
