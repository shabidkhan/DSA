# Partition DP

## What is this

Partition DP splits a sequence into contiguous parts and optimizes over the split points. The state is `dp[i][k] = best answer using first i elements split into k parts`, with transition `dp[i][k] = best over j: combine(dp[j][k-1], cost(j+1, i))`. Complexity O(n^2 * k) in the textbook form; many variants admit O(n*k) or O(n log n) with optimizations.

Examples: split array into K subarrays minimizing max sum, palindrome partitioning min cuts, allocate minimum number of pages to students, painters partition problem.

## Why we use

- Cleanly captures "split into k parts" objectives.
- General O(n^2 * k) is usually fine for small k.
- Binary-search-on-answer often simplifies the "min largest part" variant to O(n log range).
- Foundation for many "schedule jobs across k machines" problems.

## How to implement (DP for "split into k parts, minimize max sum")

```
dp[i][k] = best answer using prefix [0..i-1] split into k parts
dp[i][0] = INF for i > 0; dp[0][0] = 0
for i in 1..n:
    for k in 1..K:
        dp[i][k] = min over j in 0..i-1:
                   max(dp[j][k-1], sum(j..i-1))
```

```python
def split_min_max_sum_dp(nums, k):
    n = len(nums)
    pref = [0] * (n + 1)
    for i, x in enumerate(nums):
        pref[i + 1] = pref[i] + x
    INF = float('inf')
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for kk in range(1, k + 1):
            for j in range(i):
                seg_sum = pref[i] - pref[j]
                dp[i][kk] = min(dp[i][kk], max(dp[j][kk - 1], seg_sum))
    return dp[n][k]
```

```python
def split_min_max_sum_bs(nums, k):
    def can_split(limit):
        parts, cur = 1, 0
        for x in nums:
            if x > limit: return False
            if cur + x > limit:
                parts += 1; cur = x
            else:
                cur += x
        return parts <= k
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_split(mid): hi = mid
        else:               lo = mid + 1
    return lo
```

The DP gives the exact optimum directly; binary-search-on-answer is faster (O(n log sum)) for the specific "min largest sum" variant.

## Which problems this approach solves in the real world

- Splitting jobs across k workers to minimize max load (load balancing).
- Cutting a board into k pieces minimizing the longest piece's wastage.
- Minimum-cuts palindrome partitioning for compression preprocessing.
- Allocating documents to readers to minimize max reading load.
- Distributing tasks across stages of a pipeline.

## Pros and cons

**Pros**
- DP form is general and easy to derive.
- Binary-search variant runs in O(n log range) for monotone predicates.
- State design (i, k) is natural for partition objectives.

**Cons**
- O(n^2 * k) DP is heavy for large n.
- Memory O(n * k); rolling array trick helps but adds complexity.
- Reconstructing the splits needs backpointers.

## Limitations

- Non-contiguous partitions need different state shape.
- Streaming variants require window-based heuristics.
- Multi-criterion objectives (e.g. min max + min variance) need Pareto-style DP.

## One example

**Problem**: Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty contiguous subarrays. Minimize the largest sum among the splits and return it.

**Input**: `nums = [7, 2, 5, 10, 8]`, `k = 2`
**Output**: `18`  (split as [7, 2, 5] and [10, 8])
**Constraints**: `1 <= n <= 1000`, `1 <= k <= min(50, n)`.

## Solution explanation

```python
def splitArray(nums, k):
    def can_split(limit):
        parts, cur = 1, 0
        for x in nums:
            if x > limit: return False
            if cur + x > limit:
                parts += 1; cur = x
            else:
                cur += x
        return parts <= k

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_split(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Walkthrough on `nums = [7, 2, 5, 10, 8]`, k=2:

| lo | hi | mid | can_split(mid)? | new range |
|----|----|-----|------------------|-----------|
| 10 | 32 | 21  | parts=2 (7+2+5=14, 10+8=18) → True | (10, 21) |
| 10 | 21 | 15  | parts=3 (7+2+5=14, 10, 8) → False  | (16, 21) |
| 16 | 21 | 18  | parts=2 (7+2+5=14, 10+8=18) → True | (16, 18) |
| 16 | 18 | 17  | parts=3 (7+2=9, 5+10=15, 8) → False| (18, 18) |
| 18 | 18 | exit |                                 | return 18 |

Return 18. Time: O(n log sum). Space: O(1).

DP variant: O(n^2 * k) time, O(n * k) space.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Maximum Subarray (LeetCode 53) | https://leetcode.com/problems/maximum-subarray/ |
| Medium | Palindrome Partitioning II (LeetCode 132) | https://leetcode.com/problems/palindrome-partitioning-ii/ |
| Hard | Split Array Largest Sum (LeetCode 410) | https://leetcode.com/problems/split-array-largest-sum/ |
