# Dynamic Programming Patterns

## Folder structure

```
12-Dynamic-programming/
├── README.md
├── 01-Core/
│   ├── 01-1D/README.md
│   └── 02-2D/README.md
├── 02-Transition-type/
│   ├── 01-Linear-DP/README.md
│   ├── 02-Grid-DP/README.md
│   └── 03-Decision-DP/README.md
├── 03-Pattern-types/
│   ├── 01-Knapsack/README.md
│   ├── 02-Sequence-DP/README.md
│   ├── 03-Partition-DP/README.md
│   └── 04-Interval-DP/README.md
├── 04-Advanced/
│   ├── 01-Bitmask/README.md
│   ├── 02-Digit-DP/README.md
│   └── 03-DP-on-trees/README.md
├── 05-Optimization/
│   ├── 01-Memoization/README.md
│   └── 02-Tabulation/README.md
├── 06-LCS/README.md
└── 07-LIS/README.md
```

## What is this

Dynamic programming (DP) is the technique of solving problems with overlapping subproblems and optimal substructure by storing each subproblem's answer once and reusing it. Whenever a recursive solution would recompute the same sub-call many times, DP turns it into a polynomial-time algorithm via memoization (top-down) or tabulation (bottom-up).

DP problems organise along five axes: **core** (1D state vs 2D state), **transition type** (linear / grid / decision-based), **pattern types** (knapsack, sequence DP, partition DP, interval DP), **advanced** (bitmask DP, digit DP, DP on trees), and **optimisation** (memoization vs tabulation, space-rolling). Most interview DP problems fall into one of these buckets; recognising which bucket is half the battle.

## Why we use

- Turns exponential brute force into polynomial-time solutions for many optimisation problems.
- Memoization gives an almost-free speedup on top of recursive code.
- Once the state and transition are right, the implementation is mechanical.
- Pattern recognition (knapsack, LCS, LIS) catches a huge slice of optimisation problems.

## How to implement

```
1. Define the STATE — what parameters uniquely determine a subproblem?
2. Define the TRANSITION — how does a subproblem combine smaller ones?
3. Identify the BASE CASE.
4. Choose direction:
   - top-down: recurse + memoize (fast to write, slower constants)
   - bottom-up: fill a table iteratively (often faster, easier to space-optimise)
5. Validate complexity: states * transitions per state.
```

Subpatterns in this folder:

- **01-Core** — 1D and 2D state.
- **02-Transition-type** — linear DP, grid DP, decision DP.
- **03-Pattern-types** — knapsack, sequence DP, partition DP, interval DP.
- **04-Advanced** — bitmask DP, digit DP, DP on trees.
- **05-Optimization** — memoization vs tabulation; space-rolling.
- **06-LCS** — longest common subsequence (and its family).
- **07-LIS** — longest increasing subsequence (and its family).

## Which problems this approach solves in the real world

- Resource allocation under capacity constraints (knapsack variants).
- Sequence alignment in bioinformatics (Needleman-Wunsch, Smith-Waterman).
- Edit distance and spell correction.
- Optimal trade execution in finance.
- Path planning under cost constraints.
- Compiler optimisations (instruction scheduling, register allocation).

## Pros and cons

**Pros**
- Turns exponential into polynomial — often dramatic speedups.
- Mechanical once the state is identified.
- Many problems share the same recipe (LCS, edit distance, longest-palindrome).
- Space-rolling can drop O(n²) memory to O(n) easily.

**Cons**
- Defining the right state is the actual hard part — and rarely obvious.
- Wrong state ordering leads to off-by-one errors or wrong answers.
- Memoization can blow memory on large state spaces.
- Bitmask DP only works for n ≤ ~20.

## Limitations

- Doesn't help when subproblems don't overlap or substructure isn't optimal.
- Continuous state spaces need approximation or different techniques.
- Online / streaming variants often can't precompute a full table.
- Very-high-dimension DP is intractable; needs approximation algorithms.
