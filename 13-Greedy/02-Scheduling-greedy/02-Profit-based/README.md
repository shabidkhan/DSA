# Profit-based scheduling

## What is this

Profit-based scheduling chooses a subset of jobs (each with a profit and constraints like deadline or start/end times) to maximize total profit. When jobs cannot overlap and have variable durations, sort by end time and use DP-with-binary-search to find the most recent compatible job — a classic "weighted interval scheduling" technique.

The pattern: sort by end time, then `dp[i] = max(dp[i-1], profit[i] + dp[p(i)])` where `p(i)` is the largest index whose end ≤ start[i]. Binary search makes the lookup O(log n).

## Why we use

- O(n log n) optimal solution to weighted interval scheduling.
- DP + binary search cleanly handles per-job profit.
- Generalizes to job scheduling with deadlines, intervals with weights, asset allocation.
- The technique transfers to many "pick non-overlapping with max value" problems.

## How to implement

```
sort jobs by end time
ends = [e for (s, e, p) in jobs]
dp[i] = max profit considering first i+1 jobs
dp[0] = jobs[0].profit
for i in 1..n-1:
    incl = jobs[i].profit + dp[p(i)]   # p(i) via binary search on ends
    excl = dp[i - 1]
    dp[i] = max(incl, excl)
return dp[n-1]
```

```python
from bisect import bisect_right

def max_profit_scheduling(jobs):
    """jobs: list of (start, end, profit) sorted by end."""
    jobs = sorted(jobs, key=lambda j: j[1])
    n = len(jobs)
    ends = [j[1] for j in jobs]
    dp = [0] * n
    dp[0] = jobs[0][2]
    for i in range(1, n):
        # find rightmost job whose end <= jobs[i].start
        s_i = jobs[i][0]
        idx = bisect_right(ends, s_i) - 1
        incl = jobs[i][2] + (dp[idx] if idx >= 0 else 0)
        excl = dp[i - 1]
        dp[i] = max(incl, excl)
    return dp[-1]
```

```python
def job_scheduling(startTime, endTime, profit):
    jobs = sorted(zip(startTime, endTime, profit), key=lambda j: j[1])
    ends = [j[1] for j in jobs]
    dp = [0] * len(jobs)
    dp[0] = jobs[0][2]
    for i in range(1, len(jobs)):
        s = jobs[i][0]
        idx = bisect_right(ends, s) - 1
        incl = jobs[i][2] + (dp[idx] if idx >= 0 else 0)
        dp[i] = max(dp[i - 1], incl)
    return dp[-1]
```

Sorting by *end* time (not start) is critical — it lets binary search find the latest compatible predecessor.

## Which problems this approach solves in the real world

- Job-shop scheduling for revenue maximization.
- Conference-talk selection under non-overlap with revenue per talk.
- Ad-slot revenue maximization across an exclusive time window.
- Reservation system maximizing utilization-weighted profit.
- Selecting non-overlapping investments with different yields.

## Pros and cons

**Pros**
- O(n log n) — strong DP + binary search combination.
- Optimal for weighted interval scheduling.
- Easy to extend to other "non-overlap + max value" objectives.

**Cons**
- Sorting by end time, not start, is the most common mistake.
- DP state per job is O(1); reconstruction needs backpointers.
- Doesn't handle preemption / partial selection.

## Limitations

- Cannot model multi-resource constraints.
- Streaming variant needs online sorted structure.
- Floats / fractional profits work but compare carefully.

## One example

**Problem**: You're given `n` jobs, each with `startTime[i]`, `endTime[i]`, `profit[i]`. You can do any subset of jobs that don't overlap in time. Return the maximum profit.

**Input**: `startTime = [1, 2, 3, 3]`, `endTime = [3, 4, 5, 6]`, `profit = [50, 10, 40, 70]`
**Output**: `120`
**Constraints**: `1 <= n <= 5 * 10^4`.

## Solution explanation

```python
from bisect import bisect_right

def jobScheduling(startTime, endTime, profit):
    jobs = sorted(zip(startTime, endTime, profit), key=lambda j: j[1])
    ends = [j[1] for j in jobs]
    dp = [0] * len(jobs)
    dp[0] = jobs[0][2]
    for i in range(1, len(jobs)):
        s = jobs[i][0]
        idx = bisect_right(ends, s) - 1
        incl = jobs[i][2] + (dp[idx] if idx >= 0 else 0)
        dp[i] = max(dp[i - 1], incl)
    return dp[-1]
```

Walkthrough — after sort by end: `[(1,3,50), (2,4,10), (3,5,40), (3,6,70)]`, ends = `[3, 4, 5, 6]`.

| i | job (s,e,p) | bisect_right(ends, s) - 1 | incl              | excl | dp[i] |
|---|-------------|----------------------------|-------------------|------|-------|
| 0 | (1,3,50)    | -                          | 50                | -    | 50    |
| 1 | (2,4,10)    | bisect(3,4,5,6 right of 2) - 1 = -1 | 10 + 0 = 10 | 50 | 50 |
| 2 | (3,5,40)    | bisect(ends, 3) - 1 = 0    | 40 + dp[0] = 90   | 50   | 90    |
| 3 | (3,6,70)    | bisect(ends, 3) - 1 = 0    | 70 + dp[0] = 120  | 90   | 120   |

Return 120. Time: O(n log n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Non-overlapping Intervals (LeetCode 435) | https://leetcode.com/problems/non-overlapping-intervals/ |
| Medium | Maximum Profit in Job Scheduling (LeetCode 1235) | https://leetcode.com/problems/maximum-profit-in-job-scheduling/ |
| Hard | Maximum Number of Events That Can Be Attended II (LeetCode 1751) | https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/ |
