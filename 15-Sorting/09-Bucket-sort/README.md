# Bucket sort

## What is this

Bucket sort distributes elements across `k` buckets by a key function, sorts each bucket independently (typically with insertion sort), and concatenates the buckets in order. If the key distribution is roughly uniform across buckets, total time is O(n + k) expected.

It is the algorithm behind the proof that O(n) sorting is possible for uniformly distributed floats in `[0, 1)`, and it's the engine of "maximum gap in linear time".

## Why we use

- Expected O(n) when data is uniformly distributed.
- Trivially parallel — each bucket sorts independently.
- Beats radix sort when keys are floats.
- Works as the inner step of histogramming and percentile estimation.

## How to implement

```
buckets = [[] for _ in range(k)]
for x in a:
    buckets[bucket_of(x)].append(x)
for b in buckets:
    insertion_sort(b)
return concat(buckets)
```

```python
def bucket_sort_floats(a, k=None):
    if not a: return a
    if k is None: k = len(a)
    buckets = [[] for _ in range(k)]
    for x in a:
        idx = min(k - 1, int(x * k))   # x in [0,1)
        buckets[idx].append(x)
    out = []
    for b in buckets:
        b.sort()
        out.extend(b)
    return out
```

```python
def bucket_sort_ints(a, k=10):
    if not a: return a
    lo, hi = min(a), max(a)
    if lo == hi: return a[:]
    rng = (hi - lo) / k + 1
    buckets = [[] for _ in range(k)]
    for x in a:
        buckets[int((x - lo) / rng)].append(x)
    out = []
    for b in buckets:
        b.sort()
        out.extend(b)
    return out
```

Choose `k = n` for the classic linear-expected analysis; small k gives correctness but loses the speedup.

## Which problems this approach solves in the real world

- Sorting floating-point values in [0, 1).
- Percentile estimation via fixed-width histograms.
- "Max gap" between consecutive sorted elements in O(n).
- Image histogram equalization.
- External / parallel sorting where buckets become independent file segments.

## Pros and cons

**Pros**
- Expected O(n + k) under uniform distribution.
- Trivially parallel across buckets.
- Stable if you choose a stable inner sort.

**Cons**
- Worst case degrades to the inner sort's cost when distribution is skewed.
- Choosing `k` is a tunable parameter.
- Extra memory for buckets.

## Limitations

- Non-uniform distributions defeat the expected analysis.
- Streaming variants require online quantile estimation.
- Strings / arbitrary objects need a manual bucket-of function.

## One example

**Problem**: Given an unsorted integer array `nums`, return the maximum difference between two consecutive elements in its sorted form. Must run in O(n) time and space.

**Input**: `nums = [3, 6, 9, 1]`
**Output**: `3`  (sorted: [1, 3, 6, 9]; gaps are 2, 3, 3 → max 3)
**Constraints**: `1 <= n <= 10^5`, `0 <= nums[i] <= 10^9`.

## Solution explanation

```python
def maximumGap(nums):
    if len(nums) < 2: return 0
    lo, hi = min(nums), max(nums)
    if lo == hi: return 0
    n = len(nums)
    bucket_size = max(1, (hi - lo) // (n - 1))
    bucket_count = (hi - lo) // bucket_size + 1
    buckets = [None] * bucket_count
    for x in nums:
        idx = (x - lo) // bucket_size
        if buckets[idx] is None:
            buckets[idx] = [x, x]
        else:
            buckets[idx][0] = min(buckets[idx][0], x)
            buckets[idx][1] = max(buckets[idx][1], x)
    best, prev_hi = 0, lo
    for b in buckets:
        if b is None: continue
        best = max(best, b[0] - prev_hi)
        prev_hi = b[1]
    return best
```

Walkthrough on `[3, 6, 9, 1]`: lo=1, hi=9, n=4, bucket_size = max(1, 8//3) = 2, bucket_count = (9-1)//2 + 1 = 5.

| x | (x - lo) // bs | bucket idx | buckets state                   |
|---|----------------|------------|---------------------------------|
| 3 | 1              | 1          | [_, [3,3], _, _, _]             |
| 6 | 2              | 2          | [_, [3,3], [6,6], _, _]         |
| 9 | 4              | 4          | [_, [3,3], [6,6], _, [9,9]]     |
| 1 | 0              | 0          | [[1,1], [3,3], [6,6], _, [9,9]] |

Walking buckets: gap(1→3)=2, gap(3→6)=3, gap(6→9)=3. Max = 3.

Time: O(n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Sort Array By Parity (LeetCode 905) | https://leetcode.com/problems/sort-array-by-parity/ |
| Medium | Top K Frequent Elements (LeetCode 347) | https://leetcode.com/problems/top-k-frequent-elements/ |
| Hard | Maximum Gap (LeetCode 164) | https://leetcode.com/problems/maximum-gap/ |
