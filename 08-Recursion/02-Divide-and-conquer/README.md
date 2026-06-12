# Divide and Conquer

## Folder structure

```
02-Divide-and-conquer/
├── README.md
├── 01-Merge-sort-pattern/README.md
├── 02-Quick-select/README.md
└── 03-Count-inversions/README.md
```

## What is this

Divide and conquer solves a problem by splitting it into two or more roughly independent subproblems, solving each recursively, and combining the answers. Unlike backtracking — which enumerates possibilities — divide and conquer reduces *size* on each recursion and stitches answers back together. The work happens in two phases: the recursive descent (split) and the postorder combine (conquer).

Three sub-patterns capture most cases. Merge-sort partitions arbitrarily and combines via merging — good when both halves contribute equally. Quick-select partitions around a pivot and recurses into only one side — good when you can prune half the search per step. Inversion counting embeds an extra accumulation into the merge step — a common pattern for "count pairs satisfying P."

## Why we use

- Reduces problem size by a constant factor per recursion, giving log-linear or better complexity.
- The recurrence-relation framing (T(n) = a·T(n/b) + f(n)) makes complexity analysis mechanical.
- Splits are independent, so divide-and-conquer parallelises naturally.
- Many problems hide a combine-step where extra work (counting, merging, max) becomes free during the merge.

## How to implement

```text
function solve(input):
    if base case: return trivial answer
    parts = split(input)
    sub  = [solve(p) for p in parts]
    return combine(sub)
```

Skeletons per subpattern:

- Merge sort: split in half, sort each, merge. Combine = O(n) two-pointer merge.
- Quick select: pick a pivot, partition, recurse into the side containing index k.
- Count inversions: merge sort variant where the merge step counts cross-pair inversions in O(n).

Subpatterns in this folder:

- `01-Merge-sort-pattern/` — split-by-half + merge; basis for sorts and inversion counts.
- `02-Quick-select/` — partition + recurse one side; expected O(n) for k-th smallest.
- `03-Count-inversions/` — merge-sort with a counter that adds to the answer at each merge.

## Which problems this approach solves in the real world

- Sorting huge datasets in stable, predictable O(n log n) time (external merge sort on disk).
- Finding the median of a stream batch without fully sorting it (quick select).
- Counting "out of order" pairs in collaborative-filtering rank lists (inversion count).
- Closest-pair-of-points in computational geometry.
- Matrix multiplication via Strassen-style recursion.
- Parallel batch processing where independent halves can be scheduled on different cores.

## Pros and cons

**Pros**
- Often achieves O(n log n) on problems where naive solutions are O(n²).
- Embarrassingly parallel — sibling subproblems are independent.
- Combine step is often the cleanest place to accumulate extra answers (inversions, max-subarray).
- Works on linked structures and arrays alike.

**Cons**
- Recursion depth = log n; balanced splits matter. Bad pivots degrade quick-select to O(n²).
- Combine step can dominate (e.g., O(n) merge of two halves) — must amortise correctly.
- Auxiliary memory for splits/merges can become a hot path (cache, allocations).
- Reasoning about the recurrence requires the Master Theorem or similar discipline.

## Limitations

- Requires problem to decompose cleanly — overlapping subproblems should go to DP instead.
- For very small n, the recursion overhead can beat the gains; usually switched to insertion sort under a threshold.
- Quick-select's worst case is bad without median-of-medians or randomization.
- In-place variants (in-place merge sort) are dramatically more complex than the textbook split-and-merge.
