# Insertion sort

## What is this

Insertion sort grows a sorted prefix one element at a time. For each new element it shifts larger elements in the prefix one step right, then drops the new element into the resulting gap. The invariant after position i: `a[0..i]` is sorted.

It is the best of the simple O(n^2) sorts in practice: stable, adaptive (linear on nearly-sorted input), and the inner loop is so cheap that real implementations (Tim sort, Introsort) fall back to insertion sort below ~16 elements.

## Why we use

- O(n) on nearly-sorted input.
- Stable and in-place.
- Tiny constant factor — beats merge / quick sort on very small arrays.
- Online: can insert into a sorted prefix as new elements arrive.

## How to implement

```
for i in 1..n-1:
    x = a[i]
    j = i - 1
    while j >= 0 and a[j] > x:
        a[j+1] = a[j]
        j -= 1
    a[j+1] = x
```

```python
def insertion_sort(a):
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a
```

The shift (`a[j+1] = a[j]`) avoids repeated swaps — half the writes of a naive swap-based version.

## Which problems this approach solves in the real world

- Inner loop of Tim sort and Introsort on small subarrays.
- Streaming inserts into a small sorted buffer.
- Sorting small batches in embedded firmware.
- Maintaining a sorted "top-N recent events" window.
- Educational baseline for comparison-sort analysis.

## Pros and cons

**Pros**
- O(n) on sorted / near-sorted input.
- Stable and in-place.
- Excellent cache behavior — sequential memory access.

**Cons**
- O(n^2) on reverse-sorted input.
- Many comparisons on random data — loses to merge / quick sort beyond ~30 elements.
- Each insert may shift many elements.

## Limitations

- Impractical for n > a few thousand on random data.
- Linked lists make the shift cheap but lose cache friendliness.
- Not parallelizable.

## One example

**Problem**: Sort the integer array `nums` in non-decreasing order using insertion sort.

**Input**: `nums = [5, 2, 4, 6, 1, 3]`
**Output**: `[1, 2, 3, 4, 5, 6]`
**Constraints**: `1 <= n <= 10^4`.

## Solution explanation

```python
def sortArray(nums):
    for i in range(1, len(nums)):
        x = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > x:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = x
    return nums
```

Walkthrough on `[5, 2, 4, 6, 1, 3]`:

| i | x  | array before shift   | array after insert      |
|---|----|----------------------|-------------------------|
| 1 | 2  | [5, 2, 4, 6, 1, 3]   | [2, 5, 4, 6, 1, 3]      |
| 2 | 4  | [2, 5, 4, 6, 1, 3]   | [2, 4, 5, 6, 1, 3]      |
| 3 | 6  | [2, 4, 5, 6, 1, 3]   | [2, 4, 5, 6, 1, 3]      |
| 4 | 1  | [2, 4, 5, 6, 1, 3]   | [1, 2, 4, 5, 6, 3]      |
| 5 | 3  | [1, 2, 4, 5, 6, 3]   | [1, 2, 3, 4, 5, 6]      |

Time: O(n^2) worst, O(n) best, O(n * k) where k = max distance any element moves. Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Insertion Sort List (LeetCode 147) | https://leetcode.com/problems/insertion-sort-list/ |
| Medium | Sort Colors (LeetCode 75) | https://leetcode.com/problems/sort-colors/ |
| Hard | Count of Smaller Numbers After Self (LeetCode 315) | https://leetcode.com/problems/count-of-smaller-numbers-after-self/ |
