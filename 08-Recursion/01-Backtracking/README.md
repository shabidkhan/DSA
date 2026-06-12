# Backtracking

## Folder structure

```
01-Backtracking/
├── README.md
├── 01-Exploration/
│   ├── README.md
│   ├── 01-Decision-tree/README.md
│   ├── 02-Choose-explore-unchoose/README.md
│   ├── 03-Subsets/README.md
│   ├── 04-Permutations/README.md
│   ├── 05-Word-search-on-grid/README.md
│   ├── 06-Palindrome-partitioning/README.md
│   └── 07-N-Queens/README.md
└── 02-Pruning/README.md
```

## What is this

Backtracking is a systematic way to enumerate solutions to a problem by extending a partial candidate one decision at a time and abandoning it the moment it cannot lead to a valid full solution. It is DFS over an implicit decision tree: each node is a partial state, each edge is a choice, and each leaf is either a complete solution or a dead end.

The defining move is *undoing* the choice when returning from the recursive call. This restores the partial state and lets the caller try the next alternative without polluting other branches. Done right, the same scratch array or board can serve every branch — memory cost is the depth of the tree, not its width.

## Why we use

- Lets a single recursive skeleton enumerate subsets, permutations, paths, partitions, and constraint solutions.
- The choose / explore / unchoose pattern keeps mutation local — one scratch buffer serves every branch.
- Pruning lets you skip whole subtrees of the decision space the moment they become infeasible.
- Composes naturally with constraints, ordering, and memoization to attack NP-shaped problems within practical limits.

## How to implement

```text
function backtrack(state):
    if isComplete(state):
        record(copy(state))
        return
    for choice in candidates(state):
        if not feasible(state, choice): continue   # pruning
        apply(state, choice)
        backtrack(state)
        undo(state, choice)                        # restore!
```

Two key disciplines: (1) `record` must copy because `state` is mutated across branches; (2) `undo` must be exact — every mutation in `apply` gets reversed.

Subpatterns in this folder:

- `01-Exploration/` — the choose / explore / unchoose engine and its canonical shapes (subsets, permutations, word search, palindrome partitioning, N-Queens).
- `02-Pruning/` — techniques to skip infeasible branches early (constraint propagation, bounding, duplicate-skip on sorted input, ordering heuristics).

## Which problems this approach solves in the real world

- Generating all valid configurations of a system subject to constraints (e.g., timetable solver).
- Search-based test generation that enumerates input combinations until a failing one is found.
- Sudoku, crossword, and constraint puzzles — the classic textbook use case.
- Exhaustive route exploration on a small graph where shortest-path tools are overkill.
- Compiler synthesis: searching the small space of register assignments under constraints.
- Lock pattern / PIN enumeration in penetration testing within a bounded search space.

## Pros and cons

**Pros**
- One pattern covers a huge family of enumeration problems.
- Memory stays small — depth of recursion, not width.
- Pruning can collapse exponential spaces to tractable ones in practice.
- Solutions can be streamed (yielded one-by-one) without materializing the full set.

**Cons**
- Worst case is exponential — without pruning it can be unusable on real inputs.
- Off-by-one in `undo` corrupts the state for sibling branches and is brutal to debug.
- Recursion depth and per-frame copies can become a hot spot.
- Hard to parallelize naively because branches share mutable state.

## Limitations

- Not for problems with overlapping subproblems and optimal substructure — that is DP territory.
- Pruning quality is everything; problems with weak constraints degenerate to brute force.
- Iterative rewriting is painful — the explicit stack must also model the "undo" log.
- Without careful ordering, even pruning can leave the search wandering through useless prefixes for a long time.
