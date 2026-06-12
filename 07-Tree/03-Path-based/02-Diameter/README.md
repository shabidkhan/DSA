# Diameter / height

## What is this

The diameter of a binary tree is the length (in edges) of the longest path between any two nodes — the path need not pass through the root. Compute it in O(n) by a post-order DFS that returns the *height* of each subtree while updating a global best with `left_height + right_height` at the current node.

Height = number of edges in the longest downward path from a node to any descendant; alternatively, the count of nodes minus one along that path.

## Why we use

- O(n) single DFS pass for both height and diameter.
- Same two-value recursion pattern as max-path-sum.
- Generalizes to N-ary trees and weighted trees.
- Foundation for centroid decomposition and tree DP.

## How to implement

```
diameter(root):
    best = 0
    def height(node):
        nonlocal best
        if node is None: return 0
        l = height(node.left)
        r = height(node.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    height(root)
    return best
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def diameter_of_binary_tree(root):
    best = 0
    def h(node):
        nonlocal best
        if node is None: return 0
        l = h(node.left)
        r = h(node.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    h(root)
    return best
```

```python
def tree_height(root):
    if root is None: return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))
```

The recursion *returns* height (used by the parent) but *updates a global* the diameter — single pass.

## Which problems this approach solves in the real world

- Computing the worst-case message hop count in a tree-shaped network.
- Finding the longest pipeline / pipeline-stage path in a tree-structured DAG.
- Computing tree depth for indentation-based renderers.
- Maximum decision-chain length in decision trees.
- Centroid / centroid decomposition setup for tree DP.

## Pros and cons

**Pros**
- O(n) single DFS — no extra precomputation.
- Same template for diameter, height, max-path-sum variations.
- Easy to extend to weighted edges.

**Cons**
- O(h) recursion depth — stack overflow on degenerate trees.
- Definition (edges vs nodes) varies between problems; off-by-one is common.
- N-ary version needs to find the two largest child heights, not just `l` and `r`.

## Limitations

- Cyclic structures invalidate the recursion.
- Streaming trees (online build) require recomputation per insertion.
- Diameter does not commute with subtree merges trivially.

## One example

**Problem**: Given the root of a binary tree, return the length of the diameter — the longest path (in number of edges) between any two nodes.

**Input**: `root = [1, 2, 3, 4, 5]`
**Output**: `3`  (path 4 - 2 - 1 - 3 or 5 - 2 - 1 - 3)
**Constraints**: `1 <= nodes <= 10^4`, `-100 <= node.val <= 100`.

## Solution explanation

```python
def diameterOfBinaryTree(root):
    best = 0
    def h(node):
        nonlocal best
        if node is None: return 0
        l = h(node.left)
        r = h(node.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    h(root)
    return best
```

Walkthrough on `[1, 2, 3, 4, 5]`:

| node | l | r | l + r | best | returns 1 + max(l,r) |
|------|---|---|-------|------|----------------------|
| 4    | 0 | 0 | 0     | 0    | 1                    |
| 5    | 0 | 0 | 0     | 0    | 1                    |
| 2    | 1 | 1 | 2     | 2    | 2                    |
| 3    | 0 | 0 | 0     | 2    | 1                    |
| 1    | 2 | 1 | 3     | 3    | 3                    |

Return 3. Time: O(n). Space: O(h).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Maximum Depth of Binary Tree (LeetCode 104) | https://leetcode.com/problems/maximum-depth-of-binary-tree/ |
| Medium | Diameter of Binary Tree (LeetCode 543) | https://leetcode.com/problems/diameter-of-binary-tree/ |
| Hard | Longest Path With Different Adjacent Characters (LeetCode 2246) | https://leetcode.com/problems/longest-path-with-different-adjacent-characters/ |
