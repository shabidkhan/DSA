# Minimum platforms / rooms

## What is this

Minimum-platforms (a.k.a. meeting-rooms II) asks: given a list of intervals `[start, end]`, what is the minimum number of resources (rooms, platforms, runways) needed so that no two overlapping intervals share a resource?

The greedy approach: sort starts and ends separately. Sweep both with two pointers — when a start happens before the next end, you need a new platform; otherwise reuse one. The maximum simultaneous occupancy is the answer.

Equivalent formulations: max overlap count on a timeline, max value of a "sweep delta" prefix sum.

## Why we use

- O(n log n) sort + O(n) sweep.
- Returns the *minimum* resource count, not just feasibility.
- Two-pointer technique generalizes to many sweep-line problems.
- Same answer derived three ways: sort-and-sweep, heap of end times, or delta + prefix-max.

## How to implement (two-pointer sweep)

```
starts = sorted(starts)
ends = sorted(ends)
i = j = 0
platforms = 0
best = 0
while i < n:
    if starts[i] < ends[j]:
        platforms += 1; i += 1
        best = max(best, platforms)
    else:
        platforms -= 1; j += 1
return best
```

```python
def min_platforms(arrivals, departures):
    s = sorted(arrivals)
    e = sorted(departures)
    n = len(s)
    i = j = 0
    platforms = 0
    best = 0
    while i < n:
        if s[i] < e[j]:           # strict: same-time end before start is fine
            platforms += 1
            i += 1
            best = max(best, platforms)
        else:
            platforms -= 1
            j += 1
    return best
```

```python
import heapq

def min_meeting_rooms(intervals):
    if not intervals: return 0
    intervals.sort(key=lambda x: x[0])
    heap = []                      # end times
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heapreplace(heap, e)
        else:
            heapq.heappush(heap, e)
    return len(heap)
```

When two intervals share a boundary (one ends exactly when another starts), the convention depends on the problem — usually treated as non-overlapping.

## Which problems this approach solves in the real world

- Hospital / clinic exam-room scheduling.
- Conference room booking analytics.
- Airport runway / gate assignment.
- Container-port crane utilization.
- Train platform allocation given arrival/departure timetables.

## Pros and cons

**Pros**
- O(n log n) — fast even at scale.
- Three equivalent formulations let you pick the cleanest for the problem.
- Minimum value is provably optimal.

**Cons**
- Boundary semantics (touching ends) must be specified explicitly.
- Streaming variant requires a self-balancing tree of intervals.
- Multi-resource constraints (different sized rooms) need bin-packing.

## Limitations

- Doesn't assign *which* room each meeting goes to without extra bookkeeping.
- Cannot handle priorities — all meetings are equal.
- Real-time additions/removals need a different data structure.

## One example

**Problem**: Given an array of meeting time intervals `intervals` where `intervals[i] = [start, end]`, return the minimum number of conference rooms required.

**Input**: `intervals = [[0,30], [5,10], [15,20]]`
**Output**: `2`
**Constraints**: `1 <= n <= 10^4`, `0 <= start < end <= 10^6`.

## Solution explanation

```python
def minMeetingRooms(intervals):
    if not intervals: return 0
    starts = sorted(i[0] for i in intervals)
    ends   = sorted(i[1] for i in intervals)
    i = j = 0
    rooms = 0
    best = 0
    n = len(intervals)
    while i < n:
        if starts[i] < ends[j]:
            rooms += 1; i += 1
            best = max(best, rooms)
        else:
            rooms -= 1; j += 1
    return best
```

Walkthrough on `[[0,30], [5,10], [15,20]]`. Starts: `[0, 5, 15]`. Ends: `[10, 20, 30]`.

| step | i | j | starts[i] | ends[j] | action          | rooms | best |
|------|---|---|-----------|---------|-----------------|-------|------|
| 1    | 0 | 0 | 0         | 10      | start < end     | 1     | 1    |
| 2    | 1 | 0 | 5         | 10      | start < end     | 2     | 2    |
| 3    | 2 | 0 | 15        | 10      | start >= end    | 1     | 2    |
| 4    | 2 | 1 | 15        | 20      | start < end     | 2     | 2    |

i exhausts. Return 2. Time: O(n log n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Meeting Rooms (LeetCode 252) | https://leetcode.com/problems/meeting-rooms/ |
| Medium | Meeting Rooms II (LeetCode 253) | https://leetcode.com/problems/meeting-rooms-ii/ |
| Hard | Employee Free Time (LeetCode 759) | https://leetcode.com/problems/employee-free-time/ |
