# Array Patterns

## Folder structure

```
01-Array/
├── README.md
├── 01-Two-pointer/
│   ├── README.md
│   ├── 01-Opposite-ends/README.md
│   ├── 02-Same-direction/README.md
│   ├── 03-Fast-slow/README.md
│   └── 04-Partition/README.md
├── 02-Sliding-window/
│   ├── README.md
│   ├── 01-Fixed-size/README.md
│   └── 02-Variable-size/
│       ├── README.md
│       ├── 01-Expand-shrink/README.md
│       └── 02-Monotonic-window/README.md
├── 03-Prefix-based/
│   ├── README.md
│   ├── 01-Prefix-sum/README.md
│   ├── 02-Prefix-XOR/README.md
│   └── 03-2D-prefix/README.md
├── 04-Kadane-subarray/
│   ├── README.md
│   ├── 01-Kadane/README.md
│   ├── 02-Max-product-subarray/README.md
│   └── 03-Subarray-with-XOR/README.md
└── 05-Binary-search/
    ├── README.md
    ├── 01-On-index/README.md
    └── 02-On-answer/README.md
```

## What is this

Arrays are the foundational sequential data structure, and most array problems collapse into a handful of repeating shapes: walking from two ends inward, maintaining a window of consecutive elements, using cumulative computations to answer range queries in O(1), tracking running extremes for max-subarray problems, and binary-searching either on indices or on the answer itself. Together these five families cover the overwhelming majority of array problems.

The array family is where you first learn the "linear scan" mindset and where you start replacing nested loops with smarter single-pass algorithms. Mastering the array family makes string, linked-list, and many DP problems feel familiar — they all reuse these same skeletons.

## Why we use

- Arrays are the most common input shape; you'll encounter them in 60%+ of problems.
- Patterns here generalise: sliding window works on strings, two pointers work on linked lists, prefix sums work on 2D grids.
- The O(n) ceiling is usually achievable once you recognise the right pattern.
- These templates are short, memorable, and battle-tested.

## How to implement

Pick the subpattern that fits your problem shape:

```
two pointers       — opposite ends or same direction; sorted / partition / pair-finding
sliding window     — contiguous subarray with a constraint (sum, distinct count, max)
prefix-based       — many range queries, sum / xor / 2D prefix
Kadane / subarray  — running maximum / minimum, max-subarray / max-product
binary search      — sorted input OR monotone predicate on the answer
```

Subpatterns in this folder:

- **01-Two-pointer** — opposite ends, same direction, fast-slow, partition (Dutch flag).
- **02-Sliding-window** — fixed-size and variable-size (expand-shrink, monotonic).
- **03-Prefix-based** — prefix sum, prefix XOR, 2D prefix.
- **04-Kadane-subarray** — max subarray, max product, subarray with XOR/sum.
- **05-Binary-search** — on index (sorted data) and on answer (monotone predicate).

## Which problems this approach solves in the real world

- Order-book depth checks and price-window aggregates in trading systems.
- Time-window rate limiters in API gateways.
- Range-sum analytics in dashboards (page views over the last 24h).
- Anomaly detection over rolling windows in monitoring.
- Frame-buffer scanline operations in graphics pipelines.
- Sorted-log binary search in systems like Elasticsearch and Kafka.

## Pros and cons

**Pros**
- O(n) or O(n log n) ceilings make these patterns efficient at scale.
- Constant-extra-space solutions are common.
- Cache-friendly: sequential access patterns are fast on real hardware.
- Code templates are small and easy to memorise.

**Cons**
- Subtle off-by-one and boundary errors are the most common bug class.
- Choosing the right pattern (two pointer vs sliding window vs binary search) requires practice.
- 2D variants explode in complexity — be careful with prefix grids and matrix searches.
- Modifying the array in place may conflict with caller expectations.

## Limitations

- Arrays assume contiguous, indexable storage; linked structures need different patterns.
- Many patterns require sorted input — sorting cost may dominate.
- Binary search on answer needs a provable monotone predicate, which can be subtle.
- Streaming or infinite arrays need specialised online algorithms.
