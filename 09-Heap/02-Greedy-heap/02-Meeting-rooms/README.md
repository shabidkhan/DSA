# Meeting rooms (min-heap of end times)

## What is this

Given a set of meeting time intervals, decide either (a) whether a single person can attend all of them (no overlaps), or (b) what is the **minimum number of conference rooms** needed to host every meeting (the classic "Meeting Rooms II"). The greedy-heap solution sorts meetings by **start time**, then maintains a **min-heap of end times** of currently-running meetings. When the next meeting starts, if the heap's minimum end time is ≤ its start, that room is free — pop and reuse it; otherwise, allocate a new room. The answer is the **maximum heap size** seen during the sweep — equivalently, the heap size after all meetings have been processed if we don't pop on departure.

## Why we use

- O(n log n) time — sorting dominates; heap operations are log n.
- Models a real-world dispatch / scheduling problem directly.
- The min-heap acts as a "set of in-flight rooms ordered by who frees up next" — exactly the question we want answered at each step.
- Generalises to other "minimum resources" problems (CPUs, runways, taxi cabs).

## How to implement

```
sort meetings by start time
heap = empty min-heap (stores end times)
for (s, e) in meetings:
    if heap is non-empty and heap.top <= s:
        heap.pop()              # an earlier meeting ended in time
    heap.push(e)
return len(heap)                # peak concurrency = answer
```

Python:

```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap: list[int] = []                # min-heap of end times
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heappop(heap)
        heapq.heappush(heap, e)
    return len(heap)
```

JavaScript (using a manual min-heap or library):

```javascript
function minMeetingRooms(intervals) {
  if (!intervals.length) return 0;
  intervals.sort((a, b) => a[0] - b[0]);
  // Naive priority queue using a sorted array (fine for small inputs):
  const heap = [];
  const push = (x) => {
    let i = heap.findIndex(v => v > x);
    if (i === -1) heap.push(x); else heap.splice(i, 0, x);
  };
  for (const [s, e] of intervals) {
    if (heap.length && heap[0] <= s) heap.shift();
    push(e);
  }
  return heap.length;
}
```

Invariant: at any point during the sweep, `heap` is exactly the multiset of **end times of meetings currently in progress** — i.e. meetings that have started but not yet ended at time `s`.

## Visual

Intervals `[[0,30], [5,10], [15,20]]` after sorting by start:

```
time → 0 ──── 5 ──── 10 ──── 15 ──── 20 ──── 30
        [───── 30 ─────────────────────────]
              [─── 10 ───]
                            [─── 20 ───]
```

At time 5: room1 still busy (until 30), need room2 → 2 rooms.
At time 15: room2 free (10 ≤ 15), reuse → still 2 rooms.

Answer: **2**.

## Which problems this approach solves in the real world

- **Conference room booking systems**: minimum rooms to host all meetings.
- **Airport runway scheduling**: minimum runways to handle all takeoff/landing windows.
- **CPU / VM allocation**: minimum machines to host concurrent tasks.
- **Taxi dispatch**: minimum vehicles to satisfy ride requests.
- **Hospital bed allocation**: minimum beds needed during peak admission windows.
- **Network bandwidth slot allocation**: minimum channels to serve overlapping streams.

## Pros and cons

**Pros**
- O(n log n) — fast enough for 10⁵+ intervals.
- The heap-as-room-pool framing makes the algorithm intuitive.
- Easy to extend to "which meeting goes in which room" by storing a room id alongside the end time.
- Trivially produces a schedule, not just a count.

**Cons**
- Sorting cost dominates — overkill if `n` is small.
- A simpler "event sweep" (sort starts and ends separately, sweep both) runs in O(n log n) without a heap and is equally fast.
- Edge cases: meetings starting **at** the same time another ends — the inequality `<=` vs `<` controls whether they share a room. Pick deliberately.

## Limitations

- Assumes intervals are known up-front; doesn't handle online arrival of meetings (use a streaming algorithm or interval tree).
- Doesn't handle preemption — a meeting can't be interrupted and resumed.
- Doesn't optimise for "minimise number of meetings rejected" — that's a different problem.

## One example

**Problem**: Given an array `intervals` where `intervals[i] = [start_i, end_i]`, return the **minimum number of conference rooms** required.
Constraints: `1 ≤ n ≤ 10^4`, `0 ≤ start_i < end_i ≤ 10^6`.

**Input**: `intervals = [[0, 30], [5, 10], [15, 20]]`
**Output**: `2`.

## Solution explanation

```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
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

Walk-through on `[[0,30], [5,10], [15,20]]` after sorting:

| step | (s, e)   | heap before | top ≤ s?     | action                | heap after |
|------|----------|-------------|--------------|-----------------------|------------|
| 1    | (0, 30)  | []          | —            | push 30               | [30]       |
| 2    | (5, 10)  | [30]        | 30 ≤ 5? no   | push 10               | [10, 30]   |
| 3    | (15, 20) | [10, 30]    | 10 ≤ 15? yes | pop 10, push 20       | [20, 30]   |

Final heap size: **2**.

Correctness: by sorting by start time, we process meetings in the order they begin. The min-heap's root is the **earliest end time** among active meetings. If the next meeting starts at or after that end time, that room is free — we pop (reusing it) before pushing the new meeting's end time. Otherwise we add a new room (push without popping). The heap size at any moment is the number of rooms in use; the maximum (equal to the final size if no pops happen at the end of the sweep) is the answer.

- **Time**: O(n log n) — sort is O(n log n); each meeting does O(log n) heap work.
- **Space**: O(n) for the heap.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Meeting Rooms** — can one person attend all meetings? Sort by start, check pairwise overlap. | https://leetcode.com/problems/meeting-rooms/ |
| Medium | **Meeting Rooms II** — the canonical min-heap problem above. | https://leetcode.com/problems/meeting-rooms-ii/ |
| Hard | **Employee Free Time** — given each employee's busy intervals, find the common free time; min-heap of merge-sort style. | https://leetcode.com/problems/employee-free-time/ |
