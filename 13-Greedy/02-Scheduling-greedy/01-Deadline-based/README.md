# Deadline-based scheduling

## What is this

Deadline-based scheduling chooses jobs with profits and integer deadlines so that each chosen job runs in some slot ≤ its deadline (one job per slot). Maximize total profit.

Greedy: sort jobs by profit descending; for each job try the latest still-empty slot ≤ its deadline. If found, schedule it there; else skip. Using a Union-Find "find next free slot ≤ d" makes the operation near-O(1) amortized; total O(n α(n)) after sorting.

Equivalent formulations: maximum-profit scheduling on unit-time jobs with deadlines, EDF-greedy with priority.

## Why we use

- Provably optimal (matroid exchange argument).
- O(n log n) sort + near-linear DSU "find next free slot".
- Cleanly separates "select job" from "find slot".
- Natural template for any "fit items into slots ≤ deadline" with priority.

## How to implement

```
sort jobs by profit desc
slots = DSU(max_deadline + 1)        # slot[d] = next available <= d
total = 0
for (profit, deadline) in jobs:
    free = slots.find(deadline)
    if free > 0:
        total += profit
        slots.union(free, free - 1)   # mark slot occupied, redirect to free-1
return total
```

```python
class DSU:
    def __init__(self, n):
        self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)

def deadline_schedule(jobs):
    """jobs: list of (profit, deadline). Maximize total profit."""
    jobs.sort(key=lambda j: -j[0])
    max_d = max(j[1] for j in jobs)
    dsu = DSU(max_d + 1)
    total = 0
    for profit, d in jobs:
        free = dsu.find(d)
        if free > 0:
            total += profit
            dsu.union(free, free - 1)
    return total
```

```python
import heapq

def deadline_schedule_heap(jobs):
    """Alternative heap-based: sort by deadline asc; maintain min-heap of accepted profits."""
    jobs.sort(key=lambda j: j[1])
    heap = []          # min-heap of accepted profits
    for profit, d in jobs:
        if len(heap) < d:
            heapq.heappush(heap, profit)
        elif heap and heap[0] < profit:
            heapq.heapreplace(heap, profit)
    return sum(heap)
```

DSU version is the canonical "Union-Find slot allocation" trick; heap version trades a logarithmic factor for simpler code.

## Which problems this approach solves in the real world

- Deadline-aware job-shop revenue maximization.
- Project portfolio selection with hard deadlines.
- Ad-impression scheduling with daily deadlines per advertiser.
- Conference talk scheduling under time-slot constraints.
- Course registration with overlapping deadlines.

## Pros and cons

**Pros**
- Provably optimal greedy.
- DSU version near-linear.
- Heap version is O(n log n) and simpler.

**Cons**
- DSU code is verbose for a small concept.
- Doesn't extend to variable-duration jobs without DP.
- Requires integer deadlines.

## Limitations

- Multi-machine variants need different techniques.
- Continuous deadlines don't fit the slot model.
- Cannot model dependencies between jobs.

## One example

**Problem**: Given jobs, each with `(profit, deadline)`. Each job takes 1 time unit. At each time slot you can run one job. A job can only be done if `deadline >= time when run + 1`. Maximize total profit.

**Input**: `jobs = [(20, 2), (15, 2), (10, 1), (5, 3), (1, 3)]`
**Output**: `40`  (do job1 in slot 2, job2 in slot 1, job4 in slot 3 — wait check)
**Constraints**: `1 <= n <= 10^4`.

## Solution explanation

```python
def maxProfit(jobs):
    jobs.sort(key=lambda j: -j[0])
    max_d = max(j[1] for j in jobs)
    dsu = DSU(max_d + 1)
    total = 0
    for profit, d in jobs:
        free = dsu.find(d)
        if free > 0:
            total += profit
            dsu.union(free, free - 1)
    return total
```

Walkthrough on `jobs = [(20, 2), (15, 2), (10, 1), (5, 3), (1, 3)]` after sort by profit desc:

| job (p, d) | dsu.find(d) | accept? | total | union(free, free-1) |
|------------|-------------|---------|-------|----------------------|
| (20, 2)    | 2           | yes     | 20    | parent[2] = 1        |
| (15, 2)    | 1           | yes     | 35    | parent[1] = 0        |
| (10, 1)    | 0           | no      | 35    | -                    |
| (5, 3)     | 3           | yes     | 40    | parent[3] = 2 → find(2)=0 next |
| (1, 3)     | 0           | no      | 40    | -                    |

Return 40. Time: O(n log n). Space: O(max_d).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Two City Scheduling (LeetCode 1029) | https://leetcode.com/problems/two-city-scheduling/ |
| Medium | Course Schedule III (LeetCode 630) | https://leetcode.com/problems/course-schedule-iii/ |
| Hard | Maximum Profit in Job Scheduling (LeetCode 1235) | https://leetcode.com/problems/maximum-profit-in-job-scheduling/ |
