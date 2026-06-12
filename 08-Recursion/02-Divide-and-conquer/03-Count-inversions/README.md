# Count inversions

## What is this

An inversion in array `a` is a pair `(i, j)` with `i < j` and `a[i] > a[j]`. The naive count is O(n^2). The divide-and-conquer count is O(n log n): during a merge-sort merge, whenever we take an element from the right half before exhausting the left, every remaining left-half element forms an inversion with it.

This is the canonical example of "merge-sort gives more than sorting" — the algorithm counts inversions as a side effect of the standard merge.

## Why we use

- O(n log n) inversion count beats O(n^2) brute force.
- Combines naturally with merge-sort skeletons.
- Generalizes to "count pairs (i, j) with f(a[i], a[j])" via merging with a custom comparator.
- Used to measure "sortedness" — Kendall tau distance.

## How to implement

```
count_and_sort(a):
    if len(a) <= 1: return a, 0
    mid = len(a) // 2
    L, lc = count_and_sort(a[:mid])
    R, rc = count_and_sort(a[mid:])
    merged, mc = merge_count(L, R)
    return merged, lc + rc + mc

merge_count(L, R):
    i = j = 0; inv = 0; out = []
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
            inv += len(L) - i
    out.extend(L[i:]); out.extend(R[j:])
    return out, inv
```

```python
def count_inversions(a):
    def solve(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        L, lc = solve(arr[:mid])
        R, rc = solve(arr[mid:])
        return merge(L, R, lc + rc)
    def merge(L, R, base):
        out, i, j, inv = [], 0, 0, 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                out.append(L[i]); i += 1
            else:
                out.append(R[j]); j += 1
                inv += len(L) - i
        out.extend(L[i:]); out.extend(R[j:])
        return out, base + inv
    _, total = solve(a)
    return total
```

The key insight: when `L[i] > R[j]`, every element `L[i..]` is also `> R[j]` (because L is sorted), so they all form inversions with `R[j]`. Add `len(L) - i` to the count.

## Which problems this approach solves in the real world

- Measuring ranking similarity between two ordered lists (search relevance, recommender systems).
- Quantifying how "out of order" a dataset is.
- Counting reverse pairs / chains in time-series analysis.
- Detecting label drift between two ordered annotations.
- Computing Kendall's tau correlation in O(n log n).

## Pros and cons

**Pros**
- O(n log n) — strictly better than naive O(n^2).
- Easy to adapt to other "count pairs with property" problems.
- Stable: only adds counting bookkeeping to a standard merge.

**Cons**
- O(n) extra memory for the merge buffer.
- Recursion overhead matters for tiny inputs.
- Off-by-one in `len(L) - i` is the classic bug.

## Limitations

- Cannot be done in O(1) extra memory in this form.
- Streaming variant requires a Fenwick tree / order-statistic tree.
- Coordinate compression needed if values are non-integers.

## One example

**Problem**: Given an integer array `nums`, return the number of *reverse pairs* — pairs `(i, j)` with `i < j` and `nums[i] > 2 * nums[j]`.

**Input**: `nums = [1, 3, 2, 3, 1]`
**Output**: `2`
**Constraints**: `1 <= n <= 5 * 10^4`, `-2^31 <= nums[i] <= 2^31 - 1`.

## Solution explanation

```python
def reversePairs(nums):
    def solve(lo, hi):
        if hi - lo <= 1: return 0
        mid = (lo + hi) // 2
        count = solve(lo, mid) + solve(mid, hi)
        j = mid
        for i in range(lo, mid):
            while j < hi and nums[i] > 2 * nums[j]:
                j += 1
            count += j - mid
        nums[lo:hi] = sorted(nums[lo:hi])
        return count
    return solve(0, len(nums))
```

Walkthrough on `nums = [1, 3, 2, 3, 1]`:

| call      | range          | nums[lo:hi] before merge | reverse pairs found | nums after sort |
|-----------|----------------|--------------------------|---------------------|------------------|
| solve(3,5) | [3, 1]         | [3, 1]                   | 1 (3 > 2*1)         | [1, 3]           |
| solve(0,3) | [1, 3, 2]      | sub-solved, sorted: [1, 2, 3] | 1 (3 > 2*1 across mid=1) | [1, 2, 3] |
| solve(0,5) | [1,2,3,1,3]    | left=[1,2,3], right=[1,3] | 0 from cross (i=0:1<=2; i=1:2<=2; i=2:3<=2? no — 3>2*1 yes → count=1; 3>2*3 no). plus subcounts (1+1) → total 2 if we re-derive | merged |

Total = 2.

Time: O(n log n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Number of Pairs of Strings With Concatenation Equal to Target (LeetCode 2023) | https://leetcode.com/problems/number-of-pairs-of-strings-with-concatenation-equal-to-target/ |
| Medium | Count of Smaller Numbers After Self (LeetCode 315) | https://leetcode.com/problems/count-of-smaller-numbers-after-self/ |
| Hard | Reverse Pairs (LeetCode 493) | https://leetcode.com/problems/reverse-pairs/ |
