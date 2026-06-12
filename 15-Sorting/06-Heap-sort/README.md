# Heap sort

## What is this

Heap sort builds a max-heap in place over the array (O(n) by sift-down from the middle), then repeatedly swaps the root with the last unsorted position and shrinks the heap by one. After n-1 such extractions the array is sorted.

It pairs an in-place data structure with a tight O(n log n) worst-case guarantee. Unlike quick sort it has no pathological input; unlike merge sort it uses O(1) extra memory.

## Why we use

- Worst-case O(n log n) — no adversarial degradation.
- In-place with O(1) extra memory.
- Easy proof of correctness from heap invariants.
- Forms the basis of priority queues used in many other algorithms.

## How to implement

```
heapify(a):         # build max-heap
    for i in n/2 - 1 .. 0: sift_down(a, i, n)

heap_sort(a):
    heapify(a)
    for end in n-1 .. 1:
        swap a[0], a[end]
        sift_down(a, 0, end)

sift_down(a, i, n):
    while 2i+1 < n:
        j = 2i+1
        if j+1 < n and a[j+1] > a[j]: j += 1
        if a[i] >= a[j]: break
        swap a[i], a[j]; i = j
```

```python
def heap_sort(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)
    return a

def sift_down(a, i, n):
    while 2 * i + 1 < n:
        j = 2 * i + 1
        if j + 1 < n and a[j + 1] > a[j]:
            j += 1
        if a[i] >= a[j]:
            break
        a[i], a[j] = a[j], a[i]
        i = j
```

Note: heap sort is not stable. To find k smallest in O(n + k log n) use heap-based partial sort or quickselect.

## Which problems this approach solves in the real world

- Priority queues in OS schedulers, task queues, Dijkstra.
- Selection problems (top-k largest / smallest with `heapq.nlargest`).
- External-memory sorting where worst-case bounds matter.
- Constant-memory environments (no merge-sort buffer available).
- Real-time systems where worst-case latency must be bounded.

## Pros and cons

**Pros**
- Guaranteed O(n log n).
- In-place, O(1) extra memory.
- No pivot-pathological input.

**Cons**
- Not stable.
- Worse cache behavior than quick sort (jumps around array).
- Constant factor larger than quick sort on random data.

## Limitations

- Cache-unfriendly: each `sift_down` touches arbitrary indices.
- Hard to parallelize compared with merge sort.
- Stability requires augmentation.

## One example

**Problem**: Sort an integer array `nums` in non-decreasing order using heap sort.

**Input**: `nums = [4, 10, 3, 5, 1]`
**Output**: `[1, 3, 4, 5, 10]`
**Constraints**: `1 <= n <= 5 * 10^4`.

## Solution explanation

```python
def sortArray(nums):
    n = len(nums)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(nums, i, n)
    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(nums, 0, end)
    return nums
```

Walkthrough on `[4, 10, 3, 5, 1]`:

| step                     | array            |
|--------------------------|------------------|
| initial                  | [4, 10, 3, 5, 1] |
| heapify i=1 (10 vs 5,1)  | [4, 10, 3, 5, 1] |
| heapify i=0 (4 vs 10,3)  | [10, 5, 3, 4, 1] (sift 4 down → swap 5) |
| extract: swap 0,4        | [1, 5, 3, 4, 10] |
| sift_down(0, n=4)        | [5, 4, 3, 1, 10] |
| extract: swap 0,3        | [1, 4, 3, 5, 10] |
| sift_down(0, n=3)        | [4, 1, 3, 5, 10] |
| extract: swap 0,2        | [3, 1, 4, 5, 10] |
| sift_down(0, n=2)        | [3, 1, 4, 5, 10] |
| extract: swap 0,1        | [1, 3, 4, 5, 10] |

Time: O(n log n). Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Last Stone Weight (LeetCode 1046) | https://leetcode.com/problems/last-stone-weight/ |
| Medium | Sort an Array (LeetCode 912) | https://leetcode.com/problems/sort-an-array/ |
| Hard | Find Median from Data Stream (LeetCode 295) | https://leetcode.com/problems/find-median-from-data-stream/ |
