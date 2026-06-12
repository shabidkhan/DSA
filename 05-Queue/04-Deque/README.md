# Deque-based patterns

## What is this

A deque (double-ended queue) supports O(1) insertion and removal at *both* ends. Python's `collections.deque` is a doubly-linked block list with `append`, `appendleft`, `pop`, `popleft`, all O(1).

The signature pattern is the *monotonic deque*: maintain a deque whose values are strictly increasing (or decreasing) from front to back; pop the back while the new element violates monotonicity, then push. Combined with a sliding window, this gives O(n) algorithms for "max of every window of size k", "shortest subarray with sum >= K", and Dijkstra-on-0/1 weights.

## Why we use

- O(1) at both ends — sliding windows, undo / redo stacks.
- Monotonic deques deliver O(n) sliding-window max/min.
- Bidirectional iteration without copying.
- Underlies 0-1 BFS for graphs with 0/1 edge weights.

## How to implement (monotonic deque for window max)

```
dq = deque()
for i, x in enumerate(arr):
    while dq and dq[0] <= i - k: dq.popleft()  # drop out-of-window
    while dq and arr[dq[-1]] <= x: dq.pop()    # drop dominated
    dq.append(i)
    if i >= k - 1: emit(arr[dq[0]])
```

```python
from collections import deque

def max_sliding_window(nums, k):
    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

```python
def zero_one_bfs(adj, src):
    INF = float('inf')
    dist = [INF] * len(adj)
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0: dq.appendleft(v)
                else:      dq.append(v)
    return dist
```

The invariant for window max: deque stores *indices* whose corresponding values are monotonically decreasing.

## Which problems this approach solves in the real world

- Real-time max / min over a sliding telemetry window.
- Tactical undo / redo stacks where both ends matter.
- 0-1 BFS in pathfinding with shortcuts and full-cost edges.
- Buffered stream processing with peek-both-ends.
- Concurrent work-stealing schedulers (deque per worker).

## Pros and cons

**Pros**
- O(1) at both ends — best of stack and queue.
- Monotonic deque reduces O(nk) brute force to O(n).
- Built-in `deque` is efficient and idiomatic.

**Cons**
- Indexing into a deque is O(n), not O(1) like an array.
- Monotonic deque invariants are subtle to get right.
- Higher per-node overhead than an array (linked blocks).

## Limitations

- Random access is poor — use lists if you need indexing.
- Memory overhead per element exceeds plain arrays.
- Not thread-safe; `queue.Queue` is the locked variant.

## One example

**Problem**: Given an integer array `nums` and an integer `k`, return the maximum of each sliding window of size `k`.

**Input**: `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`
**Output**: `[3, 3, 5, 5, 6, 7]`
**Constraints**: `1 <= n <= 10^5`, `1 <= k <= n`.

## Solution explanation

```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

Walkthrough on the input, k=3:

| i | x  | dq (indices) before | after expiry | after pop dominated | after push | window output |
|---|----|--------------------|--------------|---------------------|------------|---------------|
| 0 | 1  | []                 | []           | []                  | [0]        | -             |
| 1 | 3  | [0]                | [0]          | [] (1>0:1)          | [1]        | -             |
| 2 | -1 | [1]                | [1]          | [1]                 | [1,2]      | 3             |
| 3 | -3 | [1,2]              | [1,2]        | [1,2]               | [1,2,3]    | 3             |
| 4 | 5  | [1,2,3]            | [2,3]        | [] (all<5)          | [4]        | 5             |
| 5 | 3  | [4]                | [4]          | [4]                 | [4,5]      | 5             |
| 6 | 6  | [4,5]              | [4,5]        | [] (all<6)          | [6]        | 6             |
| 7 | 7  | [6]                | [6]          | [] (6<7)            | [7]        | 7             |

Time: O(n), each index pushed and popped at most once. Space: O(k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Number of Recent Calls (LeetCode 933) | https://leetcode.com/problems/number-of-recent-calls/ |
| Medium | Sliding Window Maximum (LeetCode 239) | https://leetcode.com/problems/sliding-window-maximum/ |
| Hard | Shortest Subarray with Sum at Least K (LeetCode 862) | https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/ |
