# Dijkstra's shortest path

## What is this

Dijkstra's algorithm computes single-source shortest paths in a weighted graph with non-negative edge weights. It maintains a tentative distance `dist[v]` for every vertex, repeatedly extracts the vertex with the smallest tentative distance, and relaxes its outgoing edges. With a binary heap it runs in O((V + E) log V).

It is a greedy algorithm: once a vertex is popped from the priority queue with its current `dist`, that distance is final. This correctness depends on non-negative edge weights; for graphs with negative edges, use Bellman-Ford instead.

## Why we use

- Finds shortest paths fast in weighted graphs with non-negative weights
- Drop-in upgrade over BFS when edges carry different costs
- Generalises to any metric where edges add up (latency, distance, fuel cost)
- Heap-based variant scales to graphs with millions of edges

## How to implement

```
dist[*] = +infinity
dist[source] = 0
push (0, source) into min-heap
while heap not empty:
    d, u = pop min
    if d > dist[u]: continue          # stale entry
    for (v, w) in adj[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            push (dist[v], v)
```

```python
import heapq

def dijkstra(graph: dict[int, list[tuple[int, int]]], source: int) -> dict[int, float]:
    dist: dict[int, float] = {u: float("inf") for u in graph}
    dist[source] = 0
    heap: list[tuple[float, int]] = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
```

Invariant: when `(d, u)` is popped and `d == dist[u]`, no shorter path to `u` exists, because all edge weights are non-negative and any alternative path through the heap can only add non-negative weight.

## Which problems this approach solves in the real world

- GPS / map routing with road segment travel times
- Network routing protocols (OSPF, IS-IS) where each link has a positive cost
- Game pathfinding on weighted terrain (mud slow, road fast)
- Latency-aware request routing across data centres
- Power-grid flow planning where transmission has positive impedance

## Pros and cons

**Pros**
- O((V + E) log V) with a binary heap — fast in practice
- Stops early if you only need distance to one target (priority-queue-based)
- Easy to extend with parent pointers for path reconstruction
- A* is a direct generalisation with a heuristic

**Cons**
- Wrong (silently) on graphs with negative edge weights
- Heap operations have constant overhead — flat arrays may beat it on tiny graphs
- Standard form does not handle real-time edge updates

## Limitations

- Negative weights break correctness (use Bellman-Ford)
- Multi-source variant requires careful initialization (push all sources with distance 0)
- All-pairs shortest paths via repeated Dijkstra is O(V * (V + E) log V) — Floyd-Warshall may be better on dense graphs

## One example

Problem: Given `n` nodes labelled `1..n`, a list of weighted directed edges `(u, v, w)`, and a starting node `k`, return the minimum time it takes for a signal to reach all nodes (or `-1` if some node is unreachable).

```
Input:  n = 4, k = 2
        edges = [(2, 1, 1), (2, 3, 1), (3, 4, 1)]
Output: 2     (distances from 2: {1: 1, 2: 0, 3: 1, 4: 2}, max = 2)
Constraints: 1 <= n <= 100, 1 <= len(edges) <= 6000, 1 <= w <= 100
```

## Solution explanation

```python
import heapq

def network_delay_time(times: list[tuple[int, int, int]], n: int, k: int) -> int:
    graph: dict[int, list[tuple[int, int]]] = {i: [] for i in range(1, n + 1)}
    for u, v, w in times:
        graph[u].append((v, w))
    INF = float("inf")
    dist = {i: INF for i in range(1, n + 1)}
    dist[k] = 0
    heap: list[tuple[float, int]] = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    longest = max(dist.values())
    return longest if longest != INF else -1
```

Run Dijkstra from `k` and return the longest finalized distance.

Walkthrough for `n = 4`, `k = 2`, `edges = [(2,1,1), (2,3,1), (3,4,1)]`:

| Step | Heap (after pop)       | Popped (d, u)    | Relaxations                              | dist                                |
|------|------------------------|------------------|------------------------------------------|-------------------------------------|
| init | [(0, 2)]               |                  |                                          | {1: inf, 2: 0, 3: inf, 4: inf}      |
| 1    | []                     | (0, 2)           | dist[1]=1 push (1,1); dist[3]=1 push (1,3) | {1: 1, 2: 0, 3: 1, 4: inf}        |
| 2    | [(1, 3)]               | (1, 1)           | no outgoing edges                        | {1: 1, 2: 0, 3: 1, 4: inf}          |
| 3    | []                     | (1, 3)           | dist[4]=2 push (2,4)                     | {1: 1, 2: 0, 3: 1, 4: 2}            |
| 4    | []                     | (2, 4)           | no outgoing edges                        | {1: 1, 2: 0, 3: 1, 4: 2}            |

Max finalized distance = 2. Time O((V + E) log V), space O(V + E).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Number of Islands (BFS warmup before Dijkstra) (LeetCode 200) | https://leetcode.com/problems/number-of-islands/ |
| Medium | Network Delay Time (LeetCode 743) | https://leetcode.com/problems/network-delay-time/ |
| Hard | Path with Minimum Effort (LeetCode 1631) | https://leetcode.com/problems/path-with-minimum-effort/ |
