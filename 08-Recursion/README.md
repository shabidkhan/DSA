# Recursion Patterns

## Folder structure

```
08-Recursion/
├── README.md
├── 01-Backtracking/
│   ├── 01-Exploration/
│   │   ├── 01-Decision-tree/README.md
│   │   ├── 02-Choose-explore-unchoose/README.md
│   │   ├── 03-Subsets/README.md
│   │   ├── 04-Permutations/README.md
│   │   ├── 05-Word-search-on-grid/README.md
│   │   ├── 06-Palindrome-partitioning/README.md
│   │   └── 07-N-Queens/README.md
│   └── 02-Pruning/README.md
└── 02-Divide-and-conquer/
    ├── 01-Merge-sort-pattern/README.md
    ├── 02-Quick-select/README.md
    └── 03-Count-inversions/README.md
```

## What is this

Recursion is the technique of solving a problem by reducing it to a smaller instance of the same problem and combining the result. Two algorithmic families dominate the space: **backtracking** (systematically try choices, undo on dead-end, explore the whole decision tree) and **divide and conquer** (split the problem into independent halves, solve each recursively, merge the results).

Backtracking is the engine behind subsets, permutations, N-queens, word search, and palindrome partitioning — anything where the solution is a sequence of decisions. Divide and conquer powers merge sort, quick select, count-inversions, and many tree problems. Both rely on the same template — base case, recursive step, optional combine — but their flavours differ: backtracking explores; divide and conquer splits.

## Why we use

- Many problems have a naturally recursive structure that's awkward to express iteratively.
- Backtracking gives systematic, complete exploration with pruning.
- Divide and conquer turns linear scans into O(n log n) algorithms.
- Recursion makes code dramatically shorter than equivalent iterative versions.

## How to implement

Pick the family by the problem shape:

```
backtracking       — "build a solution; try, recurse, undo"
divide & conquer   — "split, solve each half, combine"

template:
def solve(state):
    if base_case(state):
        record_or_return()
        return
    for choice in choices(state):
        apply(choice)
        solve(extended state)
        undo(choice)            # only for backtracking
```

Subpatterns in this folder:

- **01-Backtracking** — exploration (decision-tree, choose-explore-unchoose, subsets, permutations, N-queens, word search, palindrome partitioning) and pruning.
- **02-Divide-and-conquer** — merge-sort pattern, quick-select, count inversions.

## Which problems this approach solves in the real world

- Constraint satisfaction (Sudoku, scheduling, configuration).
- AI search (game-tree minimax, chess move enumeration).
- Parsers (recursive descent for languages and protocols).
- Filesystem walks and directory enumeration.
- Image segmentation via flood fill.
- Combinatorial generation (test inputs, fuzzing, password spaces).

## Pros and cons

**Pros**
- Code mirrors the problem statement, often 10x shorter than iterative.
- Backtracking gives exhaustive search with simple pruning hooks.
- Divide and conquer enables O(n log n) sorting and selection.
- Easy to memoize for DP-style speedups.

**Cons**
- Stack overflow on deep recursion (especially Python's 1000-frame default).
- Backtracking is exponential without aggressive pruning.
- Mutable state during recursion (visited sets, board cells) needs careful undo.
- Mixing return values and side effects is a common source of bugs.

## Limitations

- Pure recursion in non-tail-call languages can be slow due to call overhead.
- Backtracking time can blow up on adversarial inputs — must measure.
- Cannot solve problems with non-decomposable state (continuous flows).
- Concurrent or distributed variants need fundamentally different machinery.
