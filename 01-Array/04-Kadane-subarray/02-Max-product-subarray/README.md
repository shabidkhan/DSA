# Maximum product subarray

## What is this

Maximum product subarray finds the contiguous subarray with the largest product. Unlike maximum *sum* (Kadane), products require tracking *both* the running max and running min — because a negative running min becomes a max when multiplied by another negative.

The DP recurrence at each index considers three candidates: extend the previous max, extend the previous min, or start fresh at `a[i]`. Take max and min across them, then update the global answer.

## Why we use

- Handles mixed signs correctly with O(1) state.
- O(n) time, O(1) space — strictly better than O(n^2) brute force.
- Mirrors Kadane's elegance for a non-additive operation.
- Generalizes to other non-commutative aggregates that can flip sign / magnitude.

## How to implement

```
max_p = min_p = best = a[0]
for i in 1..n-1:
    candidates = (a[i], a[i] * max_p, a[i] * min_p)
    max_p = max(candidates)
    min_p = min(candidates)
    best = max(best, max_p)
```

```python
def max_product(nums):
    max_p = min_p = best = nums[0]
    for x in nums[1:]:
        a, b = x * max_p, x * min_p
        max_p = max(x, a, b)
        min_p = min(x, a, b)
        best = max(best, max_p)
    return best
```

```python
def max_product_with_indices(nums):
    max_p = min_p = best = nums[0]
    s = e = 0
    cur_start = 0
    for i in range(1, len(nums)):
        if nums[i] < 0:
            max_p, min_p = min_p, max_p
        if nums[i] > nums[i] * max_p:
            max_p, cur_start = nums[i], i
        else:
            max_p = nums[i] * max_p
        min_p = min(nums[i], nums[i] * min_p)
        if max_p > best:
            best, s, e = max_p, cur_start, i
    return best, s, e
```

Zeros reset both `max_p` and `min_p` because any product containing 0 is 0.

## Which problems this approach solves in the real world

- Computing cumulative return of the best contiguous trading window.
- Finding the highest-yield contiguous segment in signal data with mixed signs.
- Identifying the contiguous slice with strongest correlation product in time series.
- Maximizing product of contiguous gain factors in a chain of multipliers.
- Detecting the best run in a streaming gain/loss sequence.

## Pros and cons

**Pros**
- O(n) time, O(1) memory.
- Correct for negatives, positives, and zeros.
- Compact code, easy to audit.

**Cons**
- Doesn't generalize to non-contiguous subsequences.
- Overflow risk on languages with fixed-width ints — Python handles big ints natively.
- Less intuitive than Kadane's — easy to forget the negative-product flip.

## Limitations

- Cannot handle "subarray with at most k zeros" without DP extension.
- Streaming variant needs the same O(1) state but no easy way to recover indices.
- Floating-point introduces rounding drift.

## One example

**Problem**: Given an integer array `nums`, return the maximum product of any contiguous (non-empty) subarray.

**Input**: `nums = [2, 3, -2, 4]`
**Output**: `6`
**Constraints**: `1 <= n <= 2 * 10^4`, `-10 <= nums[i] <= 10`.

## Solution explanation

```python
def maxProduct(nums):
    max_p = min_p = best = nums[0]
    for x in nums[1:]:
        a, b = x * max_p, x * min_p
        max_p = max(x, a, b)
        min_p = min(x, a, b)
        best = max(best, max_p)
    return best
```

Walkthrough on `[2, 3, -2, 4]`:

| i | x  | candidates (x, x*max_p, x*min_p) | max_p | min_p | best |
|---|----|----------------------------------|-------|-------|------|
| 0 | 2  | init                             | 2     | 2     | 2    |
| 1 | 3  | (3, 6, 6)                        | 6     | 3     | 6    |
| 2 | -2 | (-2, -12, -6)                    | -2    | -12   | 6    |
| 3 | 4  | (4, -8, -48)                     | 4     | -48   | 6    |

Result: 6. Time: O(n). Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Maximum Subarray (LeetCode 53) | https://leetcode.com/problems/maximum-subarray/ |
| Medium | Maximum Product Subarray (LeetCode 152) | https://leetcode.com/problems/maximum-product-subarray/ |
| Hard | Maximum Sum of 3 Non-Overlapping Subarrays (LeetCode 689) | https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/ |
