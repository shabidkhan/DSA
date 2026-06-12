# Merge-sort pattern (divide and conquer)

## What is this

The merge-sort *pattern* generalizes the merge-sort algorithm into a recipe: split a problem into two halves, recursively solve each half, then *combine* the results in linear time. Many problems beyond plain sorting fit this shape — counting inversions, finding the closest pair of points in 1D, computing the maximum-sum subarray crossing the middle, and parallel reductions.

Recursion gives O(log n) depth; the per-level linear combine yields the classic O(n log n) time bound.

## Why we use

- O(n log n) for problems whose only combine step is linear.
- Trivially parallel: two halves are independent until the merge.
- Stable: equal elements preserve order across the merge.
- Generic skeleton that adapts to many "count / aggregate" problems.

## How to implement

```
solve(a, lo, hi):
    if hi - lo <= 1: return base
    mid = (lo + hi) // 2
    left  = solve(a, lo, mid)
    right = solve(a, mid, hi)
    return combine(left, right, a, lo, mid, hi)
```

```python
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    L = merge_sort(a[:mid])
    R = merge_sort(a[mid:])
    return _merge(L, R)

def _merge(L, R):
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    out.extend(L[i:]); out.extend(R[j:])
    return out
```

```python
def max_crossing_sum(a, lo, mid, hi):
    left_max = right_max = -10**18
    s = 0
    for i in range(mid - 1, lo - 1, -1):
        s += a[i]; left_max = max(left_max, s)
    s = 0
    for i in range(mid, hi):
        s += a[i]; right_max = max(right_max, s)
    return left_max + right_max

def max_subarray_dc(a, lo=0, hi=None):
    if hi is None: hi = len(a)
    if hi - lo == 1: return a[lo]
    mid = (lo + hi) // 2
    return max(max_subarray_dc(a, lo, mid),
               max_subarray_dc(a, mid, hi),
               max_crossing_sum(a, lo, mid, hi))
```

The combine step is where the pattern earns its time bound — keep it strictly O(n) per level.

## Which problems this approach solves in the real world

- External sort: merge-sort flow on disk-resident data.
- Inversion-count metrics (Kendall tau, ranking similarity).
- Closest-pair-of-points pre-sort + merge.
- Parallel reductions in functional / data-parallel frameworks.
- Top-k merging across distributed shards.

## Pros and cons

**Pros**
- Tight O(n log n) bound whenever the combine is O(n).
- Naturally parallelizes by recursive split.
- Stable; preserves input order on equality.

**Cons**
- O(n) extra memory for the merge buffer.
- Combine cost > O(n) destroys the bound (use D&C with combine analysis).
- Recursive split overhead on tiny arrays — fall back to insertion sort below ~16.

## Limitations

- Not in-place in the simple form.
- Combine must be associative-like (left/right results must merge cleanly).
- Recursion depth O(log n) — usually fine, but explicit stack helps on small VM stacks.

## One example

**Problem**: Given an integer array `nums`, find the contiguous subarray with the largest sum and return its sum.

**Input**: `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`
**Output**: `6`
**Constraints**: `1 <= n <= 10^5`, `-10^4 <= nums[i] <= 10^4`.

## Solution explanation

```python
def maxSubArray(nums):
    def solve(lo, hi):
        if hi - lo == 1: return nums[lo]
        mid = (lo + hi) // 2
        return max(solve(lo, mid),
                   solve(mid, hi),
                   crossing(lo, mid, hi))
    def crossing(lo, mid, hi):
        left_max = right_max = float('-inf')
        s = 0
        for i in range(mid - 1, lo - 1, -1):
            s += nums[i]; left_max = max(left_max, s)
        s = 0
        for i in range(mid, hi):
            s += nums[i]; right_max = max(right_max, s)
        return left_max + right_max
    return solve(0, len(nums))
```

Walkthrough on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`:

| call          | range           | left | right | crossing | return |
|---------------|-----------------|------|-------|----------|--------|
| solve(0,9)    | full            | ?    | ?     | ?        |        |
| solve(0,4)    | [-2,1,-3,4]     | 1    | 4     | 1+4=5    | 5      |
| solve(4,9)    | [-1,2,1,-5,4]   | 3    | 4     | 3+3=6    | 6      |
| crossing(0,4,9) | best left from 4→0 = 4, best right from 4→9 = 2 (then drops) | 4+2=6 |
| solve(0,9)    |                 | 5    | 6     | 6        | **6**  |

Time: O(n log n). Space: O(log n) stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Maximum Subarray (LeetCode 53) | https://leetcode.com/problems/maximum-subarray/ |
| Medium | Sort List (LeetCode 148) | https://leetcode.com/problems/sort-list/ |
| Hard | Reverse Pairs (LeetCode 493) | https://leetcode.com/problems/reverse-pairs/ |
