# DP Pattern Types

## Folder structure

```
03-Pattern-types/
├── README.md
├── 01-Knapsack/README.md
├── 02-Sequence-DP/README.md
├── 03-Partition-DP/README.md
└── 04-Interval-DP/README.md
```

## What is this

Beyond the basic transition shapes, DP problems cluster into four classic *pattern families*. Knapsack DPs choose a subset of items subject to a capacity. Sequence DPs build the answer one element at a time and reference earlier prefixes (longest increasing subsequence, edit distance). Partition DPs split an input into contiguous segments and optimise over partitions. Interval DPs solve a problem on every (i, j) range and combine via a split point k between them.

Each pattern has a signature transition. Knapsack: `f[i][w] = max(f[i-1][w], f[i-1][w-wt[i]] + v[i])`. Sequence: `f[i] = best over j < i of (f[j] + cost(j, i))`. Partition: `f[i] = best over j ≤ i of (f[j-1] + segmentCost(j, i))`. Interval: `f[i][j] = best over k in (i, j) of (f[i][k] + f[k][j] + mergeCost(i, k, j))`.

## Why we use

- Recognising the pattern family tells you the recurrence shape immediately.
- Each family has known complexity bounds and optimisation tricks (rolling arrays, monotonic deque, Knuth optimisation).
- The mental model "what does state[i] mean?" stays consistent across many problems in a family.
- Translating from a problem statement to a DP becomes pattern-matching once you've seen each family.

## How to implement

```text
# Knapsack 0/1
function knap(items, W):
    f = array W+1 of 0
    for (w, v) in items:
        for j in W..w step -1:
            f[j] = max(f[j], f[j-w] + v)
    return f[W]

# Sequence DP (e.g., longest increasing subsequence)
function seqDP(a):
    f = [1]*len(a)
    for i in 1..len(a):
        for j in 0..i-1:
            if a[j] < a[i]: f[i] = max(f[i], f[j] + 1)
    return max(f)

# Partition DP
function partDP(a, isValid):
    f = array len(a)+1 of inf; f[0] = 0
    for i in 1..len(a):
        for j in 1..i:
            if isValid(a[j-1:i]): f[i] = min(f[i], f[j-1] + 1)
    return f[len(a)]

# Interval DP
function intervalDP(a):
    n = len(a); f = matrix n x n
    for length in 2..n:
        for i in 0..n-length:
            j = i + length - 1
            f[i][j] = min over k in i..j-1 of (f[i][k] + f[k+1][j] + cost(i, k, j))
    return f[0][n-1]
```

Subpatterns in this folder:

- `01-Knapsack/` — subset-selection under capacity. 0/1, unbounded, multi-dimensional variants.
- `02-Sequence-DP/` — build answer index-by-index referencing prefix bests (LIS, edit distance).
- `03-Partition-DP/` — split into contiguous chunks each satisfying a predicate.
- `04-Interval-DP/` — range-DP with a split point; matrix-chain, burst balloons.

## Which problems this approach solves in the real world

- Budget allocation across projects with fixed capital (knapsack).
- Resume/CV string matching using edit distance (sequence DP).
- Sentence segmentation in NLP / word-break (partition DP).
- Matrix chain multiplication order for expression evaluation (interval DP).
- Cutting stock optimisation in manufacturing (partition DP).
- Optimal binary search tree construction (interval DP).

## Pros and cons

**Pros**
- Each pattern's recurrence is well-known and quick to apply.
- Knapsack-style problems compress beautifully to 1D rolling arrays.
- Interval DP often yields the only polynomial algorithm for NP-looking problems.
- Patterns are reusable across many domains — pattern recognition pays off.

**Cons**
- Sequence DPs with full pairwise lookback are O(n²); LIS needs patience sorting for O(n log n).
- Partition DPs require an O(1) or O(log) predicate to stay polynomial.
- Interval DPs are O(n³) — bad on long inputs.
- Mixing patterns (knapsack inside interval) compounds state size quickly.

## Limitations

- Knapsack with real-valued weights needs scaling/discretization.
- Partition DPs assume order is fixed; reordering breaks them.
- Interval DPs only work on splittable structures (strings, arrays, expressions), not arbitrary graphs.
- Sequence DPs over very large alphabets benefit from data-structure speedups (Fenwick tree, segment tree).
