# Exploration

## Folder structure

```
01-Exploration/
├── README.md
├── 01-Decision-tree/README.md
├── 02-Choose-explore-unchoose/README.md
├── 03-Subsets/README.md
├── 04-Permutations/README.md
├── 05-Word-search-on-grid/README.md
├── 06-Palindrome-partitioning/README.md
└── 07-N-Queens/README.md
```

## What is this

Exploration is the *engine* of backtracking: the act of walking the implicit decision tree, making one choice at each node and recursing. Every backtracking problem reduces to two questions: what is a "choice" at each step, and when has the partial state become a complete solution. Once those are answered, the same skeleton drives subsets, permutations, partitions, grid searches, and constraint puzzles.

The unifying mental model is the decision tree: the root is the empty partial solution, each level represents one decision, and each leaf is either a complete candidate or a dead end. Different problem shapes correspond to different tree shapes (binary include/exclude, n-ary choose-an-element, m×n grid steps), but they all share the same choose / explore / unchoose body.

## Why we use

- A single recursion skeleton covers a huge family of enumeration problems.
- Thinking explicitly in terms of "decision tree shape" makes the recursion contract obvious before any code is written.
- The mutate-then-undo discipline lets one scratch buffer serve every branch — memory is tree depth, not tree width.
- Generators / yield variants let solutions stream out without holding all of them in memory.

## How to implement

```text
function explore(state, choicesLeft):
    if isComplete(state):
        record(copy(state)); return
    for choice in nextChoices(state, choicesLeft):
        apply(state, choice)
        explore(state, choicesLeft - {choice})
        undo(state, choice)
```

Variant per problem shape:

- Subsets: at each index decide include / exclude → binary tree of depth n, 2^n leaves.
- Permutations: at each position pick any unused element → n! leaves.
- Word search on grid: at each cell branch to 4 neighbours, skip if visited or mismatch.
- Partitioning: at each prefix cut a valid chunk and recurse on the tail.

Subpatterns in this folder:

- `01-Decision-tree/` — the mental model and how problem shape determines tree shape.
- `02-Choose-explore-unchoose/` — the canonical recursion template.
- `03-Subsets/` — include/exclude binary tree.
- `04-Permutations/` — order matters; used / not-used bookkeeping.
- `05-Word-search-on-grid/` — DFS with in-place visited marking and backtrack.
- `06-Palindrome-partitioning/` — cut into chunks satisfying a predicate.
- `07-N-Queens/` — strong constraint propagation across rows / columns / diagonals.

## Which problems this approach solves in the real world

- Test-case generation: enumerate combinations of feature flags subject to compatibility rules.
- Configuration solvers (Kconfig, NPM peer-dep resolution) for small subproblems.
- Generating valid HTML/JSON fragments for fuzz testing.
- Finding all matching strings within a Trie-backed dictionary on a Boggle-style grid.
- Brute-force credential or token enumeration in authorized security testing.
- Synthesizing small programs from a DSL by trying production rules.

## Pros and cons

**Pros**
- One reusable template for the entire family.
- Easy to add constraints by extending `nextChoices` and `apply` / `undo`.
- Solutions can be streamed or counted without storing them all.
- Trivial to parallelise per top-level choice if branches are independent.

**Cons**
- Worst case is exponential — without good pruning it is unusable.
- Recursion depth equals the longest solution length; deep states risk stack overflow.
- `undo` must mirror `apply` exactly; mismatches corrupt sibling branches.
- Copying `state` at each `record` becomes a hot spot for very small solutions in huge trees.

## Limitations

- Not for problems with overlapping subproblems — that is DP, not exploration.
- Tree-shape choice matters: a bad ordering of decisions can balloon the search space.
- Many problems need additional bookkeeping (visited sets, frequency maps) that complicate the template.
- Iterative rewriting requires explicitly modelling the choose-stack — rarely worth it.
