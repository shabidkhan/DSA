# Interval scheduling

## What is this

Interval scheduling problems take a set of intervals (each with a start and end) and ask for the optimal way to select, merge, partition, or count them under some constraint: maximum count of compatible intervals, minimum rooms to host them all, total coverage, minimum number of overlaps to remove, and so on.

Most variants share two preprocessing steps: sort by start or by end, then sweep with a small bookkeeping data structure (a variable, a heap, or two pointers). The right sort key depends on which quantity is being optimised.

## Why we use

- One sort + linear sweep solves a family of scheduling problems
- Greedy proofs by exchange argument are clean and short
- Common preparation for harder DP variants (weighted intervals)
- Maps naturally onto rooms, time slots, machines, and channels

## How to implement

```
Variant 1 — max non-overlapping (count):
    sort by end ascending; greedily pick earliest-finishing compatible

Variant 2 — minimum rooms (chromatic number of interval graph):
    sort by start ascending; min-heap of currently-active end times;
    if heap top <= current start, pop (reuse room); else push (new room);
    answer is max heap size seen

Variant 3 — minimum intervals to remove so the rest are non-overlapping:
    total - (max non-overlapping)
```

Minimum number of rooms needed to host all meetings:

```python
import heapq

def min_meeting_rooms(intervals: list[tuple[int, int]]) -> int:
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap: list[int] = []
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)
```

Maximum non-overlapping subset:

```python
def max_non_overlapping(intervals: list[tuple[int, int]]) -> int:
    intervals.sort(key=lambda x: x[1])
    last_end = float("-inf")
    count = 0
    for s, e in intervals:
        if s >= last_end:
            count += 1
            last_end = e
    return count
```

Invariant for the rooms variant: at any point during the sweep, the heap contains exactly the end times of currently-active meetings. The maximum heap size during the sweep equals the maximum simultaneous overlap, which is the minimum room count.

## Which problems this approach solves in the real world

- Meeting-room allocation in calendar apps
- TV / radio broadcast slot assignment
- Operating-room scheduling in hospitals
- Cloud auto-scaling: minimum number of VMs to serve all scheduled jobs
- Lab-equipment reservation across multiple research groups

## Pros and cons

**Pros**
- O(n log n) sort dominates
- Each variant has a tight one-page implementation
- Greedy decisions have provable optimality

**Cons**
- Wrong sort key silently produces wrong answers
- Heavy edge cases on equal endpoints (open vs closed intervals)
- Weighted scheduling breaks pure greedy — need DP + binary search

## Limitations

- Weighted variants (max total weight, not count) require DP
- Multi-resource generalisations (each interval needs `k` of `m` rooms) are NP-hard
- Online versions have proven competitive-ratio bounds — no offline-optimum

## One example

Problem: Given an array `intervals` where `intervals[i] = (start_i, end_i)`, return the minimum number of conference rooms required to host all meetings.

```
Input:  intervals = [(0, 30), (5, 10), (15, 20)]
Output: 2    ((0,30) needs one room; (5,10) needs another; (15,20) can reuse the room freed at 10)
Constraints: 1 <= n <= 10^4, 0 <= start_i < end_i <= 10^6
```

## Solution explanation

```python
import heapq

def min_meeting_rooms(intervals: list[tuple[int, int]]) -> int:
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap: list[int] = []
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)
```

Process meetings in start order. The heap holds the end times of currently-occupied rooms; if the earliest-ending room frees up before the current meeting starts, reuse it (pop); otherwise allocate a new room (push). Final heap size = rooms needed.

Walkthrough for `intervals = [(0, 30), (5, 10), (15, 20)]`:

| Meeting   | Heap before  | heap[0] <= s? | Heap after |
|-----------|--------------|----------------|------------|
| (0, 30)   | []           | (empty)        | [30]       |
| (5, 10)   | [30]         | 30 <= 5? no    | [10, 30]   |
| (15, 20)  | [10, 30]     | 10 <= 15? yes  | [20, 30]   |

Final heap size = 2. Time O(n log n), space O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Merge Intervals (LeetCode 56) | https://leetcode.com/problems/merge-intervals/ |
| Medium | Meeting Rooms II (LeetCode 253) | https://leetcode.com/problems/meeting-rooms-ii/ |
| Hard | Employee Free Time (LeetCode 759) | https://leetcode.com/problems/employee-free-time/ |
