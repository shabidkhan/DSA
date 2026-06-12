# DP Core

## Folder structure

```
01-Core/
├── README.md
├── 01-1D/README.md
└── 02-2D/README.md
```

## What is this

The core of dynamic programming is the *state*: a tuple of variables that summarizes everything about a partial solution that matters for the future. Once you pick the right state, the transition (how one state's answer depends on smaller states) usually writes itself. Most DP problems boil down to deciding whether the state is one-dimensional (a single index/length/capacity) or two-dimensional (a pair of indices, or position + carried context).

The 1D / 2D distinction isn't dogmatic — it's a guide to dimensionality budget. 1D DPs (Fibonacci, climbing stairs, house robber) iterate over a single index. 2D DPs (LCS, edit distance, grid pathfinding) iterate over two coordinates and depend on neighbours in the table. Higher-dimensional DPs exist but become harder to fit in memory; many of those are recast as 2D after careful state compression.

## Why we use

- "Pick the state" is the entire art of DP — these two patterns cover the bulk of textbook problems.
- 1D DP gives O(n) solutions to problems that look exponential.
- 2D DP cleanly handles two-sequence comparisons (LCS, edit distance) and 2D grids.
- Both can be space-optimised (rolling arrays) once the transition is understood.

## How to implement

```text
# 1D — state = index i; answer at i depends on f(i-1), f(i-2), ...
function dp1d(n):
    f = array of size n+1
    f[0] = base
    for i in 1..n:
        f[i] = combine(f[i-1], f[i-2], ..., input[i])
    return f[n]

# 2D — state = (i, j); answer depends on f(i-1, j), f(i, j-1), f(i-1, j-1)
function dp2d(rows, cols):
    f = matrix of size (rows+1) x (cols+1)
    initialise borders
    for i in 1..rows:
        for j in 1..cols:
            f[i][j] = combine(f[i-1][j], f[i][j-1], f[i-1][j-1], inputs)
    return f[rows][cols]
```

Subpatterns in this folder:

- `01-1D/` — single-index state; Fibonacci-class transitions, house robber, climbing stairs.
- `02-2D/` — pair-index state; LCS, edit distance, grid min-path-sum.

## Which problems this approach solves in the real world

- Decision systems that pick the best action in a sequence (recommendation re-ranking).
- Inventory planning where today's order depends on yesterday's stock and tomorrow's forecast.
- Diff and merge tools (LCS on lines is what `git diff` shows).
- Autocorrect and spell-check (edit distance).
- Path planning on grid worlds for game AI and warehouse robots.
- Bioinformatics sequence alignment (Needleman-Wunsch is 2D DP).

## Pros and cons

**Pros**
- Reduces exponential brute force to polynomial time when the state is right.
- The transition is mechanical once the state is chosen.
- Space-optimisation is often a one-line change (rolling array).
- The DP table doubles as a "why is this the answer" trace via backtracking.

**Cons**
- Choosing the wrong state silently kills correctness — bug doesn't show up as a crash.
- Memory cost grows multiplicatively with each new state dimension.
- Iteration order matters: dependencies must be filled before they're read.
- Recursion + memoization (top-down) is easier to discover; tabulation (bottom-up) is easier to optimise — switching between them takes practice.

## Limitations

- DP fails when the optimal answer cannot be decomposed by sub-states (e.g., problems with global constraints).
- High-dimensional DP (4D, 5D) is usually infeasible without state compression.
- Problems with continuous state spaces need discretization, which introduces error.
- DP doesn't naturally parallelize — neighbours in the table are dependencies.
