# 0-1 BFS

## What is this

0-1 BFS finds shortest paths in a graph whose edge weights are only **0 or 1**, in O(V + E) — beating Dijkstra's O((V + E) log V). The trick is to use a **deque** instead of a priority queue: when relaxing an edge of weight 0, push the neighbor to the **front**; for weight 1, push to the **back**. This preserves the BFS-like invariant that the deque is always sorted by distance.

It is the right algorithm for grids with "free" and "paid" steps, two-cost network problems, and shortest-path-with-flips problems.

## Why we use

- O(V + E) instead of Dijkstra's O((V + E) log V) on 0/1 graphs.
- Deque ops are O(1) — much smaller constant than heap.
- Same invariant proof as classic BFS.
- Naturally generalizes from BFS (all 1s) to 0-1.

## How to implement

```
dist = [INF] * V
dist[src] = 0
dq = deque([src])
while dq:
    u = dq.popleft()
    for v, w in adj[u]:           # w in {0, 1}
        nd = dist[u] + w
        if nd < dist[v]:
            dist[v] = nd
            if w == 0: dq.appendleft(v)
            else:      dq.append(v)
```

```python
from collections import deque

def zero_one_bfs(n, adj, src):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist
```

```python
def min_flip_cost(grid):
    """Each cell has a direction arrow; cost to traverse = 0 if you follow the arrow, 1 if you flip it."""
    rows, cols = len(grid), len(grid[0])
    DIR = {1:(0,1), 2:(0,-1), 3:(1,0), 4:(-1,0)}
    INF = float('inf')
    dist = [[INF]*cols for _ in range(rows)]
    dist[0][0] = 0
    dq = deque([(0, 0)])
    while dq:
        r, c = dq.popleft()
        for k, (dr, dc) in DIR.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                w = 0 if grid[r][c] == k else 1
                if dist[r][c] + w < dist[nr][nc]:
                    dist[nr][nc] = dist[r][c] + w
                    if w == 0: dq.appendleft((nr, nc))
                    else:      dq.append((nr, nc))
    return dist[-1][-1]
```

Allow the same vertex to be popped multiple times — outdated entries are filtered by the `nd < dist[v]` check.

## Which problems this approach solves in the real world

- Routing with toll roads (0 = free, 1 = paid).
- Minimum-cost direction flipping in grids / mazes.
- Edge-disjoint-path approximations on 0-1 weighted networks.
- Pathfinding with mandatory vs optional moves.
- Approximate shortest paths in transportation networks with two cost classes.

## Pros and cons

**Pros**
- O(V + E) — strictly better than Dijkstra on 0/1 graphs.
- Smaller constant factor (deque vs heap).
- Same correctness proof as BFS.

**Cons**
- Only works for edges with weights 0 or 1.
- Stale deque entries inflate the queue size.
- Hard to extend to {0, 1, 2} — that needs Dijkstra.

## Limitations

- Arbitrary integer weights require Dijkstra or general SSSP.
- Negative edges break the invariant.
- 0-1 BFS on dense graphs still touches every edge.

## One example

**Problem**: Given a 2D grid `grid` where each cell holds an arrow direction `1..4`, you start at (0,0) and must reach (m-1, n-1). Following an arrow costs 0, flipping it costs 1. Return the minimum total cost.

**Input**: `grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]`
**Output**: `3`
**Constraints**: `1 <= m, n <= 100`.

## Solution explanation

`min_flip_cost` above. Walkthrough on the input:

| step | popped (r,c) | dist[(r,c)] | new pushes (front/back) |
|------|--------------|-------------|--------------------------|
| 1    | (0, 0)       | 0           | (0,1) w=0 front; (1,0) w=1 back |
| 2    | (0, 1)       | 0           | (0,2) w=0 front; (1,1) w=1 back |
| 3    | (0, 2)       | 0           | (0,3) w=0 front; (1,2) w=1 back |
| 4    | (0, 3)       | 0           | (1,3) w=1 back            |
| 5    | (1, 0)       | 1           | (1,-1)? invalid; (2,0) w=0 front; (0,0) already 0 |
| 6    | (2, 0)       | 1           | (2,1) w=0 front; (3,0) w=1 back |
| ... continue until (3,3) reached at cost 3 |

Return 3. Time: O(m*n). Space: O(m*n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Number of Islands (LeetCode 200) | https://leetcode.com/problems/number-of-islands/ |
| Medium | Shortest Path in Binary Matrix (LeetCode 1091) | https://leetcode.com/problems/shortest-path-in-binary-matrix/ |
| Hard | Minimum Cost to Make at Least One Valid Path in a Grid (LeetCode 1368) | https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/ |
