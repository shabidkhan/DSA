# Sorting Patterns

## Folder structure

```
15-Sorting/
├── README.md
├── 01-Bubble-sort/README.md
├── 02-Selection-sort/README.md
├── 03-Insertion-sort/README.md
├── 04-Merge-sort/README.md
├── 05-Quick-sort/README.md
├── 06-Heap-sort/README.md
├── 07-Counting-sort/README.md
├── 08-Radix-sort/README.md
└── 09-Bucket-sort/README.md
```

## What is this

Sorting rearranges a sequence into a specific order — and it's both an algorithm family in its own right and a primitive step that unlocks countless other algorithms (binary search, sweep-line, two pointers, greedy, hash-based bucketing). The nine classical sorts fall into three buckets: **simple comparison-based** (Bubble, Selection, Insertion — O(n²), instructive), **efficient comparison-based** (Merge, Quick, Heap — O(n log n)), and **non-comparison** (Counting, Radix, Bucket — O(n) under specific assumptions on input).

Knowing the trade-offs (stable vs unstable, in-place vs auxiliary memory, worst vs average case, adversarial inputs) is more important than memorising every implementation — modern languages give you `sorted()` or `Arrays.sort()`, but knowing which underlying algorithm is at work explains performance and stability surprises.

## Why we use

- Sorting is a prerequisite for binary search, two pointers, sweep-line, and many greedy algorithms.
- The choice of algorithm dramatically affects performance on real data shapes (already-sorted, reverse, many duplicates).
- Stability matters when sorting by secondary keys (sort by date, then by id).
- Non-comparison sorts hit O(n) when assumptions hold — huge for fixed-domain data.

## How to implement

Pick by data shape and constraints:

```
small n or nearly-sorted   — insertion sort
needs stable + worst-case  — merge sort
average-case fastest       — quick sort (with median-of-three pivoting)
in-place + worst-case      — heap sort
small integer domain       — counting sort
multi-digit integers       — radix sort
uniformly distributed real — bucket sort
```

Subpatterns in this folder:

- **01-Bubble-sort** — repeated swaps; O(n²), stable.
- **02-Selection-sort** — pick min each pass; O(n²), unstable.
- **03-Insertion-sort** — shift into place; O(n²), stable, fast on small or nearly-sorted data.
- **04-Merge-sort** — divide and conquer; O(n log n) worst, stable, O(n) extra.
- **05-Quick-sort** — partition-based; O(n log n) average, in-place but unstable.
- **06-Heap-sort** — repeated max extraction; O(n log n) worst, in-place, unstable.
- **07-Counting-sort** — frequency-array fill; O(n + k), stable, integer domain only.
- **08-Radix-sort** — digit-by-digit counting sort; O(d × (n + k)).
- **09-Bucket-sort** — distribute into buckets, sort each; O(n) expected when uniform.

## Which problems this approach solves in the real world

- Database `ORDER BY` clauses (typically merge/quick variants).
- File system listings (`ls`, Finder).
- TimSort (Python, Java) is a hybrid of merge and insertion sort.
- Distributed shuffle stages in MapReduce / Spark.
- Pre-sort step for sweep-line algorithms in computational geometry.
- Indexing/external sort for data that doesn't fit in memory.

## Pros and cons

**Pros**
- Unlocks downstream algorithms (binary search, two pointers, etc.).
- O(n log n) worst-case is achievable (merge, heap).
- Non-comparison sorts hit O(n) under integer-domain assumptions.
- Modern hybrids (TimSort, IntroSort) combine the strengths automatically.

**Cons**
- O(n log n) is provably the lower bound for comparison sorts.
- Quick sort's worst case is O(n²) — adversarial inputs are real.
- Stability vs in-place is usually a trade-off.
- Non-comparison sorts have very specific input assumptions.

## Limitations

- Pure comparison sorts can't beat n log n.
- Counting/radix/bucket sorts need bounded or well-distributed inputs.
- External sort is needed when data exceeds memory.
- Custom comparators must satisfy strict weak ordering or behaviour is undefined.
