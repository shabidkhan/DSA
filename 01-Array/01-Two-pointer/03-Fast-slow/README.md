# Fast/slow two pointers

## What is this

A two-pointer technique on a **linear sequence** (array, string, or any iterable with positional access) where two pointers move forward at **different rates** — typically a `slow` pointer advancing one step per iteration and a `fast` pointer advancing two (or more). On arrays, the common use is in-place compaction: `slow` marks "the next write position" for kept elements while `fast` scans through every index looking for elements to keep. The result is an O(n) pass that rewrites the array in place with O(1) extra space.

## Why we use

- Performs in-place filtering / deduplication in O(n) time with O(1) extra space — no auxiliary array.
- The slow/fast asymmetry is exactly what's needed for "keep one of every distinct" or "skip every k-th" style operations.
- The same conceptual pattern (different rates) powers cycle detection in linked lists (Floyd's tortoise-and-hare).

## How to implement

```
slow = 0
for fast in 0..n-1:
    if should_keep(arr[fast], arr[slow]):
        arr[slow + 1] = arr[fast]    # or just arr[slow] before increment
        slow += 1
return slow + 1                       # new length
```

Python — remove duplicates from a sorted array in place:

```python
def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

Python — move zeros to the end (preserve relative order of non-zeros):

```python
def move_zeros(nums: list[int]) -> None:
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

Invariant: at all times, `arr[0..slow]` (inclusive) holds the **already-compacted prefix** — exactly the elements we've decided to keep, in their original relative order. `fast` is the read cursor; `slow` is the write cursor. Whenever the read finds something keep-worthy, we advance the write cursor and copy.

## Which problems this approach solves in the real world

- **In-place log filtering**: drop debug-level lines from a buffer without allocating a new buffer.
- **Streaming deduplication**: collapse consecutive duplicate sensor readings to save bandwidth.
- **Audio/video sample decimation**: keep every k-th sample in place for downsampling.
- **Cleaning sorted contact lists**: remove duplicate phone numbers after a merge.
- **Embedded systems compaction**: rewrite an array of records skipping "deleted" slots without dynamic allocation.

## Pros and cons

**Pros**
- O(n) time, O(1) extra space — strict in-place transformation.
- Preserves relative order of kept elements (when implemented with the copy-forward pattern).
- Cache-friendly: both pointers move forward, so memory access is sequential.
- Single loop, easy to reason about with the slow=write / fast=read mental model.

**Cons**
- The "what to keep" predicate must be local (look at current and previous-kept), otherwise extra state is needed.
- The in-place rewrite destroys the original data — if the caller needs both, you must copy first.
- For "remove all duplicates including the first occurrence" (not just consecutive), you need a hash set or sort first.

## Limitations

- Works only on **sequences with positional writes** — not on streams or read-only data.
- For unsorted arrays, "remove duplicates" requires sorting first (O(n log n)) or a hash set (O(n) extra space) — slow/fast alone is insufficient.
- Doesn't generalise to 2D or graph structures.

## One example

**Problem**: Given a sorted integer array `nums`, remove the duplicates **in place** such that each unique element appears only once. The relative order of the elements should be kept the same. Return the number of unique elements `k`; the first `k` elements of `nums` should hold the unique values. Constraints: `1 ≤ nums.length ≤ 3·10^4`, `-100 ≤ nums[i] ≤ 100`, `nums` is sorted non-decreasing.

**Input**: `nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]`
**Output**: `k = 5`, with `nums = [0, 1, 2, 3, 4, _, _, _, _, _]` (underscores are don't-cares).

## Solution explanation

```python
def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

Walk-through on `nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]`:

| fast | nums[fast] | nums[slow] | action               | slow | nums after                        |
|------|------------|------------|----------------------|------|-----------------------------------|
| 1    | 0          | 0          | equal — skip         | 0    | [0,0,1,1,1,2,2,3,3,4]            |
| 2    | 1          | 0          | new → write nums[1]=1| 1    | [0,1,1,1,1,2,2,3,3,4]            |
| 3    | 1          | 1          | equal — skip         | 1    | (unchanged)                       |
| 4    | 1          | 1          | equal — skip         | 1    | (unchanged)                       |
| 5    | 2          | 1          | new → write nums[2]=2| 2    | [0,1,2,1,1,2,2,3,3,4]            |
| 6    | 2          | 2          | equal — skip         | 2    | (unchanged)                       |
| 7    | 3          | 2          | new → write nums[3]=3| 3    | [0,1,2,3,1,2,2,3,3,4]            |
| 8    | 3          | 3          | equal — skip         | 3    | (unchanged)                       |
| 9    | 4          | 3          | new → write nums[4]=4| 4    | [0,1,2,3,4,2,2,3,3,4]            |

Return `slow + 1 = 5`. The prefix `nums[0..4] = [0, 1, 2, 3, 4]` holds the unique values in their original relative order. The garbage after index 4 is acceptable per the problem spec.

- **Time**: O(n) — `fast` scans once.
- **Space**: O(1) — two indices, in-place writes.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Remove Element** — remove all occurrences of `val` in place and return new length. | https://leetcode.com/problems/remove-element/ |
| Medium | **Remove Duplicates from Sorted Array II** — at most two duplicates allowed; compare against `nums[slow - 1]`. | https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/ |
| Hard   | **Trapping Rain Water** — fast/slow style with running max from both ends (overlaps with opposite-ends). | https://leetcode.com/problems/trapping-rain-water/ |
