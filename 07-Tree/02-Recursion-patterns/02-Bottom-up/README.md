# Bottom-up recursion (return values UP)

## What is this

A recursion style where each call **asks its children to return a summary first**, then combines those summaries to produce its own. The return type carries the information (height, size, sum, best-so-far in subtree). The parent only acts once both children have answered.

Contrast with **top-down**, where the parent passes a prefix state down and leaves decide.

## Why we use

- Natural for problems where the answer at a node depends on the **subtree rooted at the node**: height, diameter, count, max subtree sum, balanced check.
- Each subtree's result is computed **once** — no redundant recomputation.
- Encourages a small, focused return type per node, making each function easy to reason about.
- Often becomes a one-pass O(n) solution where a naive approach is O(n²).

## How to implement

```
def dfs(node):
    if node is None:
        return base_value     # 0, +inf, empty, etc.
    left_summary  = dfs(node.left)
    right_summary = dfs(node.right)
    answer_at_node = combine(left_summary, right_summary, node)
    update_global(answer_at_node)   # if global answer exists
    return summary_for_parent(left_summary, right_summary, node)
```

Note: the **summary returned to the parent** can be different from the **answer recorded at this node**. For diameter, the function returns "height", but along the way it updates a global `max(diameter_through_node)`.

Python — Maximum Depth (purely bottom-up, no global state):

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None) -> None:
        self.val, self.left, self.right = val, left, right

def max_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

Python — Diameter of Binary Tree (returns height, updates global diameter):

```python
def diameter(root: TreeNode | None) -> int:
    best = [0]
    def height(node: TreeNode | None) -> int:
        if node is None:
            return 0
        L = height(node.left)
        R = height(node.right)
        best[0] = max(best[0], L + R)   # path through node has L + R edges
        return 1 + max(L, R)
    height(root)
    return best[0]
```

JavaScript — Balanced Binary Tree check:

```javascript
function isBalanced(root) {
  function height(node) {
    if (!node) return 0;
    const L = height(node.left);
    if (L === -1) return -1;
    const R = height(node.right);
    if (R === -1) return -1;
    if (Math.abs(L - R) > 1) return -1;   // sentinel: unbalanced
    return 1 + Math.max(L, R);
  }
  return height(root) !== -1;
}
```

Invariant: at every return, the function has produced a complete summary of the subtree rooted at `node`. The parent can rely on the summary being correct without inspecting the subtree itself.

## Visual — height (bottom-up)

```
         a(h=3)
        /  \
     b(h=2) c(h=1)
     /
   d(h=1)
```
Each node's height is computed *after* its children's heights are known: `h(a) = 1 + max(2, 1) = 3`.

## Which problems this approach solves in the real world

- **Filesystem size calculation**: each directory's size = sum of children's sizes.
- **DOM layout**: each container's height = max of children's heights + padding.
- **Tax/aggregation systems**: aggregate child accounts upward.
- **Org chart**: total headcount per manager = sum of subordinates' headcount + direct reports.
- **Compiler / AST**: type-check children first, then combine to type-check parent.
- **Dependency build systems**: build leaf modules first, then dependent modules.

## Pros and cons

**Pros**
- O(n) total time — each subtree computed exactly once.
- O(h) recursion stack for tree height h.
- The function signature is self-contained: "given a subtree, what's its summary?" — easy to unit-test recursively.
- Plays nicely with caches / memoisation for DAGs (with topological ordering).

**Cons**
- Doesn't fit problems where the answer at a node depends on the **path from root** — for that, top-down is the right tool.
- Picking the right return type is sometimes the whole puzzle (e.g. for Maximum Path Sum, return "best one-armed path ending here", not "best path through subtree").
- Errors compound: a wrong return type silently corrupts every parent's combination.

## Limitations

- Recursion stack depth equals tree height — risky for unbalanced trees.
- For very large trees, stack must be replaced with an explicit iterative post-order traversal.
- Can be hard to extend with mutable global state without losing referential clarity.

## One example

**Problem**: Given the root of a binary tree, return the **diameter** of the tree. The diameter is the length (number of edges) of the longest path between any two nodes — this path may or may not pass through the root.
Constraints: `1 ≤ n ≤ 10^4`, `-100 ≤ Node.val ≤ 100`.

**Input**:
```
      1
     / \
    2   3
   / \
  4   5
```
**Output**: `3` — the longest path is `4 → 2 → 5` (or `4 → 2 → 1 → 3`), both length 3.

## Solution explanation

```python
def diameter(root: TreeNode | None) -> int:
    best = [0]
    def height(node: TreeNode | None) -> int:
        if node is None:
            return 0
        L = height(node.left)
        R = height(node.right)
        best[0] = max(best[0], L + R)
        return 1 + max(L, R)
    height(root)
    return best[0]
```

Walk-through (post-order):

| call         | L | R | L+R (diameter candidate) | height returned | best after |
|--------------|---|---|--------------------------|------------------|------------|
| height(4)    | 0 | 0 | 0                        | 1                | 0          |
| height(5)    | 0 | 0 | 0                        | 1                | 0          |
| height(2)    | 1 | 1 | 2                        | 2                | 2          |
| height(3)    | 0 | 0 | 0                        | 1                | 2          |
| height(1)    | 2 | 1 | 3                        | 3                | **3**      |

Final answer: `best = 3`.

Correctness: for any path in the tree, there is a **unique highest node** — the path's "peak". The path-through-peak has length `left_arm + right_arm`, where the arms are the longest downward paths from each child. So if we compute, at every node, `L + R = longest_left_arm + longest_right_arm`, the global max of that value is the diameter. The function returns `1 + max(L, R)` because that's the longest arm extending from this node upward — the only thing the parent needs.

- **Time**: O(n) — one call per node.
- **Space**: O(h) recursion stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Maximum Depth of Binary Tree** — the simplest bottom-up; height = 1 + max(left, right). | https://leetcode.com/problems/maximum-depth-of-binary-tree/ |
| Medium | **Diameter of Binary Tree** — the canonical problem above. | https://leetcode.com/problems/diameter-of-binary-tree/ |
| Hard | **Binary Tree Maximum Path Sum** — return "best one-armed path ending at this node"; update a global "best path through this node". | https://leetcode.com/problems/binary-tree-maximum-path-sum/ |
