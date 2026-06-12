# Bipartite check

## What is this

A graph is bipartite if its vertices can be partitioned into two sets such that every edge connects one vertex in each set — equivalently, the graph is 2-colorable. Detect bipartiteness via BFS or DFS that assigns alternating colors; if an edge connects two same-colored vertices, the graph is not bipartite.

Bipartite structure unlocks max-flow / matching algorithms with much faster specialized variants (Hopcroft-Karp, Hungarian).

## Why we use

- O(V + E) check — same as a single BFS / DFS pass.
- Foundation for bipartite matching, vertex cover, independent set.
- Cleanly detects odd cycles (bipartite ↔ no odd cycle).
- Linear-time foundation for many "2-set" partition problems.

## How to implement

```
color = [-1] * V
def bfs(start):
    color[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if color[v] == -1:
                color[v] = 1 - color[u]
                q.append(v)
            elif color[v] == color[u]:
                return False
    return True
for u: if color[u] == -1 and not bfs(u): return False
return True
```

```python
from collections import deque

def is_bipartite(n, adj):
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
```

```python
def is_bipartite_dfs(n, adj):
    color = [-1] * n
    def dfs(u, c):
        color[u] = c
        for v in adj[u]:
            if color[v] == -1:
                if not dfs(v, 1 - c): return False
            elif color[v] == c:
                return False
        return True
    for u in range(n):
        if color[u] == -1 and not dfs(u, 0):
            return False
    return True
```

Always iterate over all start vertices — a graph may have multiple components.

## Which problems this approach solves in the real world

- Bipartite matching: assignment problems (jobs ↔ workers).
- Two-team / two-color partition in conflict graphs.
- Detecting feasibility of 2-coloring constraint problems.
- Conflict-graph register allocation in compilers (degenerate cases).
- Detecting odd cycles as a structural property.

## Pros and cons

**Pros**
- O(V + E) detection.
- Single pass with no extra data structures.
- Simple correctness via the no-odd-cycle theorem.

**Cons**
- Disconnected components require an outer loop.
- DFS variant has recursion-depth risk on long chains.
- "Approximately bipartite" / k-coloring (k ≥ 3) is NP-hard — pattern doesn't generalize.

## Limitations

- Provides only yes/no plus a coloring — no matching is computed.
- Streaming / dynamic bipartite check needs incremental algorithms.
- Directed graphs ignore direction; treat as undirected for bipartite check.

## One example

**Problem**: Given an undirected graph as adjacency list `graph` where `graph[i]` lists the neighbors of node `i`, return `True` if and only if the graph is bipartite.

**Input**: `graph = [[1,2,3],[0,2],[0,1,3],[0,2]]`
**Output**: `False`
**Constraints**: `1 <= graph.length <= 100`.

## Solution explanation

```python
from collections import deque

def isBipartite(graph):
    n = len(graph)
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True
```

Walkthrough on `[[1,2,3],[0,2],[0,1,3],[0,2]]` (vertex 0 connected to 1,2,3; etc):

| step | u | adj         | color before     | result |
|------|---|-------------|------------------|--------|
| 1    | 0 | [1, 2, 3]   | [0,-1,-1,-1]     | set color[1..3]=1; queue grows |
| 2    | 1 | [0, 2]      | [0, 1, 1, 1]     | sees 2 with same color 1 → False |

Return False. Time: O(V + E). Space: O(V).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find the Town Judge (LeetCode 997) | https://leetcode.com/problems/find-the-town-judge/ |
| Medium | Is Graph Bipartite? (LeetCode 785) | https://leetcode.com/problems/is-graph-bipartite/ |
| Hard | Possible Bipartition (LeetCode 886) | https://leetcode.com/problems/possible-bipartition/ |
