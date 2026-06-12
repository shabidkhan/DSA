# Binary Search Patterns

## Folder structure

```
05-Binary-search/
├── README.md
├── 01-On-index/README.md
└── 02-On-answer/README.md
```

## What is this

Binary search is the O(log n) algorithm for finding an element (or a boundary) in a sorted sequence by repeatedly halving the search range. The classical use is "find x in a sorted array", but the more powerful use is **binary search on the answer**: when the problem has a monotone predicate P(k) — "is k a feasible answer?" — you can binary-search the smallest (or largest) k for which P(k) holds, even if the array itself isn't sorted.

The two subpatterns here are: **on index** (the data is sorted; search for a value, the first/last occurrence, or a boundary) and **on answer** (the search space is the range of possible answers; you binary-search a monotone predicate over that range). The latter unlocks problems like "minimum capacity to ship within D days", "split array largest sum", and "Koko eating bananas".

## Why we use

- O(log n) instead of O(n) — for million-element arrays, that's 20 comparisons instead of 1,000,000.
- "Binary search on answer" extends the technique far beyond sorted arrays.
- Memory cost is O(1) — just two integer bounds.
- The template is short and easy to memorise correctly once.

## How to implement

```
classic (find x):
    l, r = 0, n - 1
    while l <= r:
        m = (l + r) // 2
        if a[m] == x: return m
        elif a[m] < x: l = m + 1
        else: r = m - 1
    return -1

first true (lower bound on monotone predicate):
    l, r = 0, n              # half-open
    while l < r:
        m = (l + r) // 2
        if P(m): r = m
        else: l = m + 1
    return l                  # smallest m with P(m), or n if none

on answer:
    l, r = min_possible, max_possible
    while l < r:
        m = (l + r) // 2
        if feasible(m): r = m
        else: l = m + 1
    return l
```

Subpatterns in this folder:

- **01-On-index** — classic search in a sorted array (value, first, last occurrence).
- **02-On-answer** — binary search the smallest / largest feasible answer using a monotone predicate.

## Which problems this approach solves in the real world

- Database B-tree lookups.
- Version-control bisect (find the first bad commit).
- Page lookup in sorted logs.
- Minimum capacity / latency / bandwidth that satisfies SLA.
- Resource sizing under a monotone-feasibility constraint.
- Numerical root-finding (bisection method on continuous monotone functions).

## Pros and cons

**Pros**
- O(log n) is unbeatable on sorted data.
- O(1) extra space.
- Generalises far beyond literal sorted arrays via "on answer".
- Iterative template avoids stack overflow.

**Cons**
- Off-by-one bugs and infinite-loop bugs are common — pick one template and stick to it.
- Mid calculation with `(l + r) // 2` can overflow in some languages — use `l + (r - l) // 2`.
- "On answer" requires proving monotonicity — non-trivial mistake source.
- Floating-point binary search needs explicit precision control.

## Limitations

- Sorted input is required for "on index"; sorting cost may dominate.
- Predicate must be monotone for "on answer".
- For unsorted data without monotone predicate, hash maps or scans win.
- Adversarial inputs with many duplicates can require careful first/last variants.
