# N-Queens backtracking

## What is this

A backtracking algorithm that places `n` queens on an `n × n` chessboard such that no two queens attack each other (no shared row, column, or diagonal). Queens are placed **one row at a time**: for each row, you try every column, and for each column you recurse if and only if it doesn't conflict with queens already placed. When a placement leads to a dead end, you **undo it** ("backtrack") and try the next column. The search explores a tree of partial placements and prunes aggressively using conflict sets.

## Why we use

- Demonstrates the canonical "place-recurse-undo" backtracking skeleton, applicable to any constraint-satisfaction problem.
- Heavy pruning (rejecting whole subtrees as soon as a constraint is violated) turns an apparent `n^n` search into something tractable for moderate `n`.
- O(1) constraint checks using three integer sets (columns, two diagonal families) make every recursion step fast.

## How to implement

```
solve(row):
    if row == n:
        record current board
        return
    for col in 0..n-1:
        if col not in cols
           and (row - col) not in diag1
           and (row + col) not in diag2:
            place queen at (row, col)
            add col, row-col, row+col to the three sets
            solve(row + 1)
            remove the additions  (undo)
```

Python — count distinct solutions to N-Queens:

```python
def total_n_queens(n: int) -> int:
    cols, diag1, diag2 = set(), set(), set()
    count = 0

    def place(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            place(row + 1)
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)

    place(0)
    return count
```

Invariant: at the moment we enter `place(row)`, every row `0..row-1` already contains exactly one queen, no two of them attack, and `cols`, `diag1`, `diag2` are the **exact** set of occupied columns and diagonals. The undo step preserves this invariant on the way out of recursion.

## Which problems this approach solves in the real world

- **Constraint scheduling** (room/teacher assignment with conflict rules) — same place/conflict/backtrack structure.
- **Sudoku solvers** — try a digit, propagate constraints, undo on conflict.
- **CSP-style configurators** (e.g. product builders where each option excludes others).
- **Layout placement** in chip design with adjacency conflicts.
- **Test-case generation** where each chosen value rules out others (combinatorial coverage with constraints).

## Pros and cons

**Pros**
- Memory-light: only O(n) recursion depth + three O(n) sets.
- Conflict checks are O(1) using sets / boolean arrays / bitmasks.
- Pruning is automatic: each invalid branch is abandoned immediately.
- The same skeleton solves many other CSPs with minimal code change.

**Cons**
- Worst-case time is still exponential — feasible up to roughly `n ≈ 14` for counting all solutions.
- Naive ordering (left-to-right by column) misses heuristic speedups; smarter variable/value ordering can be much faster.
- Each "place / undo" pair must be perfectly symmetric — a missed undo silently corrupts further search.

## Limitations

- Doesn't scale to large `n` for "all solutions" enumeration; for "any solution" or "count modulo prime", specialised techniques (bitmask DP, polynomial methods) win.
- Doesn't handle generalised attack patterns (e.g. knight + queen hybrid) without rewriting the conflict checks.
- Bitmask version is faster but has the same asymptotic complexity.

## One example

**Problem**: Given `n`, return the **total number** of distinct solutions to the n-queens puzzle. Constraints: `1 ≤ n ≤ 9`.

**Input**: `n = 4`
**Output**: `2`

## Solution explanation

Using the function above, `total_n_queens(4)` explores rows in order. The two solutions for n=4 are columns `[1, 3, 0, 2]` and `[2, 0, 3, 1]`.

Walk-through of the search on `n = 4` (only successful and notable failed branches shown):

| row | col tried | conflict?                       | action               |
|-----|-----------|---------------------------------|----------------------|
| 0   | 0         | ok                              | recurse              |
| 1   | 0,1       | col 0 / diag conflict           | skip                 |
| 1   | 2         | ok                              | recurse              |
| 2   | 0,1,2,3   | every column conflicts          | dead end → backtrack |
| 1   | 3         | ok                              | recurse              |
| 2   | 1         | ok                              | recurse              |
| 3   | 0,1,2,3   | all conflict                    | dead end → backtrack |
| ... | ...       | ...                             | (eventually finds [1,3,0,2]) |
| 0   | 1         | ok                              | leads to [1,3,0,2]   |
| 0   | 2         | ok                              | leads to [2,0,3,1]   |
| 0   | 3         | mirror of col 0                 | leads to nothing new |

Why diagonals collapse to two integers: on a chess board, every cell `(r, c)` lies on exactly one "/" diagonal where `r + c` is constant, and one "\" diagonal where `r - c` is constant. So a queen at `(row, col)` is in conflict with any other queen sharing `row`, `col`, `row + col`, or `row - col` — and `set` membership checks are O(1).

- **Time**: O(n!) worst case; in practice far less due to pruning.
- **Space**: O(n) recursion + O(n) per conflict set.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Letter Tile Possibilities** — backtracking enumeration with frequency-counter pruning. | https://leetcode.com/problems/letter-tile-possibilities/ |
| Medium | **N-Queens II** — count distinct solutions to the n-queens puzzle. | https://leetcode.com/problems/n-queens-ii/ |
| Hard   | **N-Queens** — return all distinct board configurations as lists of strings. | https://leetcode.com/problems/n-queens/ |
