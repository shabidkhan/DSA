# Binary search on a sorted array

## What is this

A search technique where, on a **sorted array**, you repeatedly halve the search range by comparing the target with the middle element. The range shrinks geometrically — from `n` down to `1` in `log₂(n)` steps — so even billion-element arrays resolve in ~30 comparisons. The classic form finds an exact match; the more powerful forms (`lower_bound`, `upper_bound`) find the **boundary** between elements less than the target and elements greater than or equal to it.

## Why we use

- Reduces an O(n) linear scan to **O(log n)** time, with O(1) extra space.
- The boundary variants (`lower_bound`/`upper_bound`) unlock range-count queries, insertion-position queries, and "first/last occurrence" queries — all in log time.
- Forms the backbone of many other techniques: binary-search-on-answer, search in rotated arrays, and search in 2D row-sorted matrices.

## How to implement

```
left  = 0
right = n - 1
while left <= right:
    mid = left + (right - left) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
return -1
```

Python — classic exact match:

```python
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Python — `lower_bound` (first index `i` such that `nums[i] >= target`):

```python
def lower_bound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
```

Invariant: in the `[left, right]` form, the answer (if it exists) is always inside the closed window. Use `mid = left + (right - left) // 2` to avoid integer overflow in languages with bounded ints.

## Which problems this approach solves in the real world

- **Database index lookups**: B-tree leaves are sorted; finding a row by primary key uses binary-search-style descent.
- **Autocomplete dropdowns**: given a sorted dictionary of terms, find the first term with a given prefix using `lower_bound`.
- **Log file forensics**: locate the first log entry after a given timestamp without parsing the whole file.
- **Version lookup in package managers**: given sorted version tags, find the latest version satisfying `>= X.Y`.
- **Geospatial bucket lookups**: 1D-indexed quadtree/grid lookups land on the right bucket via binary search.

## Pros and cons

**Pros**
- O(log n) time vs O(n) linear scan — exponential speedup.
- O(1) extra space.
- Predictable, branch-light loop — cache-friendly for small ranges.
- Easy to adapt for "first occurrence", "last occurrence", "first ≥ x", "first > x" without changing the structure.

**Cons**
- Requires sorted input. Sorting first is O(n log n), which can dominate when you only search once.
- Off-by-one bugs (`left <= right` vs `left < right`, `mid` vs `mid + 1`) are notoriously easy to introduce.
- Doesn't help when the comparison function is non-monotonic with respect to the search criterion.

## Limitations

- Random access required — does not apply to singly linked lists or streamed data.
- Sorted ordering must be on the search key. If you need to search by a different key, you must re-sort or build a separate index.
- For very small arrays (n < ~16), linear scan is often faster due to branch prediction and cache effects.
- Duplicates require choosing between `lower_bound` and `upper_bound` semantics explicitly.

## One example

**Problem**: Given a sorted array `nums` and a target `t`, return the index of `t` in `nums`. If `t` is not present, return the index where it would be inserted to keep `nums` sorted. Constraints: `1 ≤ nums.length ≤ 10^4`, `-10^4 ≤ nums[i], t ≤ 10^4`.

**Input**: `nums = [1, 3, 5, 6]`, `t = 5`
**Output**: `2`

**Input**: `nums = [1, 3, 5, 6]`, `t = 2`
**Output**: `1`

## Solution explanation

```python
def search_insert(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
```

Walk-through on `nums = [1, 3, 5, 6]`, target = 2:

| step | left | right | mid | nums[mid] | action |
|------|------|-------|-----|-----------|--------|
| 0    | 0    | 4     | 2   | 5         | 5 ≥ 2 → `right = 2` |
| 1    | 0    | 2     | 1   | 3         | 3 ≥ 2 → `right = 1` |
| 2    | 0    | 1     | 0   | 1         | 1 < 2 → `left = 1`  |
| 3    | 1    | 1     | —   | —         | loop ends → return **1** |

The `[left, right)` half-open form converges on the **first** index `i` such that `nums[i] >= target` — which is exactly the insert position. When `target` exists, that index is its position; when it doesn't, that's where it belongs.

- **Time**: O(log n) — each iteration halves the range.
- **Space**: O(1) — two integer indices.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Binary Search** — return index of target in a sorted array, or -1. | https://leetcode.com/problems/binary-search/ |
| Medium | **Find First and Last Position of Element in Sorted Array** — return `[first, last]` indices of `target`. | https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/ |
| Hard   | **Median of Two Sorted Arrays** — find the median of two sorted arrays in O(log(min(m, n))) using partition-based binary search. | https://leetcode.com/problems/median-of-two-sorted-arrays/ |
