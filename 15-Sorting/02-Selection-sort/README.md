# Selection sort

## What is this

Selection sort divides the array into a sorted prefix and an unsorted suffix. On each pass it scans the suffix to find its minimum, then swaps that element into the front of the suffix, growing the sorted prefix by one. After n-1 passes the entire array is sorted.

Unlike bubble sort it performs at most n-1 swaps total, regardless of input. This is the fewest writes among the simple comparison sorts — useful when writes are expensive.

## Why we use

- Minimal number of writes (at most n-1 swaps).
- Predictable O(n^2) time on any input, including sorted.
- In-place, O(1) extra memory.
- Easy to reason about: invariant is "first i positions hold the i smallest values, sorted".

## How to implement

```
for i in 0..n-1:
    m = i
    for j in i+1..n-1:
        if a[j] < a[m]: m = j
    swap a[i], a[m]
```

```python
def selection_sort(a):
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
    return a
```

Selection sort is **not stable** by default — the swap can move an equal element past another equal element. A stable version uses shifting instead of swapping at extra cost.

## Which problems this approach solves in the real world

- Sorting small arrays on devices with expensive writes (EEPROM / flash).
- "Find k smallest" via partial selection sort (k passes only).
- Teaching the relationship between min-selection and heap sort.
- Hardware sorters where comparator count is the budget.
- Embedded systems with strict memory budgets.

## Pros and cons

**Pros**
- Minimal writes — useful when writes are costly.
- In-place, simple to implement.
- Performance is independent of input ordering.

**Cons**
- Always O(n^2) — no adaptive speedup on sorted input.
- Not stable in the standard form.
- Worse cache behavior than insertion sort on small arrays.

## Limitations

- Impractical beyond a few hundred elements.
- Inferior to insertion sort on nearly-sorted data.
- Stability requires a non-trivial rewrite.

## One example

**Problem**: Sort an integer array `nums` in non-decreasing order using selection sort.

**Input**: `nums = [64, 25, 12, 22, 11]`
**Output**: `[11, 12, 22, 25, 64]`
**Constraints**: `1 <= n <= 10^3`.

## Solution explanation

```python
def sortArray(nums):
    n = len(nums)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if nums[j] < nums[m]:
                m = j
        if m != i:
            nums[i], nums[m] = nums[m], nums[i]
    return nums
```

Walkthrough on `[64, 25, 12, 22, 11]`:

| pass i | min idx in [i..] | array after swap        |
|--------|------------------|-------------------------|
| 0      | 4 (val 11)       | [11, 25, 12, 22, 64]    |
| 1      | 2 (val 12)       | [11, 12, 25, 22, 64]    |
| 2      | 3 (val 22)       | [11, 12, 22, 25, 64]    |
| 3      | 3 (val 25)       | [11, 12, 22, 25, 64]    |

Time: O(n^2). Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Sort an Array (LeetCode 912) — selection sort variant | https://leetcode.com/problems/sort-an-array/ |
| Medium | Kth Largest Element in an Array (LeetCode 215) | https://leetcode.com/problems/kth-largest-element-in-an-array/ |
| Hard | Wiggle Sort II (LeetCode 324) | https://leetcode.com/problems/wiggle-sort-ii/ |
