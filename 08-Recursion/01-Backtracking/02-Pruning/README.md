# Pruning in backtracking

## What is this

**Pruning** is the practice of cutting off whole subtrees of the decision tree the moment they become *provably hopeless*. Backtracking without pruning is exhaustive search — pruning is what makes backtracking practically fast on otherwise-exponential problems.

Common pruning techniques:

1. **Constraint violation pruning** — if the current partial state already violates a constraint, abandon.
2. **Bound pruning (branch-and-bound)** — if even the best possible completion of the current partial state cannot beat the best answer found so far, abandon.
3. **Duplicate skipping** — when choices contain equal elements, skip later identical choices that would generate the same subtree.
4. **Ordering for early failure** — sort choices so that high-information branches are tried first (e.g. most-constrained-variable in CSPs).
5. **Memoisation** — when the *same state* is reached via different paths, store and reuse the result.

## Why we use

- Without pruning, backtracking is O(branching^depth) — astronomical for non-trivial inputs.
- A well-placed prune can convert "infeasible" into "fast" (e.g. N-Queens, sudoku) without changing the algorithm's structure.
- Pruning is local: a small check at the top of `dfs(...)` may collapse millions of leaves.

## How to implement

The skeleton is identical to plain backtracking, with **early-return guards** added:

```
def dfs(state):
    if invalid(state):       return            # constraint pruning
    if cannot_beat_best(state): return         # bound pruning
    if state seen before:    return cached     # memoisation
    if is_solution(state):
        record(state); return
    for choice in ordered_choices(state):
        if skip_duplicate(choice): continue   # duplicate pruning
        apply(state, choice)
        dfs(state)
        undo(state, choice)
```

Python — **Subsets II** with duplicate pruning:

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums.sort()                # so duplicates sit next to each other
    res, path = [], []
    def dfs(start: int) -> None:
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue       # skip duplicate at this branching level
            path.append(nums[i])
            dfs(i + 1)
            path.pop()
    dfs(0)
    return res
```

Python — **Combination Sum II** with sort-skip + bound pruning:

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    res, path = [], []
    def dfs(start: int, remaining: int) -> None:
        if remaining == 0:
            res.append(path[:]); return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break          # bound prune: rest are even larger (sorted)
            if i > start and candidates[i] == candidates[i - 1]:
                continue       # duplicate prune
            path.append(candidates[i])
            dfs(i + 1, remaining - candidates[i])
            path.pop()
    dfs(0, target)
    return res
```

JavaScript — **N-Queens** with constraint sets (pruning by conflict):

```javascript
function totalNQueens(n) {
  const cols = new Set(), d1 = new Set(), d2 = new Set();
  let count = 0;
  function place(r) {
    if (r === n) { count++; return; }
    for (let c = 0; c < n; c++) {
      if (cols.has(c) || d1.has(r - c) || d2.has(r + c)) continue;  // constraint prune
      cols.add(c); d1.add(r - c); d2.add(r + c);
      place(r + 1);
      cols.delete(c); d1.delete(r - c); d2.delete(r + c);
    }
  }
  place(0);
  return count;
}
```

Invariant: every prune **provably** removes only invalid or suboptimal branches. A buggy prune that removes valid solutions is much worse than no prune at all.

## Duplicate pruning intuition

For `nums = [1, 1, 2]`, the decision tree for "pick a subset starting at index `start`":

```
                 start=0
        ┌───────────┼─────────────┐
       [1]         [1]'           [2]   ← second [1] is the duplicate of the first at start=0
       ...         ...            ...
```

Both `[1]` subtrees produce **identical** sets of subsets. Skipping the second one (`i > start and nums[i] == nums[i-1]`) cuts the tree in half without losing any answer.

## Bound pruning intuition

In **Combination Sum II**, candidates are sorted ascending. If `candidates[i] > remaining`, every later candidate is also `> remaining` — so the whole tail of the loop is hopeless. We `break` instead of `continue`. This single line can speed up the search dramatically.

## Which problems this approach solves in the real world

- **Sudoku / constraint satisfaction**: constraint propagation prunes 99%+ of branches.
- **Combinatorial optimisation**: TSP with branch-and-bound; knapsack with bound pruning.
- **Resource scheduling**: prune assignments that exceed budgets before exploring further.
- **Game search**: alpha-beta pruning is the chess/go canonical example.
- **Compilers**: register allocation with conflict graph pruning.
- **Test generation**: skip equivalence-class duplicates to keep test suites small.

