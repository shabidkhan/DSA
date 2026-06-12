# Breadth-First Search (BFS)

## What is this

Breadth-First Search explores a graph layer by layer starting from a source vertex. It uses a FIFO queue and a `visited` set: pop a vertex, push all unvisited neighbours, mark them visited. Every vertex is discovered at the smallest possible number of edges from the source, so BFS yields the shortest path in an unweighted graph.

The same skeleton works on directed/undirected graphs, grids (treating cells as nodes and 4/8 directions as edges), and implicit state graphs in puzzles (Rubik's cube positions, word ladders).

## Why we use

- Finds shortest path in unweighted graphs in O(V + E)
- Discovers all vertices reachable from a source
- Computes connected components and bipartite checks
- Underpins level-order traversal, flood-fill, multi-source shortest path

## How to implement

```
queue = deque([source])
visited = {source}
while queue:
    u = queue.popleft()
    for v in neighbours(u):
        if v not in visited:
            visited.add(v)
            queue.append(v)
```

Standard BFS returning the distance map from `source`:

```python
from collections import deque

def bfs(graph: dict[int, list[int]], source: int) -> dict[int, int]:
    dist = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist
```

BFS on a grid (4-directional) returning shortest path length from `(0, 0)` to `(m-1, n-1)`:

```python
from collections import deque

def shortest_grid_path(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[m-1][n-1] == 1:
        return -1
    queue = deque([(0, 0, 1)])
    visited = {(0, 0)}
    while queue:
        r, c, d = queue.popleft()
        if (r, c) == (m - 1, n - 1):
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, d + 1))
    return -1
```

Invariant: when a vertex is dequeued, its distance is final and minimal because BFS processes vertices in non-decreasing distance order.

## Which problems this approach solves in the real world

- Shortest hop count in a social network (degrees of separation)
- Web crawling within a fixed link-depth budget
- Flood-fill in paint tools and segmentation in images
- Network broadcast hop count (e.g. routing in LAN)
- Puzzle solving where each move has uniform cost (sliding puzzles, word ladders)

## Pros and cons

**Pros**
- Simple to implement and reason about
- Optimal for unweighted shortest paths
- Linear in graph size, predictable memory pattern

**Cons**
- Memory grows with the frontier — bad on extremely wide graphs
- Does not handle weighted edges (use Dijkstra instead)
- Repeated lookups on a hash-based `visited` set hurt cache locality

## Limitations

- Cannot find shortest path in weighted graphs (use Dijkstra / Bellman-Ford)
- Cycle detection in directed graphs needs DFS-based coloring
- BFS on infinite graphs may never terminate without a depth bound
- High memory use on dense or wide graphs

## One example

Problem: Given a binary grid (0 = passable, 1 = wall), return the length (in cells) of the shortest path from `(0, 0)` to `(m-1, n-1)` moving 4-directionally, or `-1` if unreachable.

```
Input:  grid = [[0, 0, 1],
                [1, 0, 0],
                [1, 1, 0]]
Output: 5   (cells: (0,0) -> (0,1) -> (1,1) -> (1,2) -> (2,2))
Constraints: 1 <= m, n <= 100
```

## Solution explanation

```python
from collections import deque

def shortest_grid_path(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[m-1][n-1] == 1:
        return -1
    queue = deque([(0, 0, 1)])
    visited = {(0, 0)}
    while queue:
        r, c, d = queue.popleft()
        if (r, c) == (m - 1, n - 1):
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, d + 1))
    return -1
```

Each cell is enqueued once with its current path length. BFS guarantees the first time we dequeue the target, the distance is shortest.

Walkthrough for the input above:

| Step | Queue (front -> back)                        | Dequeue | Action                          |
|------|----------------------------------------------|---------|---------------------------------|
| 1    | [(0,0,1)]                                    | (0,0,1) | push (0,1,2)                    |
| 2    | [(0,1,2)]                                    | (0,1,2) | push (1,1,3)                    |
| 3    | [(1,1,3)]                                    | (1,1,3) | push (1,2,4)                    |
| 4    | [(1,2,4)]                                    | (1,2,4) | push (2,2,5)                    |
| 5    | [(2,2,5)]                                    | (2,2,5) | target -> return 5              |

Time O(m * n), space O(m * n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find the Town Judge (BFS/indegree) | https://leetcode.com/problems/find-the-town-judge/ |
| Medium | Rotting Oranges | https://leetcode.com/problems/rotting-oranges/ |
| Hard | Word Ladder | https://leetcode.com/problems/word-ladder/ |
