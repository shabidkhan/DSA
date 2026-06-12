# Longest Increasing Subsequence (LIS)

## What is this

The Longest Increasing Subsequence problem asks for the length (and optionally the content) of the longest subsequence of a given array whose elements are in strictly increasing order. A subsequence preserves the original order but does not need to be contiguous.

The classical DP solution runs in O(n^2) using `dp[i]` = LIS ending at index `i`. A faster O(n log n) approach maintains a `tails` array via binary search, where `tails[k]` is the smallest possible tail value of any increasing subsequence of length `k + 1` seen so far.

## Why we use

- Quantifies "how monotonic-ish" a sequence is
- O(n log n) variant scales to large inputs
- Fundamental building block for patience sorting, box stacking, and version-tracking algorithms
- LIS-style reasoning unlocks many seemingly unrelated DP problems

## How to implement

```
O(n^2) DP:
  dp[i] = 1
  for j in 0..i-1:
      if a[j] < a[i]:
          dp[i] = max(dp[i], dp[j] + 1)
  return max(dp)

O(n log n) patience method:
  tails = []
  for x in a:
      pos = bisect_left(tails, x)        # strict increase
      if pos == len(tails):
          tails.append(x)
      else:
          tails[pos] = x
  return len(tails)
```

O(n^2) DP returning the length:

```python
def lis_length_n2(a: list[int]) -> int:
    if not a:
        return 0
    dp = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

O(n log n) using `bisect_left` for the strictly increasing variant:

```python
from bisect import bisect_left

def lis_length_nlogn(a: list[int]) -> int:
    tails: list[int] = []
    for x in a:
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)
```

Invariant for the O(n log n) version: `tails[k]` is the smallest tail value among all increasing subsequences of length `k + 1` discovered so far. Replacing `tails[pos]` never increases the size but can lower a tail, opening room for future extensions.

## Which problems this approach solves in the real world

- Stock analysis: longest run of weeks with strictly increasing close prices
- Aircraft / box stacking: longest stack where each next box strictly dominates the previous
- Version comparison: longest sequence of compatible upgrades respecting order
- Russian-doll envelopes / nested objects with strict dimension increase
- Patience sort and online ranking estimators

## Pros and cons

**Pros**
- O(n log n) is fast enough for n up to 10^5-10^6
- Tail array doubles as a tool to reconstruct one valid LIS
- Simple to extend to non-decreasing (use `bisect_right`) or 2D variants

**Cons**
- Reconstructing an actual LIS requires extra parent pointers
- `tails` array values do not themselves form an LIS — only their length is meaningful
- O(n^2) DP becomes slow above n ~ 10^4

## Limitations

- LIS-only counts longest length; "count of LIS" needs auxiliary arrays
- Strict vs non-strict variants are easy to confuse — read the constraint carefully
- Multidimensional LIS (e.g. boxes) requires sorting + 1D LIS on a derived dimension

## One example

Problem: Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

```
Input:  nums = [10, 9, 2, 5, 3, 7, 101, 18]
Output: 4   (one LIS is [2, 3, 7, 18])
Constraints: 1 <= len(nums) <= 2500, -10^4 <= nums[i] <= 10^4
```

## Solution explanation

```python
from bisect import bisect_left

def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []
    for x in nums:
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)
```

For each new element, find the leftmost tail that is at least as large and replace it. If no such tail exists, append. The length of `tails` is the LIS length.

Walkthrough for `nums = [10, 9, 2, 5, 3, 7, 101, 18]`:

| x   | tails before        | action                              | tails after         |
|-----|---------------------|-------------------------------------|---------------------|
| 10  | []                  | append                              | [10]                |
| 9   | [10]                | replace position 0                  | [9]                 |
| 2   | [9]                 | replace position 0                  | [2]                 |
| 5   | [2]                 | append                              | [2, 5]              |
| 3   | [2, 5]              | replace position 1                  | [2, 3]              |
| 7   | [2, 3]              | append                              | [2, 3, 7]           |
| 101 | [2, 3, 7]           | append                              | [2, 3, 7, 101]      |
| 18  | [2, 3, 7, 101]      | replace position 3                  | [2, 3, 7, 18]       |

Final length = 4. Time O(n log n), space O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Longest Continuous Increasing Subsequence | https://leetcode.com/problems/longest-continuous-increasing-subsequence/ |
| Medium | Longest Increasing Subsequence | https://leetcode.com/problems/longest-increasing-subsequence/ |
| Hard | Russian Doll Envelopes | https://leetcode.com/problems/russian-doll-envelopes/ |