## Pros and cons

**Pros**
- Can convert exponential search into practical runtime.
- Local: each prune is a guard at the top of a recursive call.
- Composable: multiple prunes stack to multiply their savings.
- Often the *single* difference between TLE and AC on competitive problems.

**Cons**
- A **wrong prune is silent** — it removes valid answers without raising an error.
- Bound pruning requires a fast and *tight* bound function — too loose and it doesn't help; too aggressive and it may prune optima.
- Duplicate pruning requires a sort and discipline (skip only at the *same branching level*).

## Limitations

- Doesn't change asymptotic worst-case complexity in the absence of structure — worst-case inputs (no duplicates, no bound tightness) still explode.
- For DAG-shaped state spaces, prune-via-cache (memoisation) is required; "skip if seen" needs a hashable state representation.
- Bound pruning depends on a problem-specific lower/upper bound oracle that you have to invent.

## One example

**Problem**: Given an array `candidates` (which may contain duplicates) and a target `target`, return **all unique combinations** of candidates summing to `target`. Each candidate may be used **at most once** in any combination.
Constraints: `1 ≤ candidates.length ≤ 100`, `1 ≤ candidates[i] ≤ 50`, `1 ≤ target ≤ 30`.

**Input**: `candidates = [10, 1, 2, 7, 6, 1, 5]`, `target = 8`
**Output** (any order):
```
[[1, 1, 6],
 [1, 2, 5],
 [1, 7],
 [2, 6]]
```

## Solution explanation

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()                                    # enables both prunes
    res, path = [], []
    def dfs(start: int, remaining: int) -> None:
        if remaining == 0:
            res.append(path[:]); return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                                    # bound prune
            if i > start and candidates[i] == candidates[i - 1]:
                continue                                 # duplicate prune
            path.append(candidates[i])
            dfs(i + 1, remaining - candidates[i])
            path.pop()
    dfs(0, target)
    return res
```

Walk-through (sorted = `[1, 1, 2, 5, 6, 7, 10]`, target = 8):

| call          | remaining | path  | tries (and prunes)                                       |
|---------------|-----------|-------|-----------------------------------------------------------|
| dfs(0, 8)     | 8         | []    | i=0 pick 1 → dfs(1, 7); i=1 dup skip; i=2 pick 2 → dfs(3,6); i=3 pick 5 → dfs(4,3); i=4 pick 6 → dfs(5,2); i=5 pick 7 → dfs(6,1); i=6 candidates[6]=10>8 → break |
| dfs(1, 7)     | 7         | [1]   | i=1 pick 1 → dfs(2, 6); i=2 pick 2 → dfs(3,5); i=3 pick 5 → dfs(4,2); i=4 pick 6 → dfs(5,1); i=5 pick 7 → dfs(6,0) → **commit [1,7]**; i=6 break |
| dfs(2, 6)     | 6         | [1,1] | i=2 pick 2 → dfs(3,4); ...; i=4 pick 6 → dfs(5,0) → **commit [1,1,6]** |
| dfs(3, 5)     | 5         | [1,2] | i=3 pick 5 → dfs(4,0) → **commit [1,2,5]** |
| dfs(3, 6)     | 6         | [2]   | i=4 pick 6 → dfs(5,0) → **commit [2,6]** |

The duplicate prune skips the second `1` at index 1 when entering with `start = 0`, so we don't generate `[1, 7]` twice. The bound prune cuts the loop when `candidates[i] > remaining`.

- **Time**: worst case still exponential; pruning makes typical inputs tractable.
- **Space**: O(target) recursion depth + O(output).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Combination Sum III** — `k` distinct digits 1–9 summing to `n`; tight bounds prune most branches. | https://leetcode.com/problems/combination-sum-iii/ |
| Medium | **Combination Sum II** — the canonical sort + duplicate-skip + bound-prune problem. | https://leetcode.com/problems/combination-sum-ii/ |
| Hard | **N-Queens II** — constraint-set pruning over columns and diagonals; classic example of pure constraint pruning. | https://leetcode.com/problems/n-queens-ii/ |
