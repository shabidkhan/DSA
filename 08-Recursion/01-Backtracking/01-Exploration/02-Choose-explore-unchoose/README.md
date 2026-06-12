# Choose → Explore → Unchoose (the canonical backtracking template)

## What is this

The bedrock template for backtracking. At every decision point:

1. **Choose** — mutate a shared state to reflect making a choice (append to a path list, mark a cell visited, place a queen).
2. **Explore** — recurse into the resulting subproblem.
3. **Unchoose** — undo the mutation, so the parent's iteration over alternatives starts from a clean slate.

This pattern *shares* a single mutable container (path, board, visited set) across all recursive calls — instead of *copying* state at every level. The "unchoose" step is the price you pay for that efficiency: it must exactly mirror the "choose" step.

The alternative is **functional recursion** (pass an immutable updated state to the child). Functional is simpler but allocates copies; choose-explore-unchoose is faster but requires discipline.

## Why we use

- O(depth) extra memory for the path — vs. O(depth) per call for the functional style.
- Faster in practice: no list-copy on every call.
- Idiomatic in interviews and competitive code — recognisable on sight.
- Works uniformly for permutations, subsets, combinations, N-Queens, sudoku, word search, etc.

## How to implement

```
path = []                # shared mutable state
def dfs(...):
    if reached terminal:
        record snapshot(path)
        return
    for choice in choices:
        if pruned(choice): continue
        choose(choice)            # mutate state
        dfs(...)
        unchoose(choice)          # undo
```

Python — permutations (choose/explore/unchoose):

```python
def permutations(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)
    def dfs() -> None:
        if len(path) == len(nums):
            res.append(path[:])    # snapshot — important!
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            # CHOOSE
            used[i] = True
            path.append(x)
            # EXPLORE
            dfs()
            # UNCHOOSE
            path.pop()
            used[i] = False
    dfs()
    return res
```

JavaScript — N-Queens (choose/explore/unchoose with a column/diag set):

```javascript
function solveNQueens(n) {
  const res = [], cols = new Set(), d1 = new Set(), d2 = new Set();
  const board = Array.from({ length: n }, () => '.'.repeat(n));
  function place(r) {
    if (r === n) { res.push([...board]); return; }
    for (let c = 0; c < n; c++) {
      if (cols.has(c) || d1.has(r - c) || d2.has(r + c)) continue;
      // CHOOSE
      cols.add(c); d1.add(r - c); d2.add(r + c);
      board[r] = '.'.repeat(c) + 'Q' + '.'.repeat(n - c - 1);
      // EXPLORE
      place(r + 1);
      // UNCHOOSE
      cols.delete(c); d1.delete(r - c); d2.delete(r + c);
      board[r] = '.'.repeat(n);
    }
  }
  place(0);
  return res;
}
```

Invariant: at the entry of every call to `dfs`, `path` contains exactly the choices the call chain has made so far — no more, no less. At the *exit*, `path` is restored to the same state it had on entry.

## When to choose mutation vs. functional copy

| You want…                                                | Use mutation + unchoose | Use functional copy |
|----------------------------------------------------------|-------------------------|---------------------|
| Best performance, ok with discipline                     | ✓                       |                     |
| Solving competitive problems with tight time limits      | ✓                       |                     |
| Beginner-friendly code, easy proofs                      |                         | ✓                   |
| Concurrent / immutable-state architecture                |                         | ✓                   |
| Multi-threaded recursion (rare)                          |                         | ✓                   |

The functional equivalent of permutations:

```python
def permutations_functional(nums: list[int]) -> list[list[int]]:
    if not nums:
        return [[]]
    out = []
    for i, x in enumerate(nums):
        for tail in permutations_functional(nums[:i] + nums[i+1:]):
            out.append([x] + tail)
    return out
```

Cleaner — but quadratic copying overhead.

## Which problems this approach solves in the real world

- **Sudoku solver** — fill a cell, recurse, undo if stuck.
- **Crossword filler** — place a word in a slot, recurse, remove.
- **Scheduler** — assign a task to a slot, recurse, unassign.
- **Maze solving** — mark cell visited, recurse to neighbours, unmark.
- **DNA assembly** — extend a contig, recurse, retract.
- **Compilers** — register allocation by trial assignment, recurse, undo on conflict.

## Pros and cons

**Pros**
- O(depth) shared state — minimum memory footprint.
- The pattern is identical across many problems — recognise it once, apply everywhere.
- Easy to add pruning (skip branches inside the for-loop).
- Easy to add early termination (return as soon as one solution found).

**Cons**
- **Forgetting to unchoose** is the single most common backtracking bug — state leaks into sibling branches and answers come out garbled.
- **Forgetting to snapshot** (`path[:]` or `[...path]`) is the second most common bug — the recorded answer mutates as recursion continues.
- The mutation makes debug prints lie — what you printed at recursion entry may not be what's in memory anymore by the time you read the log.

## Limitations

- Doesn't work well with concurrency (mutable shared state).
- For DAG-shaped state spaces (same state reachable by multiple paths), choose-explore-unchoose still works but you waste work — add memoisation instead.
- For very deep recursion, the choose/unchoose log isn't free — each is O(1), but n of them is O(n) extra constant.

## One example

**Problem**: Given an array `nums` of distinct integers, return all possible **permutations** in any order.
Constraints: `1 ≤ nums.length ≤ 6`, `-10 ≤ nums[i] ≤ 10`.

**Input**: `nums = [1, 2, 3]`
**Output**: `[[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]`

## Solution explanation

```python
def permutations(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)
    def dfs() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True; path.append(x)
            dfs()
            path.pop(); used[i] = False
    dfs()
    return res
```

Walk-through — only the leaf events (where we commit a snapshot) on `[1, 2, 3]`:

| pick order            | path at leaf | committed |
|-----------------------|--------------|-----------|
| 1, 2, 3               | [1,2,3]      | [1,2,3]   |
| 1, 3, 2               | [1,3,2]      | [1,3,2]   |
| 2, 1, 3               | [2,1,3]      | [2,1,3]   |
| 2, 3, 1               | [2,3,1]      | [2,3,1]   |
| 3, 1, 2               | [3,1,2]      | [3,1,2]   |
| 3, 2, 1               | [3,2,1]      | [3,2,1]   |

Exactly 3! = 6 leaves.

Correctness: at the entry to any `dfs()` call, `path` is the prefix of choices made so far, and `used[i]` records exactly which elements appear in `path`. The loop tries each unused element as the next choice, recurses, then undoes — preserving the invariant for the parent's next iteration. When `len(path) == len(nums)`, the prefix has covered every element exactly once — a valid permutation.

- **Time**: O(n · n!) — n! permutations, each costs O(n) to copy.
- **Space**: O(n) recursion + O(n) path + O(n · n!) output.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Letter Combinations of a Phone Number** — for each digit, append a letter, recurse, pop. | https://leetcode.com/problems/letter-combinations-of-a-phone-number/ |
| Medium | **Permutations** — the canonical problem above. | https://leetcode.com/problems/permutations/ |
| Hard | **Sudoku Solver** — at each empty cell, try digits 1–9 with full choose/explore/unchoose of row/col/box constraints. | https://leetcode.com/problems/sudoku-solver/ |
