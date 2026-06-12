# Partition (Dutch national flag)

## What is this

The partition pattern rearranges an array around a pivot (or a set of categories) so that elements are grouped by class while moving each element at most once. The Dutch national flag algorithm by Dijkstra is its canonical form: three pointers split the array into "less than pivot", "equal to pivot", and "greater than pivot" in a single O(n) pass with O(1) extra space.

It is the partition primitive behind quicksort, three-way quicksort (great for arrays with many duplicates), and "sort colors" style problems.

## Why we use

- O(n) single-pass classification — strictly better than two-pass solutions.
- O(1) extra memory (in-place swaps).
- Stable behavior for the three-class output regions.
- Foundation for three-way quicksort (handles duplicates efficiently).

## How to implement

```
i = 0          # boundary of "less"
j = 0          # cursor
k = n - 1      # boundary of "greater"
while j <= k:
    if a[j] < pivot:  swap(a[i], a[j]); i += 1; j += 1
    elif a[j] > pivot: swap(a[j], a[k]); k -= 1
    else:              j += 1
```

```python
def dutch_flag(a, pivot):
    i, j, k = 0, 0, len(a) - 1
    while j <= k:
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1; j += 1
        elif a[j] > pivot:
            a[j], a[k] = a[k], a[j]
            k -= 1
        else:
            j += 1
    return a
```

```python
def sort_colors(nums):
    return dutch_flag(nums, pivot=1)
```

When swapping with `k` you do **not** advance `j` — the swapped-in element from the back has not been classified yet.

## Which problems this approach solves in the real world

- Three-class label sorting (positive / neutral / negative sentiment).
- Triage queues partitioned into high / medium / low priority.
- Partitioning packet streams into accepted / pending / dropped.
- Splitting a dataset by a categorical column before grouping.
- Quickselect / quicksort partition step.

## Pros and cons

**Pros**
- O(n) in-place classification.
- Handles three categories without two passes.
- Excellent for arrays with many duplicates (three-way quicksort).

**Cons**
- Not stable in the within-class ordering sense.
- Pivot must be a comparable value the algorithm understands.
- Off-by-one on `j` advance after the right-swap is the classic bug.

## Limitations

- Only directly handles 2 or 3 partitions; more classes need a different scheme (counting sort).
- Comparator must be a total order.
- Not directly parallelizable without merging boundaries.

## One example

**Problem**: Given an array `nums` with `n` objects colored red (0), white (1), or blue (2), sort them in place so that objects of the same color are adjacent in the order red, white, blue. Use a one-pass O(1)-space algorithm.

**Input**: `nums = [2, 0, 2, 1, 1, 0]`
**Output**: `[0, 0, 1, 1, 2, 2]`
**Constraints**: `1 <= n <= 300`, `nums[i] in {0, 1, 2}`.

## Solution explanation

```python
def sortColors(nums):
    i, j, k = 0, 0, len(nums) - 1
    while j <= k:
        if nums[j] == 0:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1; j += 1
        elif nums[j] == 2:
            nums[j], nums[k] = nums[k], nums[j]
            k -= 1
        else:
            j += 1
    return nums
```

Walkthrough on `[2, 0, 2, 1, 1, 0]`:

| step | i | j | k | array               | action               |
|------|---|---|---|---------------------|----------------------|
| 0    | 0 | 0 | 5 | [2, 0, 2, 1, 1, 0]  | a[j]=2 → swap j,k; k-- |
| 1    | 0 | 0 | 4 | [0, 0, 2, 1, 1, 2]  | a[j]=0 → swap i,j; i++,j++ |
| 2    | 1 | 1 | 4 | [0, 0, 2, 1, 1, 2]  | a[j]=0 → swap i,j; i++,j++ |
| 3    | 2 | 2 | 4 | [0, 0, 2, 1, 1, 2]  | a[j]=2 → swap j,k; k-- |
| 4    | 2 | 2 | 3 | [0, 0, 1, 1, 2, 2]  | a[j]=1 → j++         |
| 5    | 2 | 3 | 3 | [0, 0, 1, 1, 2, 2]  | a[j]=1 → j++         |
| 6    | 2 | 4 | 3 | done (j > k)        |                      |

Time: O(n). Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Move Zeroes (LeetCode 283) | https://leetcode.com/problems/move-zeroes/ |
| Medium | Sort Colors (LeetCode 75) | https://leetcode.com/problems/sort-colors/ |
| Hard | Wiggle Sort II (LeetCode 324) | https://leetcode.com/problems/wiggle-sort-ii/ |
