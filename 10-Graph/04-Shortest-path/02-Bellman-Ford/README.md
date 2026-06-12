# Bellman-Ford shortest path

## What is this

Bellman-Ford computes single-source shortest paths in a weighted directed graph that may contain negative edge weights. It relaxes every edge `V - 1` times: after `k` iterations the shortest path that uses at most `k` edges is known. A `V`-th relaxation that still decreases a distance proves the existence of a negative cycle reachable from the source.

It is slower than Dijkstra (O(V * E) vs O((V + E) log V)) but tolerates negative weights and can detect negative cycles, which Dijkstra cannot.

## Why we use

- Handles negative edge weights correctly
- Detects negative-weight cycles reachable from the source
- Simple to implement with just an edge list
- Foundation for distributed routing protocols (RIP, distance-vector)

## How to implement

```
dist[*] = +infinity
dist[source] = 0
for i in 0 .. V - 2:
    for each edge (u, v, w):
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
# negative-cycle check:
for each edge (u, v, w):
    if dist[u] + w < dist[v]:
        report negative cycle
```

```python
def bellman_ford(n: int, edges: list[tuple[int, int, int]], source: int) -> list[float] | None:
    INF = float("inf")
    dist = [INF] * n
    dist[source] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # negative cycle
    return dist
```

Invariant: after iteration `k`, `dist[v]` is at most the shortest-path cost from source to `v` using at most `k` edges. After `V - 1` iterations this equals the true shortest path (if no negative cycle exists), because any simple path uses at most `V - 1` edges.

## Which problems this approach solves in the real world

- Distance-vector routing protocols (RIP) where edge costs can change and links may go down
- Currency arbitrage detection: model exchange rates as `-log(rate)` and look for negative cycles
- Schedule feasibility when constraints include "task A must follow B by at most/least X time" (Bellman-Ford on a difference constraint graph)
- Detecting negative-feedback loops in financial transaction networks
- Path-finding in graphs where rewards (negative costs) are possible

## Pros and cons

**Pros**
- Works with negative weights
- Detects negative cycles
- Simple skeleton using just an edge list
- Naturally distributed (each node only needs its neighbours)

**Cons**
- O(V * E) is slow compared to Dijkstra for non-negative weights
- Does not give path reconstruction without parent pointers
- Sensitive to relaxation order — bad order makes it slow in practice (SPFA variant fixes this)

## Limitations

- Not suitable for very large graphs where Dijkstra suffices
- Cannot handle multi-source shortest paths efficiently in this raw form (use Floyd-Warshall or repeated runs)
- Negative cycle detection only catches cycles reachable from the source

## One example

Problem: Given `n` nodes and a list of directed weighted edges, return shortest distances from node `source` to every other node, or report a negative cycle.

```
Input:  n = 4
        edges = [(0, 1, 1), (1, 2, -1), (2, 3, -1), (3, 1, -1)]
        source = 0
Output: negative cycle detected (cycle 1 -> 2 -> 3 -> 1 has total weight -3)
Constraints: 1 <= n <= 1000, |w| <= 10^4
```

## Solution explanation

```python
def bellman_ford(n: int, edges: list[tuple[int, int, int]], source: int) -> list[float] | None:
    INF = float("inf")
    dist = [INF] * n
    dist[source] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None
    return dist
```

We relax all edges `n - 1` times, then one extra pass: if any relaxation still helps, a negative cycle is reachable.

Walkthrough for the input above. Edge order: `(0,1,1)`, `(1,2,-1)`, `(2,3,-1)`, `(3,1,-1)`.

| Iteration | dist[0] | dist[1] | dist[2] | dist[3] |
|-----------|---------|---------|---------|---------|
| init      | 0       | inf     | inf     | inf     |
| 1         | 0       | 1       | 0       | -1      |
| 2         | 0       | -2      | -3      | -4      |
| 3         | 0       | -5      | -6      | -7      |
| extra     | (still updates) -> negative cycle |

Time O(V * E), space O(V).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find the City With the Smallest Number of Neighbors at a Threshold Distance | https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/ |
| Medium | Cheapest Flights Within K Stops | https://leetcode.com/problems/cheapest-flights-within-k-stops/ |
| Hard | Currency Arbitrage Detection (negative cycle in -log rates) | Classic competitive problem |
