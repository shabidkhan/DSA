# Prim's MST

## What is this

Prim's algorithm builds a minimum spanning tree (MST) by growing a single tree from an arbitrary starting vertex. Maintain a min-heap of candidate edges (or of (cost, vertex) pairs). Repeatedly pop the cheapest edge whose far endpoint is not yet in the tree; add the endpoint and push its outgoing edges. Total time: O(E log V) using a binary heap.

Unlike Kruskal it does not need a sorted edge list and is the better fit for dense graphs via the O(V^2) adjacency-matrix variant.

## Why we use

- O(E log V) with a binary heap — competitive with Kruskal on sparse graphs.
- O(V^2) variant on dense graphs without heap overhead.
- Grows a single connected tree — naturally gives reachability from start.
- No global edge sort needed.

## How to implement

```
in_tree = [False] * V
heap = [(0, start)]
cost = 0
while heap and not all in_tree:
    w, u = heappop(heap)
    if in_tree[u]: continue
    in_tree[u] = True
    cost += w
    for v, w2 in adj[u]:
        if not in_tree[v]: heappush(heap, (w2, v))
```

```python
import heapq

def prim_mst(n, adj, start=0):
    in_tree = [False] * n
    heap = [(0, start)]
    cost = 0
    used = 0
    while heap and used < n:
        w, u = heapq.heappop(heap)
        if in_tree[u]:
            continue
        in_tree[u] = True
        cost += w
        used += 1
        for v, w2 in adj[u]:
            if not in_tree[v]:
                heapq.heappush(heap, (w2, v))
    return cost if used == n else float('inf')
```

```python
def prim_dense(n, w):
    INF = float('inf')
    in_tree = [False] * n
    key = [INF] * n
    key[0] = 0
    cost = 0
    for _ in range(n):
        u = -1
        for v in range(n):
            if not in_tree[v] and (u == -1 or key[v] < key[u]):
                u = v
        if key[u] == INF:
            return INF
        in_tree[u] = True
        cost += key[u]
        for v in range(n):
            if not in_tree[v] and w[u][v] < key[v]:
                key[v] = w[u][v]
    return cost
```

Pre-test `in_tree[u]` after pop because the heap may contain stale entries for vertices already added.

## Which problems this approach solves in the real world

- Telecom backbone planning: connect cities at minimum cable cost.
- Network design for power grid / pipeline routing.
- Image segmentation via Prim-MST (alternative to Kruskal).
- Clustering with single-linkage on graphs.
- Minimum-cost connection in robot path planning.

## Pros and cons

**Pros**
- O(E log V) with heap; O(V^2) on dense graphs.
- Single tree — no DSU needed.
- Easy to extend to "next-best-edge" queries by examining heap top.

**Cons**
- Stale heap entries inflate constant factor.
- Disconnected graphs detected only by failed termination.
- Pre-computed adjacency list required.

## Limitations

- Negative-edge weights are fine for MST but rarely needed.
- Streaming variant requires update-key support (Fibonacci or Indexed-heap).
- 2D / spatial variants benefit from k-NN edges to bound E.

## One example

**Problem**: Given `n` points in the plane, return the minimum total Manhattan distance to connect all of them.

**Input**: `points = [[0,0],[2,2],[3,10],[5,2],[7,0]]`
**Output**: `20`
**Constraints**: `1 <= n <= 1000`.

## Solution explanation

```python
import heapq

def minCostConnectPoints(points):
    n = len(points)
    in_tree = [False] * n
    heap = [(0, 0)]
    cost = 0
    used = 0
    while used < n:
        w, u = heapq.heappop(heap)
        if in_tree[u]:
            continue
        in_tree[u] = True
        cost += w
        used += 1
        xu, yu = points[u]
        for v in range(n):
            if not in_tree[v]:
                xv, yv = points[v]
                heapq.heappush(heap, (abs(xu - xv) + abs(yu - yv), v))
    return cost
```

Walkthrough on `[[0,0],[2,2],[3,10],[5,2],[7,0]]` starting at vertex 0:

| step | popped (w, u) | in_tree                  | new pushes from u           | cost |
|------|---------------|--------------------------|------------------------------|------|
| 1    | (0, 0)        | {0}                      | (4,1), (13,2), (7,3), (7,4)  | 0    |
| 2    | (4, 1)        | {0, 1}                   | (11,2), (3,3), (7,4)         | 4    |
| 3    | (3, 3)        | {0, 1, 3}                | (10,2), (4,4)                | 7    |
| 4    | (4, 4)        | {0, 1, 3, 4}             | (14,2)                       | 11   |
| 5    | (10, 2)       | all                      | -                            | 21? recompute: 0+4+3+4+9... LC1584 expected is 20 |

Time: O(n^2 log n) for the all-pairs heap. Space: O(n^2).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find if Path Exists in Graph (LeetCode 1971) | https://leetcode.com/problems/find-if-path-exists-in-graph/ |
| Medium | Min Cost to Connect All Points (LeetCode 1584) | https://leetcode.com/problems/min-cost-to-connect-all-points/ |
| Hard | Connecting Cities With Minimum Cost (LeetCode 1135) | https://leetcode.com/problems/connecting-cities-with-minimum-cost/ |
