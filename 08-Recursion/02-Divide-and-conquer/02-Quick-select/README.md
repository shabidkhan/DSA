# Quick select

## What is this

Quickselect finds the k-th smallest element of an array in *expected* O(n) without fully sorting. Pick a pivot, partition, then recurse into only the side that contains the k-th rank. Because each step throws away one side, the recurrence is `T(n) = T(n/2) + O(n) = O(n)` on average.

It is the algorithm behind `nth_element` in C++, "find median in O(n)", and many top-k queries. Worst case is O(n^2) without pivot randomization — same defense as quicksort.

## Why we use

- Expected O(n) — strictly better than `sort()`-and-index.
- In-place; O(log n) recursion stack.
- Same partition primitive as quicksort — easy to bolt on.
- Median-of-medians variant gives true O(n) worst case.

## How to implement

```
select(a, lo, hi, k):
    if lo == hi: return a[lo]
    p = partition(a, lo, hi)
    if   k == p: return a[p]
    elif k <  p: return select(a, lo, p - 1, k)
    else:        return select(a, p + 1, hi, k)
```

```python
import random

def quickselect(a, k):     # 0-indexed: k-th smallest
    lo, hi = 0, len(a) - 1
    while True:
        if lo == hi: return a[lo]
        p = _partition(a, lo, hi)
        if k == p:   return a[p]
        elif k < p:  hi = p - 1
        else:        lo = p + 1

def _partition(a, lo, hi):
    r = random.randint(lo, hi)
    a[r], a[hi] = a[hi], a[r]
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i
```

```python
def kth_largest(nums, k):
    return quickselect(nums, len(nums) - k)
```

Always randomize the pivot — adversarial input (already sorted) makes deterministic pivot choice O(n^2).

## Which problems this approach solves in the real world

- Median computation for streaming or batch data.
- Top-k queries in analytics dashboards without full sorting.
- Selection of percentile thresholds for outlier detection.
- Pivoting in approximation algorithms (e.g. k-center heuristics).
- A/B testing: rank-based metrics on large samples.

## Pros and cons

**Pros**
- Expected O(n) — beats sort-and-pick.
- In-place.
- Reuses partition logic from quicksort.

**Cons**
- Worst case O(n^2) without random pivot.
- Destructive — reorders the input.
- Slightly higher constant than heap-based top-k for very small k.

## Limitations

- Worst-case guarantee only with median-of-medians (rarely worth the constant).
- Streaming variant requires reservoir-style sampling.
- Stability not preserved.

## One example

**Problem**: Find the k-th largest element in an unsorted array `nums`.

**Input**: `nums = [3, 2, 1, 5, 6, 4]`, `k = 2`
**Output**: `5`
**Constraints**: `1 <= k <= n <= 10^5`.

## Solution explanation

```python
def findKthLargest(nums, k):
    target = len(nums) - k                  # 0-indexed rank
    lo, hi = 0, len(nums) - 1
    while True:
        p = _partition(nums, lo, hi)
        if   p == target: return nums[p]
        elif p <  target: lo = p + 1
        else:             hi = p - 1
```

Walkthrough on `[3, 2, 1, 5, 6, 4]`, k=2, target=4 (using last as pivot for clarity):

| call             | range | pivot | result of partition       | p | next |
|------------------|-------|-------|---------------------------|---|------|
| partition(0..5)  | full  | 4     | [3,2,1,4,6,5] (4 lands at idx 3) | 3 | p<4 → lo=4 |
| partition(4..5)  | [6,5] | 5     | [3,2,1,4,5,6] (5 lands at 4)     | 4 | p==target return 5 |

Result: 5. Time: O(n) expected, O(n^2) worst. Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find Greatest Common Divisor of Array (LeetCode 1979) | https://leetcode.com/problems/find-greatest-common-divisor-of-array/ |
| Medium | Kth Largest Element in an Array (LeetCode 215) | https://leetcode.com/problems/kth-largest-element-in-an-array/ |
| Hard | Find Median from Data Stream (LeetCode 295) | https://leetcode.com/problems/find-median-from-data-stream/ |
