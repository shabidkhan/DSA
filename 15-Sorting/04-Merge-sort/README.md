# Merge sort

## What is this

Merge sort is a divide-and-conquer sort: split the array in half, recursively sort each half, then merge the two sorted halves into one. The merge step walks two pointers and writes the smaller front element into output. Total work per level is O(n) for the merge, and there are O(log n) levels — giving an O(n log n) worst-case guarantee.

It is stable and forms the basis of Tim sort (Python's `sorted`), external sorting (sort datasets larger than memory), and parallel sorting frameworks.

## Why we use

- Guaranteed O(n log n) — no worst-case degradation.
- Stable: equal elements preserve relative order.
- Naturally external: works in linear streaming passes for disk-resident data.
- Parallelizable — independent halves sort independently.

## How to implement

```
sort(a, lo, hi):
    if lo + 1 >= hi: return
    mid = (lo + hi) // 2
    sort(a, lo, mid)
    sort(a, mid, hi)
    merge(a, lo, mid, hi)
```

```python
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return merge(left, right)

def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out
```

```python
def merge_sort_inplace(a, lo=0, hi=None):
    if hi is None: hi = len(a)
    if hi - lo <= 1: return
    mid = (lo + hi) // 2
    merge_sort_inplace(a, lo, mid)
    merge_sort_inplace(a, mid, hi)
    buf = a[lo:mid]
    i, j, k = 0, mid, lo
    while i < len(buf) and j < hi:
        if buf[i] <= a[j]:
            a[k] = buf[i]; i += 1
        else:
            a[k] = a[j]; j += 1
        k += 1
    while i < len(buf):
        a[k] = buf[i]; i += 1; k += 1
```

Use `<=` (not `<`) in the merge comparison to keep the sort stable.

## Which problems this approach solves in the real world

- External sorting of multi-terabyte log files.
- `sorted()` / `list.sort()` in Python (Tim sort variant of merge sort).
- Counting inversions in O(n log n).
- Parallel sort frameworks in Spark / Hadoop.
- Sorting linked lists with O(1) extra pointer space.

## Pros and cons

**Pros**
- Guaranteed O(n log n) on any input.
- Stable.
- Excellent for external / streaming data.

**Cons**
- O(n) extra memory (or O(log n) for in-place variants).
- Constant factor higher than quick sort on in-memory random data.
- Worse cache behavior than insertion sort on tiny arrays.

## Limitations

- Memory allocator pressure on the recursive splits.
- Not in-place in the textbook form.
- Recursion depth O(log n) — overflow risk on extremely small stacks.

## One example

**Problem**: Sort an integer array `nums` in non-decreasing order using merge sort.

**Input**: `nums = [38, 27, 43, 3, 9, 82, 10]`
**Output**: `[3, 9, 10, 27, 38, 43, 82]`
**Constraints**: `1 <= n <= 5 * 10^4`.

## Solution explanation

```python
def sortArray(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = sortArray(nums[:mid])
    right = sortArray(nums[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out
```

Walkthrough on `[38, 27, 43, 3, 9, 82, 10]`:

| level | splits                                                  |
|-------|---------------------------------------------------------|
| 0     | [38,27,43,3,9,82,10]                                     |
| 1     | [38,27,43] [3,9,82,10]                                   |
| 2     | [38] [27,43] [3,9] [82,10]                               |
| 3     | [38] [27] [43] [3] [9] [82] [10]                         |
| merge | [27,43] [3,9] [10,82]                                    |
| merge | [27,38,43] [3,9,10,82]                                   |
| merge | [3,9,10,27,38,43,82]                                     |

Time: O(n log n) worst case. Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Merge Sorted Array (LeetCode 88) | https://leetcode.com/problems/merge-sorted-array/ |
| Medium | Sort List (LeetCode 148) | https://leetcode.com/problems/sort-list/ |
| Hard | Count of Smaller Numbers After Self (LeetCode 315) | https://leetcode.com/problems/count-of-smaller-numbers-after-self/ |
