# Decision tree (mental model for backtracking)

## What is this

The **decision tree** is the conceptual map of every choice a backtracking algorithm could make. Each internal node represents a *decision point* (which element to pick next, include or exclude, where to place a queen). Each edge is a specific choice. Each leaf is a complete configuration — either a valid answer or a dead end.

Backtracking is then just **DFS over this tree**: we follow a branch down, commit choices on the way in, undo them on the way out, and harvest leaves that satisfy our predicate.

Drawing or visualising the decision tree turns "is my recursion correct?" into "does my tree have the right shape?", which is a much easier debugging question.

## Why we use

- Backtracking is hard to reason about by code alone — the decision tree makes branching factor, depth, and pruning *visual*.
- Estimating runtime becomes mechanical: total work ≈ number of nodes in the tree ≈ branching^depth (modulo pruning).
- Spotting redundancy: nodes that represent the same state appear multiple times in many decision trees, hinting that memoisation / pruning is possible.
- The structure exposes whether the algorithm is **enumerating subsets** (depth = n, branching = 2), **permutations** (depth = n, branching shrinks: n, n−1, …), or **k-choose-from-set** (variable branching).

## How to read a decision tree

For each node:
- The **state** at that node (current partial solution + remaining choices).
- The **edges** are labelled with the action you take (pick element `x`, skip element `x`, place a queen in column `c`).
- **Leaves** are either complete solutions or pruned ("dead ends").

## Example tree — subsets of `[1, 2, 3]`

At each step, decide whether to **include** the current element.

```
                      []                    (decide about 1)
                /             \
          [1]                  []            (decide about 2)
         /    \               /    \
       [1,2]  [1]           [2]    []        (decide about 3)
       /  \   /  \         /  \   /  \
   [1,2,3][1,2][1,3][1] [2,3][2][3]  []      <-- 8 leaves = 2^3 subsets
```

Branching factor 2, depth n = 3 → exactly 2^3 = 8 leaves, one per subset.

## Example tree — permutations of `[1, 2, 3]`

At each step, decide which **remaining** element to place next.

```
                       []
            /          |          \
         [1]          [2]         [3]
         /  \         / \         / \
     [1,2] [1,3]  [2,1][2,3]  [3,1][3,2]
        |    |      |    |      |    |
   [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]
```

Branching shrinks each level (3 → 2 → 1) → 3! = 6 leaves, one per permutation.

## How to implement

```
def dfs(state):
    if is_terminal(state):
        record(state)
        return
    for choice in choices(state):
        if not promising(state, choice):
            continue              # pruning
        apply(state, choice)
        dfs(state)
        undo(state, choice)
```

Python — subsets via decision tree (include/exclude):

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(i: int) -> None:
        if i == len(nums):
            res.append(path[:])      # leaf: commit copy
            return
        # branch 1: include nums[i]
        path.append(nums[i])
        dfs(i + 1)
        path.pop()
        # branch 2: exclude nums[i]
        dfs(i + 1)
    dfs(0)
    return res
```

JavaScript — same tree, depth-first walk:

```javascript
function subsets(nums) {
  const res = [], path = [];
  function dfs(i) {
    if (i === nums.length) { res.push([...path]); return; }
    path.push(nums[i]);
    dfs(i + 1);
    path.pop();
    dfs(i + 1);
  }
  dfs(0);
  return res;
}
```

## Why this matters for runtime

- Number of leaves ≤ branching factor ^ depth.
- Total work = work per node × number of nodes (≈ branching × leaves).
- Pruning removes whole **subtrees** of the decision tree, not just individual nodes — that's where backtracking gets its leverage.

## Which problems this approach solves in the real world

- **Combinatorial search** — anywhere you enumerate selections (menu plans, scheduling, lineup picks).
- **Constraint satisfaction** — N-Queens, sudoku, map colouring, course assignment.
- **Game tree exploration** — chess, go, tic-tac-toe (with minimax pruning).
- **Test case generation** — exhaustively enumerate input shapes within a bounded grammar.
- **Optimization problems** — branch and bound on top of a decision tree (TSP, knapsack).

## Pros and cons

**Pros**
- A picture you can draw makes correctness arguments concrete.
- Identifies pruning opportunities (whole subtrees collapse).
- Identifies repeated states for memoisation.
- Gives a precise time-complexity bound: O(leaves × work_per_leaf).

**Cons**
- For high branching factors (game trees, TSP), the tree is astronomically large — drawing the full tree is impossible.
- Mental model only — the tree is implicit in code; mismatch between drawing and code is a common bug source.
- Doesn't itself reduce complexity — it's a thinking tool, not an algorithm.

## Limitations

- Some problems have *DAG-shaped* search spaces (states reachable via multiple paths) — drawing as a tree double-counts; switch to memoisation.
- For continuous search spaces, "decision tree" doesn't directly apply.
- For very deep trees, the decision tree's depth becomes the recursion stack depth — risk of overflow.

## One example

**Problem**: Given a set of distinct integers `nums`, return all possible **subsets** (the power set). The solution must not contain duplicates.
Constraints: `1 ≤ nums.length ≤ 10`, all integers in `[-10, 10]`.

**Input**: `nums = [1, 2, 3]`
**Output**: `[[], [3], [2], [2,3], [1], [1,3], [1,2], [1,2,3]]` (any order acceptable).

## Solution explanation

Use the include/exclude decision tree:

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(i: int) -> None:
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i]); dfs(i + 1); path.pop()
        dfs(i + 1)
    dfs(0)
    return res
```

Walk-through for `nums = [1, 2, 3]` — sequence of leaves encountered, with `path` at the moment of `res.append`:

| call sequence (action)          | path at leaf | committed subset |
|---------------------------------|--------------|------------------|
| inc 1 → inc 2 → inc 3 → leaf    | [1, 2, 3]    | [1, 2, 3]        |
| inc 1 → inc 2 → exc 3 → leaf    | [1, 2]       | [1, 2]           |
| inc 1 → exc 2 → inc 3 → leaf    | [1, 3]       | [1, 3]           |
| inc 1 → exc 2 → exc 3 → leaf    | [1]          | [1]              |
| exc 1 → inc 2 → inc 3 → leaf    | [2, 3]       | [2, 3]           |
| exc 1 → inc 2 → exc 3 → leaf    | [2]          | [2]              |
| exc 1 → exc 2 → inc 3 → leaf    | [3]          | [3]              |
| exc 1 → exc 2 → exc 3 → leaf    | []           | []               |

Exactly 8 leaves = 2^3 subsets.

Correctness: every subset corresponds to a unique sequence of include/exclude decisions on each element — a unique root-to-leaf path. Both branches are taken at every internal node, so every leaf is visited, and `path` at the leaf is the partial subset built by following that path.

- **Time**: O(n · 2^n) — 2^n leaves, copying `path` is O(n).
- **Space**: O(n) recursion depth + O(n · 2^n) output.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Letter Case Permutation** — at each letter, branch include-lowercase / include-uppercase. Classic small decision tree. | https://leetcode.com/problems/letter-case-permutation/ |
| Medium | **Subsets** — the canonical problem; 2^n leaf decision tree. | https://leetcode.com/problems/subsets/ |
| Hard | **N-Queens** — branching factor n at each row; pruning by column / diagonal conflict prunes huge subtrees. | https://leetcode.com/problems/n-queens/ |
