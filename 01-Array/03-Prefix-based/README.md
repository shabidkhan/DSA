# Prefix-based Patterns

## Folder structure

```
03-Prefix-based/
├── README.md
├── 01-Prefix-sum/README.md
├── 02-Prefix-XOR/README.md
└── 03-2D-prefix/README.md
```

## What is this

Prefix-based techniques precompute a cumulative array `P` such that `P[i]` aggregates the first `i` elements under some associative operation (sum, XOR, min via persistent structure). Once built, the aggregate of any subarray `a[l..r]` collapses to a single combination of two prefix values — `P[r+1] - P[l]` for sums, `P[r+1] ^ P[l]` for XOR — answering range queries in O(1) after an O(n) preprocessing pass.

The three subpatterns here are **prefix sum** (the canonical version for additive queries), **prefix XOR** (for parity, target-XOR counting, and subarray-XOR queries), and **2D prefix** (inclusion-exclusion to query rectangular regions in a matrix in O(1)). Combined with a hashmap, prefix arrays answer "how many subarrays have aggregate K?" in O(n).

## Why we use

- O(1) range queries after O(n) preprocessing — turning many O(n²) algorithms into O(n).
- Memory cost is just one extra array.
- Combines beautifully with hash maps for counting-subarray-with-property problems.
- 2D variant gives O(1) rectangle queries in matrices.

## How to implement

```
prefix sum:
    P[0] = 0
    for i in 0..n-1: P[i+1] = P[i] + a[i]
    range_sum(l, r) = P[r+1] - P[l]

prefix XOR:
    P[0] = 0
    for i in 0..n-1: P[i+1] = P[i] ^ a[i]
    range_xor(l, r) = P[r+1] ^ P[l]

2D prefix sum:
    P[i+1][j+1] = a[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]
    rect(r1,c1,r2,c2) = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]
```

Subpatterns in this folder:

- **01-Prefix-sum** — 1D additive prefix; the canonical version.
- **02-Prefix-XOR** — parity / XOR aggregates; pairs with hashmap for subarray-XOR counts.
- **03-2D-prefix** — inclusion-exclusion in 2D for O(1) rectangle queries.

## Which problems this approach solves in the real world

- Range-sum analytics in dashboards (pageviews this week).
- Image processing (integral image for box filters in O(1) per pixel).
- Heatmap region queries in GIS.
- Subarray-count-with-property in trading and monitoring.
- Cumulative gain / loss tracking in finance.
- Game-board score aggregation.

## Pros and cons

**Pros**
- O(1) range queries after O(n) preprocessing — huge for many-query workloads.
- Tiny memory overhead.
- Pairs with hashmaps for subarray-counting problems.
- 2D extension is mechanical and powerful.

**Cons**
- Only works for static arrays — any update invalidates the prefix.
- Easy to off-by-one (`P[r+1] - P[l]` vs `P[r] - P[l-1]`).
- 2D inclusion-exclusion is one of the most-bug-prone DP-adjacent patterns.
- For dynamic arrays, use Fenwick trees instead.

## Limitations

- Mutations require O(n) rebuild; switch to Fenwick or segment tree.
- Non-invertible operations (min, max) can't use prefix difference — need sparse tables or segment trees.
- 3D and beyond is rarely worth the complexity.
- Floating-point cumulative sums accumulate rounding errors over large n.
