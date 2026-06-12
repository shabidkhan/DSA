# Bubble sort

## What is this

Bubble sort repeatedly walks the array comparing adjacent pairs and swapping them if they are out of order. After one full pass the largest element has "bubbled" to the end. After k passes the last k elements are in their final position. The algorithm terminates when a pass performs no swaps.

It is the simplest comparison sort: easy to explain, easy to prove correct, and useful as a teaching baseline. In practice it is rarely deployed — its O(n^2) worst case loses to merge / quick / Tim sort by orders of magnitude.

## Why we use

- Easiest sort to understand and implement.
- In-place (O(1) extra memory).
- Stable (equal elements preserve relative order).
- Adaptive — exits early on nearly-sorted input.

## How to implement

```
for i in 0..n-1:
    swapped = False
    for j in 0..n-i-2:
        if a[j] > a[j+1]:
            swap a[j], a[j+1]
            swapped = True
    if not swapped: break
```

```python
def bubble_sort(a):
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a
```

The `swapped` flag turns a worst-case O(n^2) algorithm into O(n) on already-sorted input.

## Which problems this approach solves in the real world

- Teaching the comparison-sort family.
- Sorting tiny lists (n < 10) where constant factors dominate.
- Detecting whether an array is sorted (single pass with no swap).
- Generating adjacent-swap distance metrics (number of swaps = inversion count).
- Lightweight embedded code where binary size matters more than speed.

## Pros and cons

**Pros**
- Trivial implementation, very small code footprint.
- Stable and in-place.
- Adaptive on near-sorted data.

**Cons**
- O(n^2) average and worst case.
- Many writes — bad for write-expensive media (flash).
- Outperformed by insertion sort on the same workload.

## Limitations

- Unusable beyond a few hundred elements.
- Worst on reverse-sorted input.
- Cache-unfriendly compared with merge sort on large data.

## One example

**Problem**: Sort an integer array `nums` in non-decreasing order using bubble sort.

**Input**: `nums = [5, 1, 4, 2, 8]`
**Output**: `[1, 2, 4, 5, 8]`
**Constraints**: `1 <= n <= 10^3`, `-10^4 <= nums[i] <= 10^4`.

## Solution explanation

```python
def sortArray(nums):
    n = len(nums)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:
            break
    return nums
```

Walkthrough on `[5, 1, 4, 2, 8]`:

| pass | array after pass    | swaps |
|------|---------------------|-------|
| 1    | [1, 4, 2, 5, 8]     | 3     |
| 2    | [1, 2, 4, 5, 8]     | 1     |
| 3    | [1, 2, 4, 5, 8]     | 0 → break |

Time: O(n^2) worst, O(n) best. Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Sort an Array (LeetCode 912) — use bubble sort | https://leetcode.com/problems/sort-an-array/ |
| Medium | Pancake Sorting (LeetCode 969) | https://leetcode.com/problems/pancake-sorting/ |
| Hard | Global and Local Inversions (LeetCode 775) | https://leetcode.com/problems/global-and-local-inversions/ |
