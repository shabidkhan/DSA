# Quick sort

## What is this

Quick sort picks a pivot, partitions the array so elements `< pivot` go left and `> pivot` go right, then recursively sorts the two sides. The pivot ends up in its final position after partition. Average time O(n log n); worst case O(n^2) with bad pivot choices (sorted input + first-element pivot).

It is the dominant in-memory sort by constant factor on random data, and the foundation of std::sort, Introsort, and many language runtimes (with safeguards against worst case).

## Why we use

- Smallest constant factor among comparison sorts in practice.
- In-place — O(log n) recursion stack only.
- Cache-friendly partitioning.
- Easy to parallelize on the two halves.

## How to implement

```
quicksort(a, lo, hi):
    if lo >= hi: return
    p = partition(a, lo, hi)
    quicksort(a, lo, p - 1)
    quicksort(a, p + 1, hi)

partition(a, lo, hi):  # Lomuto
    pivot = a[hi]
    i = lo
    for j in lo..hi-1:
        if a[j] <= pivot:
            swap a[i], a[j]; i += 1
    swap a[i], a[hi]
    return i
```

```python
import random

def quicksort(a, lo=0, hi=None):
    if hi is None: hi = len(a) - 1
    if lo >= hi: return
    p = partition(a, lo, hi)
    quicksort(a, lo, p - 1)
    quicksort(a, p + 1, hi)

def partition(a, lo, hi):
    r = random.randint(lo, hi)
    a[r], a[hi] = a[hi], a[r]
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i
```

Randomize the pivot (or use median-of-three) to avoid the O(n^2) worst case on adversarial input.

## Which problems this approach solves in the real world

- General-purpose in-memory sort (C `qsort`, C++ `std::sort` introsort variant).
- Quickselect: find the k-th smallest in expected O(n).
- Sorting large arrays where O(n) extra memory is too much.
- Dual-pivot quicksort (Java's `Arrays.sort` for primitives).
- Partition-based 3-way for arrays with many duplicates.

## Pros and cons

**Pros**
- Best average constant factor among comparison sorts.
- In-place with O(log n) recursion.
- Cache-friendly.

**Cons**
- O(n^2) worst case without pivot randomization.
- Not stable.
- Many duplicates degrade naive Lomuto partition (use 3-way).

## Limitations

- Pathological worst case must be defended against (random pivot or introsort).
- Stability requires extra bookkeeping.
- Deep recursion risk on already-sorted input if not randomized.

## One example

**Problem**: Sort an integer array `nums` in non-decreasing order using quick sort.

**Input**: `nums = [3, 6, 8, 10, 1, 2, 1]`
**Output**: `[1, 1, 2, 3, 6, 8, 10]`
**Constraints**: `1 <= n <= 5 * 10^4`.

## Solution explanation

```python
def sortArray(nums):
    quicksort(nums, 0, len(nums) - 1)
    return nums
# quicksort and partition from above
```

Walkthrough on `[3, 6, 8, 10, 1, 2, 1]` (pivot = last element each call, no randomization for clarity):

| call           | range           | pivot | partition result          | next subproblems |
|----------------|-----------------|-------|---------------------------|------------------|
| sort(0..6)     | [3,6,8,10,1,2,1]| 1     | [1,1,8,10,6,2,3], p=1     | sort(0..0), sort(2..6) |
| sort(2..6)     | [_,_,8,10,6,2,3]| 3     | [_,_,2,3,6,10,8], p=3     | sort(2..2), sort(4..6) |
| sort(4..6)     | [_,_,_,_,6,10,8]| 8     | [_,_,_,_,6,8,10], p=5     | sort(4..4), sort(6..6) |

Final: `[1, 1, 2, 3, 6, 8, 10]`. Time: O(n log n) average, O(n^2) worst. Space: O(log n) stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Sort an Array (LeetCode 912) | https://leetcode.com/problems/sort-an-array/ |
| Medium | Kth Largest Element in an Array (LeetCode 215) | https://leetcode.com/problems/kth-largest-element-in-an-array/ |
| Hard | Wiggle Sort II (LeetCode 324) | https://leetcode.com/problems/wiggle-sort-ii/ |
