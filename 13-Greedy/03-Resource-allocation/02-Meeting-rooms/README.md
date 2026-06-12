# Meeting Rooms (Resource Allocation)

## What is this

Meeting Rooms framed as resource allocation answers two related questions: "can all meetings share a single room?" (Meeting Rooms I) and "how many rooms are needed at peak concurrency?" (Meeting Rooms II). It is the canonical example of the **sweep-line + counter** family of greedy problems: we transform interval data into a stream of `+1` (start) and `-1` (end) events, then walk through time tracking how many resources are currently in use.

The single-resource version reduces to scanning sorted intervals and checking any overlap. The multi-resource version computes `max(concurrent_count)` over all events, which equals the chromatic number of the interval conflict graph and is achievable by either a min-heap of end-times or the chronological event sweep.

## Why we use

- It directly answers "how many resources do I need?" — a question that arises in calendars, threading, and connection pools.
- The event-sweep view generalises to weighted demand (e.g., each meeting needs 2 rooms), bandwidth, or memory profiling.
- Min-heap variant runs in O(n log n) and uses O(rooms) extra space — both tight bounds.
- Combined with greedy room assignment, it produces an actual schedule, not just a count.

## How to implement

Meeting Rooms I — sort by start, check adjacents:

```python
def can_attend_all(intervals):
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True
```

Meeting Rooms II — min-heap of end times:

```python
import heapq
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []                          # min-heap of end times
    for s, e in intervals:
        if heap and heap[0] <= s:      # room frees in time
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)
```

```javascript
function minMeetingRooms(intervals) {
    const starts = intervals.map(i => i[0]).sort((a,b)=>a-b);
    const ends   = intervals.map(i => i[1]).sort((a,b)=>a-b);
    let rooms = 0, j = 0;
    for (let i = 0; i < starts.length; i++) {
        if (starts[i] < ends[j]) rooms++;
        else j++;
    }
    return rooms;
}
```

Invariant (heap version): the heap always contains the end times of currently-occupied rooms; the smallest end time tells us when the next room will be free.

## Which problems this approach solves in the real world

- Sizing a conference center: how many rooms do we need at peak?
- Determining minimum connection-pool size to satisfy peak DB load.
- Choosing the number of cashier lanes for a forecast of arrival/end times.
- Air-traffic gate allocation given inbound/outbound schedules.
- Cloud instance auto-scaling based on overlapping job intervals.
- Hospital bed planning during overlapping admission windows.

## Pros and cons

**Pros**
- O(n log n) — optimal for comparison-based solutions.
- Min-heap version yields a concrete room-assignment scheme.
- Adapts cleanly to weighted/capacitated variants.
- Easy to reason about and to unit-test.

**Cons**
- Sort-by-start with the heap pattern is subtle; it's easy to wire it wrong.
- Half-open vs closed intervals materially change the comparison.
- The chronological two-array sweep (starts vs ends) is faster in practice but reveals less about *which* meeting goes in *which* room.
- For very large `n`, sorting dominates; bucketing by time may be needed.

## Limitations

- Works only when intervals are known up-front; for streaming arrivals, online algorithms are needed.
- Assumes rooms are identical; heterogeneous rooms need DP or matching.
- Ignores priorities — a high-priority meeting can be evicted in some formulations.
- Tie-breaking among equal start/end times must match the spec.

## One example

**Problem (Meeting Rooms II)**: Given an array of meeting time intervals `intervals[i] = [start_i, end_i]`, return the **minimum number of conference rooms** required so that no two meetings in the same room overlap.

Constraints: 1 <= n <= 10^4; 0 <= start_i < end_i <= 10^6.

**Input**: `intervals = [[0,30],[5,10],[15,20]]`

**Output**: `2`

## Solution explanation

```python
import heapq

def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)
```

Sorted input: `[[0,30],[5,10],[15,20]]`. Walk-through:

| Step | Meeting | Heap top before | Free a room? | Heap after push | Rooms in use |
|------|---------|-----------------|--------------|-----------------|--------------|
| 1 | [0,30] | empty | no | [30] | 1 |
| 2 | [5,10] | 30 (5<30) | no | [10,30] | 2 |
| 3 | [15,20] | 10 (10<=15) | yes, pop 10 | [20,30] | 2 |

Final heap size is 2, so two rooms suffice. Correctness: at any instant the heap contains exactly the rooms still occupied; pushing always reflects "this meeting takes a room", and popping reflects "an old meeting has ended on time". The heap size therefore tracks current concurrency, and the maximum it ever reaches is the answer.

- **Time**: O(n log n)
- **Space**: O(n) for the heap in the worst case

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Meeting Rooms | https://leetcode.com/problems/meeting-rooms/ |
| Medium | Meeting Rooms II | https://leetcode.com/problems/meeting-rooms-ii/ |
| Hard | Employee Free Time | https://leetcode.com/problems/employee-free-time/ |
