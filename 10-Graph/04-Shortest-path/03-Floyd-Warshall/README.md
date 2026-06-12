# Floyd-Warshall (all-pairs shortest path)

## What is this

Floyd-Warshall computes the shortest distance between *every* pair of vertices in a weighted graph in O(V^3). The algorithm performs `V` rounds; in round `k`, it asks "can we improve `dist[i][j]` by going through intermediate vertex `k`?" — if yes, update.

It handles negative edge weights and detects negative cycles (a vertex with `dist[v][v] < 0` after the algorithm). It does not handle negative cycles in path reconstruction without further care.

## Why we use

- All-pairs shortest paths in one O(V^3) call.
- Handles negative edges (no Dijkstra restriction).
- Detects negative cycles via `dist[v][v] < 0`.
- Triple-loop is trivial to implement and parallelize.

## How to implement

```
dist = [[INF] * V for _ in V]
for v: dist[v][v] = 0
for (u, v, w) in edges: dist[u][v] = min(dist[u][v], w)
for k in 0..V-1:
    for i in 0..V-1:
        for j in 0..V-1:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

```python
def floyd_warshall(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for v in range(n):
        dist[v][v] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
    return dist
```

```python
def has_negative_cycle(dist):
    return any(dist[v][v] < 0 for v in range(len(dist)))
```

The outer `k` loop is the intermediate vertex — its position inside `i` and `j` would silently produce wrong answers, so order matters.

## Which problems this approach solves in the real world

- Pre-computing pairwise travel times in small city networks.
- Centrality / closeness scores in social-network analysis.
- Transitive closure (reachability) — set `dist` to boolean and replace `min, +` with `or, and`.
- Currency arbitrage detection (negative cycle in -log(rate) graph).
- Pairwise correlation chain computation in small fully-connected graphs.

## Pros and cons

**Pros**
- All-pairs in O(V^3) with O(V^2) memory.
- Handles negative edges (no Dijkstra restriction).
- Simple triple loop, trivially parallel.

**Cons**
- O(V^3) — prohibitive beyond ~500 vertices.
- O(V^2) memory.
- For sparse graphs, V * Dijkstra is faster (E V log V).

## Limitations

- Cannot scale to large sparse graphs.
- Memory cost dominates for V > a few thousand.
- Path reconstruction needs an additional `next[i][j]` matrix.

## One example

**Problem**: Given `n` cities labeled `0..n-1` and a list of edges `[u, v, w]` (bidirectional), and an integer `distanceThreshold`, return the city with the smallest number of cities reachable within the threshold. Tie-break by largest index.

**Input**: `n = 4`, `edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]]`, `distanceThreshold = 4`
**Output**: `3`
**Constraints**: `2 <= n <= 100`, `1 <= edges.length <= n*(n-1)/2`.

## Solution explanation

```python
def findTheCity(n, edges, distanceThreshold):
    INF = float('inf')
    d = [[INF] * n for _ in range(n)]
    for v in range(n):
        d[v][v] = 0
    for u, v, w in edges:
        d[u][v] = d[v][u] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    best_count, best_city = n + 1, -1
    for city in range(n):
        count = sum(1 for j in range(n) if j != city and d[city][j] <= distanceThreshold)
        if count <= best_count:
            best_count, best_city = count, city
    return best_city
```

Walkthrough on `n=4, edges=[[0,1,3],[1,2,1],[1,3,4],[2,3,1]]`:

Initial dist matrix (INF for non-edges, 0 on diagonal):
```
[0, 3, INF, INF]
[3, 0,  1,   4 ]
[INF,1, 0,   1 ]
[INF,4, 1,   0 ]
```
After k=0..3, final dist:
```
[0, 3, 4, 5]
[3, 0, 1, 2]
[4, 1, 0, 1]
[5, 2, 1, 0]
```
Reachable within 4: city 0 → {1,3 = 3, 4 — wait — count entries `<= 4 and != self`} actually: 0 sees {1:3, 2:4} (2 cities); 1 sees {0:3, 2:1, 3:2} (3); 2 sees {0:4, 1:1, 3:1} (3); 3 sees {1:2, 2:1} (2). Tie 0 and 3 with count 2; tie-break largest index → 3.

Time: O(V^3). Space: O(V^2).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find Center of Star Graph (LeetCode 1791) | https://leetcode.com/problems/find-center-of-star-graph/ |
| Medium | Find the City With the Smallest Number of Neighbors at a Threshold Distance (LeetCode 1334) | https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/ |
| Hard | Course Schedule IV (LeetCode 1462) | https://leetcode.com/problems/course-schedule-iv/ |
