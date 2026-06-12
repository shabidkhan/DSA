# Task scheduler (heap)

## What is this

Given a list of tasks (each identified by a letter) and a cooldown period `n` between two identical tasks, schedule all tasks in the minimum number of time units. Idle slots may be inserted. The greedy heap-based approach: always run the task with the highest remaining count; "cool down" the just-run task by parking it in a waiting queue until `n + 1` time units pass; then return it to the heap.

The structure: a max-heap of remaining counts plus a FIFO of `(release_time, count)` for cooling tasks.

## Why we use

- O((n + k) log k) where k is unique task count — fast enough for 10^4 tasks.
- Greedy "always run most-frequent eligible task" provably minimizes idles.
- Heap + queue cleanly separates "ready" from "cooling".
- Generalizes to scheduling with different cooldown per task type.

## How to implement

```
heap = max-heap of -counts
wait = deque of (release_time, count_remaining)
time = 0
while heap or wait:
    time += 1
    if heap:
        c = -heappop(heap)
        if c - 1 > 0:
            wait.append((time + n, c - 1))
    if wait and wait[0][0] == time:
        _, c = wait.popleft()
        heappush(heap, -c)
return time
```

```python
import heapq
from collections import Counter, deque

def least_interval(tasks, n):
    counts = Counter(tasks)
    heap = [-c for c in counts.values()]
    heapq.heapify(heap)
    wait = deque()
    time = 0
    while heap or wait:
        time += 1
        if heap:
            c = -heapq.heappop(heap)
            if c - 1 > 0:
                wait.append((time + n, c - 1))
        if wait and wait[0][0] == time:
            _, c = wait.popleft()
            heapq.heappush(heap, -c)
    return time
```

```python
def least_interval_formula(tasks, n):
    counts = Counter(tasks).values()
    max_c = max(counts)
    n_max = sum(c == max_c for c in counts)
    return max(len(tasks), (max_c - 1) * (n + 1) + n_max)
```

The closed-form is a tighter analysis: maximum count rules, ties broken by count of equally-frequent tasks.

## Which problems this approach solves in the real world

- CPU scheduling with cooldown between same-task executions.
- Robotics: serializing arm movements with cooldown for actuator wear.
- Distributed-systems rate limiting per-key with global cooldown.
- Reorganizing notification sends so no user receives back-to-back pings.
- Job scheduling around tool maintenance windows.

## Pros and cons

**Pros**
- O((n + k) log k) heap-based solution.
- Closed-form O(n) for the canonical "same cooldown" variant.
- Greedy structure is provably optimal.

**Cons**
- Heap + queue bookkeeping is verbose vs the formula.
- Variant constraints (different cooldown per task) break the closed form.
- Idle slots count toward total time — must be accounted for explicitly.

## Limitations

- Cannot directly model deadlines per task.
- Streaming variant needs continuous re-ranking.
- Tied counts produce many equivalent schedules — picking any is fine.

## One example

**Problem**: Given a character array `tasks` representing tasks and an integer `n` representing the cooldown between two same tasks, return the least number of units of time needed to finish all tasks.

**Input**: `tasks = ["A","A","A","B","B","B"]`, `n = 2`
**Output**: `8`  (one valid schedule: A B idle A B idle A B)
**Constraints**: `1 <= tasks.length <= 10^4`, `0 <= n <= 100`.

## Solution explanation

```python
import heapq
from collections import Counter, deque

def leastInterval(tasks, n):
    counts = Counter(tasks)
    heap = [-c for c in counts.values()]
    heapq.heapify(heap)
    wait = deque()
    time = 0
    while heap or wait:
        time += 1
        if heap:
            c = -heapq.heappop(heap)
            if c - 1 > 0:
                wait.append((time + n, c - 1))
        if wait and wait[0][0] == time:
            _, c = wait.popleft()
            heapq.heappush(heap, -c)
    return time
```

Walkthrough on `tasks = ["A","A","A","B","B","B"]`, n=2:

| time | heap before | wait before | task run | wait after release |
|------|-------------|-------------|----------|--------------------|
| 1    | [-3, -3]    | []          | A (3→2)  | [(3,2)]            |
| 2    | [-3]        | [(3,2)]     | B (3→2)  | [(3,2),(4,2)]      |
| 3    | []          | [(3,2),(4,2)] | idle  | heap=[-2]          |
| 4    | [-2]        | [(4,2)]     | A (2→1)  | wait=[(6,1)]; heap=[-2] |
| 5    | [-2]        | [(6,1)]     | B (2→1)  | wait=[(6,1),(7,1)] |
| 6    | []          | [(6,1),(7,1)] | idle (heap empty) | heap=[-1] |
| 7    | [-1]        | [(7,1)]     | A (1→done) | heap=[-1]        |
| 8    | [-1]        | []          | B (1→done) | done             |

Return 8. Time: O(N log k). Space: O(k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Last Stone Weight (LeetCode 1046) | https://leetcode.com/problems/last-stone-weight/ |
| Medium | Task Scheduler (LeetCode 621) | https://leetcode.com/problems/task-scheduler/ |
| Hard | Reorganize String (LeetCode 767) | https://leetcode.com/problems/reorganize-string/ |
