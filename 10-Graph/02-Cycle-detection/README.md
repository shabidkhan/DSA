# Cycle detection

## Folder structure

```
02-Cycle-detection/
├── README.md
├── 01-Directed/README.md
└── 02-Undirected/README.md
```

## What is this

Cycle detection asks: does a graph contain a cycle? The technique depends on directedness:

- **Undirected**: DFS with parent tracking — a non-parent visited neighbor signals a cycle. Union-Find works too.
- **Directed**: DFS with three colors (white = unvisited, gray = in current path, black = finished). A gray neighbor signals a cycle. Alternatively, Kahn's topological sort: if the result has fewer vertices than V, a cycle exists.

Both run in O(V + E).

## Why we use

- O(V + E) detection — no extra logarithmic factors.
- Two distinct techniques cover both directed and undirected cases.
- Foundation for topological sort, deadlock detection, and DSU-based cycle handling.
- Color-coded DFS extends to "find all back edges" or "report any cycle".

## How to implement (directed, 3-color DFS)

```
color = [WHITE] * V
def dfs(u):
    color[u] = GRAY
    for v in adj[u]:
        if color[v] == GRAY: return True   # back edge
        if color[v] == WHITE and dfs(v): return True
    color[u] = BLACK
    return False

for u in 0..V-1:
    if color[u] == WHITE and dfs(u): return True
return False
```

```python
def has_cycle_directed(n, adj):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    def dfs(u):
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY: return True
            if color[v] == WHITE and dfs(v): return True
        color[u] = BLACK
        return False
    for u in range(n):
        if color[u] == WHITE and dfs(u):
            return True
    return False
```

```python
def has_cycle_undirected(n, adj):
    visited = [False] * n
    def dfs(u, parent):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                if dfs(v, u): return True
            elif v != parent:
                return True
        return False
    for u in range(n):
        if not visited[u] and dfs(u, -1):
            return True
    return False
```

For directed, the "gray" color *must* be reset to BLACK only after children finish — a stale GRAY produces wrong cycles.

## Which problems this approach solves in the real world

- Deadlock detection in lock-graph analysis.
- Build-system DAG validation (no circular dependencies).
- Course-prerequisite cycle detection.
- Currency-arbitrage detection (negative cycle in log-rate graph).
- DAG enforcement in workflow / pipeline configs.

## Pros and cons

**Pros**
- O(V + E) — optimal asymptotically.
- Simple recursive structure.
- Easy to extend to "find and report cycle" via backtracking.

**Cons**
- Recursion depth O(V) — overflow risk on long chains.
- 3-color directed variant trips up beginners.
- Disconnected graphs need outer iteration over all vertices.

## Limitations

- Recursion stack must accommodate worst-case depth.
- Multi-edges / self-loops need explicit handling.
- Identifying *all* cycles is exponential in worst case.

## One example

**Problem**: Given a directed graph as an adjacency list, return `True` if it contains a cycle.

**Input**: `n = 4`, `edges = [[0,1],[1,2],[2,3],[3,1]]`
**Output**: `True`  (cycle 1 → 2 → 3 → 1)
**Constraints**: `1 <= n <= 10^4`, `0 <= edges.length <= 10^4`.

## Solution explanation

```python
def hasCycle(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    def dfs(u):
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY: return True
            if color[v] == WHITE and dfs(v): return True
        color[u] = BLACK
        return False
    for u in range(n):
        if color[u] == WHITE and dfs(u):
            return True
    return False
```

Walkthrough on edges `[[0,1],[1,2],[2,3],[3,1]]`:

| step | call    | color state before     | action                          |
|------|---------|------------------------|----------------------------------|
| 1    | dfs(0)  | WWWW                   | mark GRAY[0]                     |
| 2    | dfs(1)  | GWWW                   | mark GRAY[1]                     |
| 3    | dfs(2)  | GGWW                   | mark GRAY[2]                     |
| 4    | dfs(3)  | GGGW                   | mark GRAY[3]; sees 1 (GRAY) → cycle |

Return True. Time: O(V + E). Space: O(V).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find the Town Judge (LeetCode 997) | https://leetcode.com/problems/find-the-town-judge/ |
| Medium | Course Schedule (LeetCode 207) | https://leetcode.com/problems/course-schedule/ |
| Hard | Critical Connections in a Network (LeetCode 1192) | https://leetcode.com/problems/critical-connections-in-a-network/ |
