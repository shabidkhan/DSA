# Multi-source BFS

## What is this

Multi-source BFS starts BFS simultaneously from *several* sources. Seed the queue with all source vertices at distance 0, then run normal BFS. Each cell / node ends up at its distance from the *nearest* source — without running V independent BFS passes.

It is the right algorithm for "rotten oranges" spread, multi-fire propagation, "distance from nearest gate", and any "shortest distance to the nearest of a set" question on unweighted graphs.

## Why we use

- O(V + E) total, regardless of source count.
- Solves "nearest source" simultaneously for all targets.
- Identical inner loop to single-source BFS.
- Natural fit for spread / contagion modeling.

## How to implement

```
q = deque(sources)
dist = {s: 0 for s in sources}
while q:
    u = q.popleft()
    for v in neighbors(u):
        if v not in dist:
            dist[v] = dist[u] + 1
            q.append(v)
```

```python
from collections import deque

def multi_source_bfs(grid, source_value):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == source_value:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1 and grid[nr][nc] != 'wall':
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
```

```python
def rotten_oranges(grid):
    rows, cols = len(grid), len(grid[0])
    fresh = 0
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q:
        r, c, t = q.popleft()
        minutes = max(minutes, t)
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, t + 1))
    return minutes if fresh == 0 else -1
```

Seeding all sources at distance 0 in the same queue lets a single BFS produce the simultaneous nearest-source distances.

## Which problems this approach solves in the real world

- Modeling disease / fire / rumor spread from multiple origins.
- Computing distance from any cell to the nearest hospital / facility.
- Multi-channel network propagation analysis.
- Wavefront-style cellular-automaton updates.
- Resource-availability shortest-distance maps in robotics.

## Pros and cons

**Pros**
- O(V + E) — single BFS for all sources.
- Trivially extends to weighted "0-1 BFS" with a deque.
- Simple correctness — BFS invariant scaled to many sources.

**Cons**
- Source count k must fit in memory (initial queue size).
- Unweighted only; weighted needs Dijkstra.
- Disconnected nodes from any source remain at infinity.

## Limitations

- Single-source path reconstruction is ambiguous — store a `parent` per cell.
- Cannot prioritize by source rank without extra bookkeeping.
- Dynamic source set requires recomputation.

## One example

**Problem**: You are given a 2D grid `grid` where each cell is one of: `2` rotten orange, `1` fresh orange, `0` empty. Every minute, any fresh orange adjacent (4-direction) to a rotten one becomes rotten. Return the minimum minutes after which no fresh orange remains, or `-1` if impossible.

**Input**: `grid = [[2,1,1],[1,1,0],[0,1,1]]`
**Output**: `4`
**Constraints**: `1 <= m, n <= 10`, `grid[i][j] in {0, 1, 2}`.

## Solution explanation

`rotten_oranges` above. Walkthrough on the input:

Initial grid (R = rotten, F = fresh, _ = empty):
```
R F F
F F _
_ F F
```
Minute 0: only one rotten at (0,0).

| minute | new rotten cells       | fresh remaining |
|--------|------------------------|------------------|
| 1      | (0,1), (1,0)           | 4                |
| 2      | (0,2), (1,1)           | 2                |
| 3      | (2,1)                  | 1                |
| 4      | (2,2)                  | 0                |

Return 4. Time: O(m*n). Space: O(m*n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Flood Fill (LeetCode 733) | https://leetcode.com/problems/flood-fill/ |
| Medium | 01 Matrix (LeetCode 542) | https://leetcode.com/problems/01-matrix/ |
| Hard | Walls and Gates (LeetCode 286) | https://leetcode.com/problems/walls-and-gates/ |
