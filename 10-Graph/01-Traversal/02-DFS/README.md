# Depth-First Search (DFS)

## What is this

Depth-First Search explores a graph by going as deep as possible along each branch before backtracking. It uses a stack (explicit or via recursion) and a `visited` set. From the current vertex, recurse into one unvisited neighbour at a time; when all neighbours are exhausted, backtrack.

DFS yields a depth-first tree of discovery edges, plus classifications of remaining edges as tree, back, forward, or cross edges. These classifications power cycle detection, topological sort, strongly connected components, and bridge/articulation finding.

## Why we use

- Linear time O(V + E) traversal of every reachable vertex
- Naturally expresses recursive structure (trees, components, parentheses)
- Powers cycle detection, topological sort, SCC (Tarjan/Kosaraju), articulation points
- Lower memory in narrow-deep graphs than BFS (no frontier explosion)

## How to implement

```
def dfs(u):
    visited.add(u)
    for v in neighbours(u):
        if v not in visited:
            dfs(v)
```

Recursive DFS collecting visit order:

```python
def dfs(graph: dict[int, list[int]], source: int) -> list[int]:
    visited: set[int] = set()
    order: list[int] = []
    def visit(u: int) -> None:
        visited.add(u)
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visit(v)
    visit(source)
    return order
```

Iterative DFS with an explicit stack (avoids recursion depth limits):

```python
def dfs_iterative(graph: dict[int, list[int]], source: int) -> list[int]:
    visited = {source}
    order: list[int] = []
    stack = [source]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                stack.append(v)
    return order
```

Cycle detection in a directed graph (3-color DFS):

```python
def has_cycle(graph: dict[int, list[int]]) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {u: WHITE for u in graph}
    def visit(u: int) -> bool:
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and visit(v):
                return True
        color[u] = BLACK
        return False
    return any(color[u] == WHITE and visit(u) for u in graph)
```

Invariant: at the start of `visit(u)`, all ancestors on the current path are GRAY; a GRAY edge target therefore signals a back edge (cycle).

## Which problems this approach solves in the real world

- Build-system dependency resolution (topological order, cycle detection)
- Detecting deadlocks via wait-for graph cycle analysis
- Finding connected components in social networks or file systems
- Maze and game-AI exploration where deep paths are pruned by heuristics
- Static analyzers (call-graph traversal, dead code, reachability)

## Pros and cons

**Pros**
- Tiny code, natural recursion
- O(V + E) time, O(V) auxiliary memory in recursion stack
- Foundation for many graph algorithms (topo sort, SCC, bridges)

**Cons**
- Recursion depth can blow Python's default stack for chains of 1000+
- Doesn't yield shortest paths in unweighted graphs (use BFS)
- Sensitive to neighbour iteration order in some applications (e.g. lexicographic DFS)

## Limitations

- Recursive form unsuitable for very deep graphs without increasing recursion limit
- Doesn't compute distances or shortest paths
- Edge classification logic must be tracked manually for advanced uses

## One example

Problem: Given an undirected graph as an adjacency list, count the number of connected components.

```
Input:  n = 5, edges = [(0, 1), (1, 2), (3, 4)]
Output: 2     (component {0, 1, 2} and component {3, 4})
Constraints: 1 <= n <= 10^4, 0 <= len(edges) <= 10^5
```

## Solution explanation

```python
def count_components(n: int, edges: list[tuple[int, int]]) -> int:
    graph: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited: set[int] = set()
    def visit(u: int) -> None:
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                visit(v)
    count = 0
    for u in range(n):
        if u not in visited:
            count += 1
            visit(u)
    return count
```

For each unvisited vertex, DFS marks all reachable vertices and counts the launches.

Walkthrough for `n = 5`, `edges = [(0, 1), (1, 2), (3, 4)]`:

| Vertex (outer) | visited before  | action                          | visited after          | count |
|----------------|-----------------|---------------------------------|------------------------|-------|
| 0              | {}              | DFS visits 0, 1, 2              | {0, 1, 2}              | 1     |
| 1              | {0, 1, 2}       | already visited, skip           | {0, 1, 2}              | 1     |
| 2              | {0, 1, 2}       | skip                            | {0, 1, 2}              | 1     |
| 3              | {0, 1, 2}       | DFS visits 3, 4                 | {0, 1, 2, 3, 4}        | 2     |
| 4              | {0, 1, 2, 3, 4} | skip                            | {0, 1, 2, 3, 4}        | 2     |

Time O(V + E), space O(V) for recursion + visited set.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find if Path Exists in Graph | https://leetcode.com/problems/find-if-path-exists-in-graph/ |
| Medium | Number of Islands | https://leetcode.com/problems/number-of-islands/ |
| Hard | Critical Connections in a Network (Tarjan bridges) | https://leetcode.com/problems/critical-connections-in-a-network/ |
