# Minimum Removals to Eliminate Overlaps

## What is this

Minimum Removals is the complementary view of the activity-selection greedy. Instead of asking "what is the largest set of compatible intervals?", we ask "what is the smallest set we must delete so the remainder is non-overlapping?". The answer is always `n - max_non_overlapping`, but framing the problem in removal terms changes the questions you can answer: cost-of-deletion, priority of removal, and survival of must-keep intervals.

The algorithm still sorts by end time and walks left-to-right, but now we explicitly **count what we discard** at every conflict, and we drop the interval that *ends later* — because keeping the one that ends earlier preserves room for future intervals. When the problem has weights or fixed-keep markers, the count becomes a sum of weights of removed items.

## Why we use

- It re-frames scheduling as a deletion-cost problem, which is more natural when each removal carries a penalty or rebooking cost.
- It generalises directly to weighted removal: minimise the total weight of dropped intervals.
- The greedy gives the same optimal answer as activity selection but exposes the conflict points, useful for explaining "why this one was removed".
- It is the canonical pattern for "minimum deletions" / "minimum cancellations" / "minimum reschedules" interview phrasings.

## How to implement

```
sort intervals by end ascending
prev_end = -infinity
removed = 0
for [s, e] in intervals:
    if s < prev_end:         # overlaps with last kept
        removed += 1         # drop this one (later end)
    else:
        prev_end = e         # keep this one
return removed
```

```python
def min_removals(intervals):
    intervals.sort(key=lambda x: x[1])
    prev_end = float('-inf')
    removed = 0
    for s, e in intervals:
        if s < prev_end:
            removed += 1
        else:
            prev_end = e
    return removed
```

```javascript
function minRemovals(intervals) {
    intervals.sort((a, b) => a[1] - b[1]);
    let prevEnd = -Infinity, removed = 0;
    for (const [s, e] of intervals) {
        if (s < prevEnd) removed++;
        else prevEnd = e;
    }
    return removed;
}
```

Invariant: at every conflict we discard the **later-ending** interval, which is the current `(s, e)` because the kept set is sorted-by-end-asc and `prev_end <= e`.

## Which problems this approach solves in the real world

- Cancelling the fewest flights so all remaining flights fit a single runway window.
- Removing the fewest sponsored time slots so a TV schedule has no clashes.
- Dropping the fewest reservations to clear a single-machine factory line.
- Trimming the minimum overlapping highlight clips when producing a non-overlap reel.
- Reducing the fewest course timetable conflicts for a single classroom.
- Pruning the smallest set of operations so concurrent locks become serializable.

## Pros and cons

**Pros**
- Same O(n log n) cost as activity selection but answers the deletion question directly.
- A single counter — no auxiliary structures.
- Plays well with weighted variants by replacing `removed += 1` with `removed += weight`.
- Easy to log *which* intervals were dropped (audit trail).

**Cons**
- Naive port to weighted intervals is no longer optimal; you need DP for general weights.
- Endpoint inclusivity (`<` vs `<=`) must match the problem statement.
- Does not by itself respect "fixed keep" intervals — those need a custom comparator.
- For multi-resource scheduling, this single-track greedy is insufficient.

## Limitations

- Single-track only — multi-room scheduling requires `k` parallel tracks (use a heap).
- Cannot honor priority/importance without a comparator change.
- Assumes intervals are static; with arrivals over time, switch to streaming heuristics.
- Floating-point endpoints risk equality edge cases; prefer integer tick representations.

## One example

**Problem**: Given an array `intervals` where `intervals[i] = [start_i, end_i]`, return the **minimum number of intervals you must remove** so that the rest are non-overlapping (touching is allowed: `[1,2]` and `[2,3]` are fine).

Constraints: 1 <= n <= 10^5; -5*10^4 <= start < end <= 5*10^4.

**Input**: `intervals = [[1,100],[11,22],[1,11],[2,12]]`

**Output**: `2`

## Solution explanation

```python
def min_removals(intervals):
    intervals.sort(key=lambda x: x[1])
    prev_end = float('-inf')
    removed = 0
    for s, e in intervals:
        if s < prev_end:
            removed += 1
        else:
            prev_end = e
    return removed
```

After sorting by end: `[[1,11],[2,12],[11,22],[1,100]]`. Walk-through:

| Step | Interval | prev_end before | Decision | removed | prev_end after |
|------|----------|-----------------|----------|---------|----------------|
| 1 | [1,11] | -inf | keep | 0 | 11 |
| 2 | [2,12] | 11 | overlap (2<11) → drop | 1 | 11 |
| 3 | [11,22] | 11 | keep (11>=11) | 1 | 22 |
| 4 | [1,100] | 22 | overlap (1<22) → drop | 2 | 22 |

Two removals leave `[[1,11],[11,22]]`, which are mutually non-overlapping. The exchange argument: at every conflict, dropping the later-ending interval is no worse than any alternative because keeping the earlier-ending one preserves at least as much future capacity.

- **Time**: O(n log n)
- **Space**: O(1) extra

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Meeting Rooms | https://leetcode.com/problems/meeting-rooms/ |
| Medium | Non-overlapping Intervals | https://leetcode.com/problems/non-overlapping-intervals/ |
| Hard | Course Schedule III | https://leetcode.com/problems/course-schedule-iii/ |
