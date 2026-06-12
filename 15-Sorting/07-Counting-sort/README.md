# Counting sort

## What is this

Counting sort is a non-comparison sort for integers in a known small range `[lo..hi]`. Build a counts array of size `hi - lo + 1`, increment `counts[x - lo]` for each input `x`, then write back each value `c.count` times in order. Time and space are both O(n + k) where k is the range size.

It dominates comparison sorts when k is comparable to or smaller than n. Its stable variant uses a prefix sum over the counts and is the building block of radix sort.

## Why we use

- O(n + k) — linear when range is small.
- Stable in its prefix-sum form.
- Beats all O(n log n) comparison sorts when applicable.
- Foundation for radix sort.

## How to implement

```
counts = [0] * (hi - lo + 1)
for x in a: counts[x - lo] += 1
out = []
for v, c in enumerate(counts):
    out.extend([v + lo] * c)
```

```python
def counting_sort(a, lo=None, hi=None):
    if lo is None: lo = min(a)
    if hi is None: hi = max(a)
    counts = [0] * (hi - lo + 1)
    for x in a:
        counts[x - lo] += 1
    out = []
    for v, c in enumerate(counts):
        out.extend([v + lo] * c)
    return out
```

```python
def counting_sort_stable(a, key, k):
    counts = [0] * (k + 1)
    for x in a:
        counts[key(x)] += 1
    for i in range(1, k + 1):
        counts[i] += counts[i - 1]
    out = [0] * len(a)
    for x in reversed(a):
        counts[key(x)] -= 1
        out[counts[key(x)]] = x
    return out
```

Stability comes from iterating the input in reverse during the placement step and using the prefix sums as write positions.

## Which problems this approach solves in the real world

- Sorting age, score, or pixel-intensity arrays (small range).
- Counting / histogram queries.
- Building a sorted index of fixed-vocabulary categorical data.
- Building block of radix sort for integer / string keys.
- Bucketing telemetry events by an integer category.

## Pros and cons

**Pros**
- Linear time when range is small.
- Stable with prefix sums.
- Trivial constant factor.

**Cons**
- Memory proportional to the value range, not n.
- Useless if range >> n.
- Only works on integer-keyed data.

## Limitations

- Range must be known and bounded (no streaming with unbounded ints).
- Floats / strings need an explicit key-to-int mapping.
- Negative values require offsetting by `-lo`.

## One example

**Problem**: Given an integer array `nums` where every element is in `[0, 100]`, sort it in non-decreasing order.

**Input**: `nums = [4, 2, 2, 8, 3, 3, 1]`
**Output**: `[1, 2, 2, 3, 3, 4, 8]`
**Constraints**: `1 <= n <= 10^5`, `0 <= nums[i] <= 100`.

## Solution explanation

```python
def sortArray(nums):
    k = max(nums) + 1
    counts = [0] * k
    for x in nums:
        counts[x] += 1
    out = []
    for v, c in enumerate(counts):
        out.extend([v] * c)
    return out
```

Walkthrough on `[4, 2, 2, 8, 3, 3, 1]`:

| step    | counts (indices 0..8)               |
|---------|--------------------------------------|
| init    | [0, 0, 0, 0, 0, 0, 0, 0, 0]          |
| after counting | [0, 1, 2, 2, 1, 0, 0, 0, 1]   |

Emitting `[1*1, 2*2, 3*2, 4*1, 5..7 nothing, 8*1]` gives `[1, 2, 2, 3, 3, 4, 8]`.

Time: O(n + k). Space: O(k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Height Checker (LeetCode 1051) | https://leetcode.com/problems/height-checker/ |
| Medium | Sort Colors (LeetCode 75) | https://leetcode.com/problems/sort-colors/ |
| Hard | Maximum Gap (LeetCode 164) | https://leetcode.com/problems/maximum-gap/ |
