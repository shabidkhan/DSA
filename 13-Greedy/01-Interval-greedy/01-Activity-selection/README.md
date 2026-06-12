# Activity selection

## What is this

The Activity Selection Problem asks: given `n` activities each with a start time and an end time, pick the maximum-size set of pairwise non-overlapping activities. The optimal greedy strategy is to sort activities by end time and repeatedly pick the next activity whose start is at least the previously picked activity's end.

It is a textbook example of a greedy algorithm whose optimality is provable by an exchange argument: replacing any chosen activity with the next-earliest-ending compatible one cannot reduce the total count.

## Why we use

- O(n log n) solution to a problem that appears combinatorial
- Easy proof of optimality (exchange / cut-and-paste argument)
- Foundation for many scheduling and interval-graph problems
- Linear sweep after sorting — minimal memory

## How to implement

```
sort activities by end time
last_end = -infinity
count = 0
for (s, e) in activities:
    if s >= last_end:
        count += 1
        last_end = e
return count
```

```python
def activity_selection(activities: list[tuple[int, int]]) -> int:
    activities.sort(key=lambda a: a[1])
    last_end = float("-inf")
    count = 0
    for s, e in activities:
        if s >= last_end:
            count += 1
            last_end = e
    return count
```

Returning the actual selected activities:

```python
def select_activities(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    activities.sort(key=lambda a: a[1])
    chosen: list[tuple[int, int]] = []
    last_end = float("-inf")
    for s, e in activities:
        if s >= last_end:
            chosen.append((s, e))
            last_end = e
    return chosen
```

Invariant: after iterating to index `i`, `chosen` is the largest compatible subset of `activities[:i+1]` whose last activity ends earliest among all such subsets.

## Which problems this approach solves in the real world

- Conference-room booking: pack the most non-overlapping meetings into one room
- CPU job scheduling when each job has a fixed (start, finish) and the CPU runs one at a time
- TV ad-slot selection: fit the most non-overlapping ads in a time block
- Lecture hall assignment to maximise classes per room
- Resource leasing: maximise number of rentals with fixed start/finish times

## Pros and cons

**Pros**
- O(n log n) sort + O(n) scan
- Optimal by an easy exchange argument
- Pure greedy — no DP table needed

**Cons**
- Maximises *count*, not weighted reward — for that use weighted interval scheduling (DP)
- Sensitive to tie-breaking on equal end times in some variants
- Greedy intuition does not transfer to multi-resource versions (NP-hard)

## Limitations

- Cannot handle weights on activities (use DP on intervals)
- Cannot handle multiple parallel resources (multi-machine scheduling is NP-hard in general)
- Online streaming variant requires different approach (competitive ratios)

## One example

Problem: You are given `n` activities with `(start[i], end[i])`. Return the maximum number of activities you can perform in a single day if no two can overlap (sharing an endpoint is allowed).

```
Input:  activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
Output: 4    (e.g. (1,4), (5,7), (8,11), (12,16))
Constraints: 1 <= n <= 10^5, 0 <= start[i] < end[i] <= 10^9
```

## Solution explanation

```python
def activity_selection(activities: list[tuple[int, int]]) -> int:
    activities.sort(key=lambda a: a[1])
    last_end = float("-inf")
    count = 0
    for s, e in activities:
        if s >= last_end:
            count += 1
            last_end = e
    return count
```

Sort by end time, then sweep. Each pick is the earliest-finishing activity compatible with everything previously chosen — by exchange argument this is optimal.

Walkthrough for the input above. After sort by end time:

`[(1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16)]`

| Activity | last_end before | s >= last_end? | last_end after | count |
|----------|-----------------|-----------------|----------------|-------|
| (1, 4)   | -inf            | yes             | 4              | 1     |
| (3, 5)   | 4               | no              | 4              | 1     |
| (0, 6)   | 4               | no              | 4              | 1     |
| (5, 7)   | 4               | yes             | 7              | 2     |
| (3, 9)   | 7               | no              | 7              | 2     |
| (5, 9)   | 7               | no              | 7              | 2     |
| (6, 10)  | 7               | no              | 7              | 2     |
| (8, 11)  | 7               | yes             | 11             | 3     |
| (8, 12)  | 11              | no              | 11             | 3     |
| (2, 14)  | 11              | no              | 11             | 3     |
| (12, 16) | 11              | yes             | 16             | 4     |

Final count = 4. Time O(n log n), space O(1) extra.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Maximum Units on a Truck (LeetCode 1710) | https://leetcode.com/problems/maximum-units-on-a-truck/ |
| Medium | Non-overlapping Intervals (LeetCode 435) | https://leetcode.com/problems/non-overlapping-intervals/ |
| Hard | Maximum Number of Events That Can Be Attended II (LeetCode 1751) | https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/ |
