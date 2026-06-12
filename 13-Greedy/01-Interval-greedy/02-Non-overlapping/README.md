# Non-overlapping Intervals

## What is this

The non-overlapping intervals pattern is a greedy technique that, given a set of intervals, picks the largest possible subset such that no two chosen intervals overlap. It is the dual of "minimum removals to make intervals non-overlapping" — once you know the maximum number you can keep, the rest must be removed.

The core insight is that if we sort intervals by their **end time**, then repeatedly accepting the interval that ends earliest leaves the maximum room for future intervals. Greedy by end-time is provably optimal because any interval we skip in favor of an earlier-ending one cannot extend later opportunities, and any earlier-ending interval we pick blocks no more than the one we would have picked.

## Why we use

- It produces an **optimal** solution to maximum non-overlapping selection in O(n log n), beating any DP-based approach.
- It generalises trivially: switch the sort key to "deadline" or "profit" and you cover whole families of scheduling problems.
- The bookkeeping is minimal — just one running variable `prev_end` — making it easy to reason about and to extend with weights or counts.
- It is the building block for "minimum number of conferences", "least arrows to burst balloons", and "non-overlapping segment scheduling".

## How to implement

```
sort intervals by end ascending
prev_end = -infinity
kept = 0
for [s, e] in intervals:
    if s >= prev_end:        # no overlap with last kept
        kept += 1
        prev_end = e
return kept                  # or n - kept  for removal count
```

```python
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])
    prev_end = float('-inf')
    kept = 0
    for s, e in intervals:
        if s >= prev_end:
            kept += 1
            prev_end = e
    return kept
```

```javascript
function maxNonOverlapping(intervals) {
    intervals.sort((a, b) => a[1] - b[1]);
    let prevEnd = -Infinity, kept = 0;
    for (const [s, e] of intervals) {
        if (s >= prevEnd) { kept++; prevEnd = e; }
    }
    return kept;
}
```

Invariant: after processing the i-th interval, `kept` is the size of the largest non-overlapping subset achievable using only intervals that end at or before `prev_end`.

## Which problems this approach solves in the real world

- Scheduling lectures into a single room without conflicts.
- Booking the maximum number of non-conflicting meetings on one resource.
- Choosing TV programmes to record on a single tuner.
- Placing the maximum number of non-overlapping ads in a time slot.
- Allocating runway slots to flights so the most flights land/take-off.
- Selecting the largest set of compatible tasks that share a machine.

## Pros and cons

**Pros**
- Optimal and provable in one pass after sort.
- O(n log n) time, O(1) extra space (besides the sort).
- Easy to adapt to "minimum removals" by returning `n - kept`.
- Extends to weighted variants by combining with DP when needed.

**Cons**
- Requires sorting — not suitable for hard streaming use cases.
- Sort by **end** (not start) is a common mistake.
- Equality handling (`s >= prev_end` vs `s > prev_end`) depends on whether endpoints are inclusive.
- The simple version assumes equal weights; weighted intervals need DP.

## Limitations

- Works only when intervals share a single resource; multi-resource needs heaps or graph coloring.
- Cannot directly handle priorities or preferences beyond endpoints.
- Closed vs half-open interval semantics must be agreed on with the caller.
- Adversarial inputs that all share a common endpoint defeat naive tie-breakers.

## One example

**Problem**: Given an array of intervals `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest non-overlapping. Treat `[1,2]` and `[2,3]` as non-overlapping.

Constraints: 1 <= n <= 10^5, -5*10^4 <= start, end <= 5*10^4.

**Input**: `intervals = [[1,2],[2,3],[3,4],[1,3]]`

**Output**: `1`

## Solution explanation

```python
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    prev_end = float('-inf')
    kept = 0
    for s, e in intervals:
        if s >= prev_end:
            kept += 1
            prev_end = e
    return len(intervals) - kept
```

Walk-through on the sorted list `[[1,2],[2,3],[1,3],[3,4]]`:

| Step | Interval | prev_end before | s >= prev_end? | Action | kept | prev_end after |
|------|----------|-----------------|----------------|--------|------|----------------|
| 1 | [1,2] | -inf | yes | keep | 1 | 2 |
| 2 | [2,3] | 2 | yes (2>=2) | keep | 2 | 3 |
| 3 | [1,3] | 3 | no (1<3) | skip | 2 | 3 |
| 4 | [3,4] | 3 | yes (3>=3) | keep | 3 | 4 |

We kept 3 intervals out of 4, so we removed `4 - 3 = 1`. Correctness: the greedy that keeps the earliest-ending compatible interval is optimal because swapping any kept interval for a later-ending alternative can never increase future options — a standard exchange argument.

- **Time**: O(n log n)
- **Space**: O(1) extra (in-place sort)

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Meeting Rooms | https://leetcode.com/problems/meeting-rooms/ |
| Medium | Non-overlapping Intervals | https://leetcode.com/problems/non-overlapping-intervals/ |
| Medium | Minimum Number of Arrows to Burst Balloons | https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/ |
