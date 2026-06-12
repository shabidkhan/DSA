# DP on trees

## What is this

DP on trees evaluates a recurrence over a rooted tree by post-order traversal: compute children's DP values first, then combine them at the current node. The state typically encodes "best answer for the subtree rooted at v under some constraint" (e.g. include v / exclude v).

Classic examples: House Robber III (no two adjacent nodes), Tree Diameter, Sum of distances in a tree, and longest path with a given property.

## Why we use

- O(V) — single post-order traversal.
- Encodes "rooted-subtree" semantics naturally.
- State per node is usually O(1) or O(k); total O(V * k).
- Foundation for re-rooting DP (compute answers for every root in O(V) total).

## How to implement

```
def dp(v, parent):
    state = base_state(v)
    for c in children(v) where c != parent:
        child_state = dp(c, v)
        state = combine(state, child_state, v)
    return state
result = dp(root, -1)
```

```python
import sys
sys.setrecursionlimit(10**5)

def rob_tree(root):
    """House Robber III: max sum, no two adjacent."""
    def go(node):
        if not node: return (0, 0)
        l_rob, l_skip = go(node.left)
        r_rob, r_skip = go(node.right)
        rob_here  = node.val + l_skip + r_skip
        skip_here = max(l_rob, l_skip) + max(r_rob, r_skip)
        return (rob_here, skip_here)
    return max(go(root))
```

```python
def sum_of_distances_in_tree(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    count = [1] * n
    answer = [0] * n
    def post(u, p):
        for v in adj[u]:
            if v == p: continue
            post(v, u)
            count[u] += count[v]
            answer[u] += answer[v] + count[v]
    def pre(u, p):
        for v in adj[u]:
            if v == p: continue
            answer[v] = answer[u] - count[v] + (n - count[v])
            pre(v, u)
    post(0, -1)
    pre(0, -1)
    return answer
```

The two-pass "re-rooting" DP: first post-order to compute "rooted at 0", then pre-order to derive "rooted at v" from the parent's answer in O(1) each.

## Which problems this approach solves in the real world

- Telecommunications subtree cost analysis on hierarchical networks.
- Org-chart aggregate computation: sum of distances from each employee.
- Compute best subtree under constraint (e.g. include or exclude this node).
- Game theory on trees: minimax with subtree values.
- Statistical aggregation in phylogenetic trees.

## Pros and cons

**Pros**
- O(V) or O(V * k) — linear in tree size.
- Two-pass re-rooting answers "for every root" in O(V) total.
- Clean separation of subtree state and combination logic.

**Cons**
- Recursion depth O(V) on degenerate trees — stack overflow risk.
- Re-rooting derivation is problem-specific and error-prone.
- Doesn't apply to general DAGs (need topological DP).

## Limitations

- Cycles invalidate the recursion — only trees / forests.
- Heavy state per node bloats memory.
- Streaming / dynamic trees need link-cut trees or Euler tour DP.

## One example

**Problem**: The "House Robber III" problem: given the root of a binary tree where each node has a non-negative value (money), maximize the total money robbed under the constraint that no two adjacent nodes (parent-child) are robbed.

**Input**: `root = [3, 2, 3, null, 3, null, 1]`
**Output**: `7`
**Constraints**: `1 <= nodes <= 10^4`, `0 <= node.val <= 10^4`.

## Solution explanation

```python
def rob(root):
    def go(node):
        if not node: return (0, 0)
        l_rob, l_skip = go(node.left)
        r_rob, r_skip = go(node.right)
        rob_here  = node.val + l_skip + r_skip
        skip_here = max(l_rob, l_skip) + max(r_rob, r_skip)
        return (rob_here, skip_here)
    return max(go(root))
```

Walkthrough on `[3, 2, 3, null, 3, null, 1]`:

```
        3
       / \
      2   3
       \   \
        3   1
```

| node | rob_here | skip_here | returns |
|------|----------|-----------|---------|
| 3 (left leaf, val=3)   | 3 | 0 | (3, 0)   |
| 2 (val=2, right=3-leaf) | 2 + 0 = 2 | max(3, 0) + 0 = 3 | (2, 3) |
| 1 (right leaf, val=1)  | 1 | 0 | (1, 0)   |
| 3 (val=3, right=1-leaf) | 3 + 0 = 3 | max(1, 0) + 0 = 1 | (3, 1) |
| 3 (root, val=3, left=(2,3), right=(3,1)) | 3 + 3 + 1 = 7 | max(2,3) + max(3,1) = 3 + 3 = 6 | (7, 6) |

Return max(7, 6) = 7. Time: O(n). Space: O(h).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Maximum Depth of Binary Tree (LeetCode 104) | https://leetcode.com/problems/maximum-depth-of-binary-tree/ |
| Medium | House Robber III (LeetCode 337) | https://leetcode.com/problems/house-robber-iii/ |
| Hard | Sum of Distances in Tree (LeetCode 834) | https://leetcode.com/problems/sum-of-distances-in-tree/ |
