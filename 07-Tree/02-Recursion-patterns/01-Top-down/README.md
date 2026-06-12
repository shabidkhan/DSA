# Top-down recursion (pass state DOWN)

## What is this

A recursion style for trees where each call **passes accumulated state from parent to children**. The parent doesn't wait for the children to return — instead it computes "the partial answer so far at me" and passes it down so each leaf can decide whether to commit to the final result. The return type of the recursive function is usually `None` (or void); the answer accumulates in a closure variable, an outer list, or a mutable reference passed by parameter.

Contrast with **bottom-up**, where each call asks its children to compute something first and then combines the children's returned values.

## Why we use

- Natural for problems where the answer at a node depends on the **path from the root**: e.g. running maximum, depth, sum-from-root.
- Avoids re-deriving the same prefix many times — the parent computes it once and passes it down.
- Pairs cleanly with "find all root-to-leaf paths" style problems where you build up a partial path and commit on hitting a leaf.
- Often results in iterative-feeling code despite being recursive.

## How to implement

```
result = empty
def dfs(node, state_so_far):
    if node is None: return
    new_state = update(state_so_far, node)
    if node is a leaf:
        commit new_state to result
    dfs(node.left,  new_state)
    dfs(node.right, new_state)
dfs(root, initial_state)
return result
```

Python — "Maximum Depth of Binary Tree" in top-down form:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None) -> None:
        self.val, self.left, self.right = val, left, right

def max_depth_top_down(root: TreeNode | None) -> int:
    best = [0]
    def dfs(node: TreeNode | None, depth: int) -> None:
        if node is None:
            return
        depth += 1
        if not node.left and not node.right:
            best[0] = max(best[0], depth)
        dfs(node.left,  depth)
        dfs(node.right, depth)
    dfs(root, 0)
    return best[0]
```

JavaScript — "Path Sum: does any root-to-leaf path sum to targetSum?":

```javascript
function hasPathSum(root, targetSum) {
  function dfs(node, remaining) {
    if (!node) return false;
    remaining -= node.val;
    if (!node.left && !node.right) return remaining === 0;
    return dfs(node.left, remaining) || dfs(node.right, remaining);
  }
  return dfs(root, targetSum);
}
```

Invariant: at every call to `dfs(node, state)`, the `state` parameter represents the **complete information about the path from the root to (and including) node's parent**. The first thing the function does is incorporate `node` into that state.

## Visual — depth (top-down) vs height (bottom-up)

```
       a(depth=1)
      / \
   b(2) c(2)
   /
 d(3)
```
Top-down passes `depth` downward; each node sees the depth that *it* sits at without waiting for children.

```
       a(height=3)
      / \
   b(2) c(1)
   /
 d(1)
```
Bottom-up returns height upward; each node waits for children, then computes its height = `1 + max(left, right)`.

Same tree, two views of "vertical distance".

## Which problems this approach solves in the real world

- **Filesystem walk** that decides at each file whether to commit (e.g. virus scans where we test against a running checksum of the path).
- **Permission inheritance**: as we descend, accumulate effective permissions; commit a verdict at each leaf resource.
- **Compiler scope analysis**: pass an accumulating symbol table down into nested scopes.
- **Game AI minimax with α-β pruning**: pass alpha/beta down so children can prune early.
- **Decision-tree evaluation**: at each internal node, narrow the candidate set passed down.
- **HTML / DOM** style propagation: parent-applied CSS contributes to child computation.

## Pros and cons

**Pros**
- Avoids redundant recomputation of prefixes.
- Easy to support early termination — return as soon as the goal is reached.
- The recursion stack mirrors the natural "path from root" structure, simplifying debugging.
- Works for problems where the result is a **collection of root-to-leaf facts** (all paths, deepest leaf, etc.).

**Cons**
- The answer often lives in a closure or out-parameter, which can be confusing.
- If the state is mutable (e.g. a list of path nodes), you must remember to **undo your push** on backtrack.
- Doesn't naturally compose results from children — for things like diameter or subtree size, bottom-up is the better fit.

## Limitations

- Doesn't fit problems where the answer at a node depends on the **subtree** rooted at the node (height, count, diameter).
- Mixing top-down with mutable state often requires explicit undo (backtracking), which is easy to get wrong.
- For very deep trees, recursion stack depth still equals the tree height — switch to iterative + explicit stack if you're risking stack overflow.

## One example

**Problem**: Given the root of a binary tree and an integer `targetSum`, return `true` if the tree has a **root-to-leaf path** such that adding up all the values along the path equals `targetSum`.
Constraints: `0 ≤ n ≤ 5000`, `-1000 ≤ Node.val ≤ 1000`, `-1000 ≤ targetSum ≤ 1000`.

**Input**:
```
        5
       / \
      4   8
     /   / \
    11  13  4
   /  \      \
  7    2      1
```
`targetSum = 22`. The path `5 → 4 → 11 → 2` sums to 22.

**Output**: `true`.

## Solution explanation

```python
def has_path_sum(root: TreeNode | None, target: int) -> bool:
    def dfs(node: TreeNode | None, remaining: int) -> bool:
        if node is None:
            return False
        remaining -= node.val
        if not node.left and not node.right:
            return remaining == 0
        return dfs(node.left, remaining) or dfs(node.right, remaining)
    return dfs(root, target)
```

Walk-through on the tree above with `target = 22` (focus on the winning path):

| call               | node | remaining before | after subtracting | leaf? | decision                      |
|--------------------|------|------------------|-------------------|-------|-------------------------------|
| dfs(5, 22)         | 5    | 22               | 17                | no    | recurse left then right       |
| dfs(4, 17)         | 4    | 17               | 13                | no    | recurse left                  |
| dfs(11, 13)        | 11   | 13               | 2                 | no    | recurse left then right       |
| dfs(7, 2)          | 7    | 2                | -5                | yes   | -5 ≠ 0 → false                |
| dfs(2, 2)          | 2    | 2                | 0                 | yes   | 0 == 0 → **true**, propagates |

Once any leaf returns `true`, `or` short-circuits and the call chain returns `true` upward.

Correctness: at every recursive call, `remaining` is exactly `target` minus the sum of values on the path from root to the current node's parent. Subtracting `node.val` gives the residual that the subtree must produce. A leaf produces exactly its own value, so `remaining == 0` at the leaf is the right condition.

- **Time**: O(n) — every node visited at most once.
- **Space**: O(h) recursion depth.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Path Sum** — the canonical "does any root-to-leaf path sum to target" problem. | https://leetcode.com/problems/path-sum/ |
| Medium | **Path Sum II** — return *all* root-to-leaf paths summing to target; top-down with a mutable path list + backtracking. | https://leetcode.com/problems/path-sum-ii/ |
| Hard | **Binary Tree Maximum Path Sum** — actually best solved bottom-up; useful for *contrasting* the two paradigms. | https://leetcode.com/problems/binary-tree-maximum-path-sum/ |
