# Topological sort

## Folder structure

```
03-Topological-sort/
├── README.md
├── 01-Kahn/README.md
└── 02-DFS-based/README.md
```

## What is this

Topological sort produces a linear ordering of the vertices of a directed acyclic graph (DAG) such that for every directed edge `u -> v`, `u` appears before `v` in the ordering. It only exists when the graph has no cycles; cycle detection is a free byproduct.

Two standard algorithms produce it: Kahn's algorithm (BFS over zero-indegree vertices) and DFS-based postorder reversal. Both run in O(V + E).

## Why we use

- Schedules tasks subject to dependencies (build systems, course prerequisites)
- Detects cycles in directed graphs (the algorithm fails ⇔ a cycle exists)
- Lays the groundwork for DAG-shortest/longest paths in linear time
- Produces evaluation orders for dataflow graphs, spreadsheets, ML pipelines

## How to implement

```
Kahn's algorithm:
  indeg[v] = number of incoming edges
  queue = all v with indeg[v] == 0
  while queue not empty:
      u = queue.popleft()
      order.append(u)
      for v in adj[u]:
          indeg[v] -= 1
          if indeg[v] == 0:
              queue.append(v)
  if len(order) != V: cycle exists
```

```python
from collections import deque

def topo_sort_kahn(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    graph: dict[int, list[int]] = {i: [] for i in range(n)}
    indeg = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indeg[v] += 1
    queue = deque(i for i in range(n) if indeg[i] == 0)
    order: list[int] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return order if len(order) == n else None
```

DFS-based variant (reverse postorder):

```python
def topo_sort_dfs(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    graph: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    order: list[int] = []
    def visit(u: int) -> bool:
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == GRAY:
                return False
            if color[v] == WHITE and not visit(v):
                return False
        color[u] = BLACK
        order.append(u)
        return True
    for u in range(n):
        if color[u] == WHITE and not visit(u):
            return None
    return order[::-1]
```

Invariant for Kahn's: vertices enter the queue only after all their dependencies have been emitted, so the output is a valid order. Termination with `len(order) < n` means some vertex still has `indeg > 0`, which only happens inside a cycle.

## Which problems this approach solves in the real world

- Build systems: compile order of files based on `#include` / `import` dependencies
- Course planning: order classes so prerequisites are always taken first
- Spreadsheet recalc order: evaluate cells in dataflow order
- Module loading in package managers (npm, pip, apt)
- Pipeline scheduling in ETL / data engineering DAGs (Airflow, Dagster)

## Pros and cons

**Pros**
- Linear O(V + E)
- Kahn's variant naturally identifies independent tasks (multiple zero-indegree vertices => parallelisable)
- DFS variant exposes finish times useful for SCC and longest-path algorithms

**Cons**
- Only defined for DAGs; cycles produce no valid ordering
- Ordering is not unique — downstream consumers need to handle ties
- DFS variant must handle Python recursion depth on long chains

## Limitations

- Cannot order graphs that contain cycles (must first condense SCCs)
- Provides one ordering; if you need all topological orderings, do backtracking
- Dynamic insertion/deletion of edges requires incremental algorithms (Pearce-Kelly)

## One example

Problem: There are `numCourses` courses labelled `0..numCourses-1`. Some courses have prerequisites: `prereq[i] = (a, b)` means you must take `b` before `a`. Return an order in which you can take all the courses, or an empty list if impossible.

```
Input:  numCourses = 4, prereq = [(1, 0), (2, 0), (3, 1), (3, 2)]
Output: [0, 1, 2, 3]   (or [0, 2, 1, 3])
Constraints: 1 <= numCourses <= 2000, 0 <= len(prereq) <= 5000
```

## Solution explanation

```python
from collections import deque

def find_order(num_courses: int, prereq: list[tuple[int, int]]) -> list[int]:
    graph: dict[int, list[int]] = {i: [] for i in range(num_courses)}
    indeg = [0] * num_courses
    for a, b in prereq:           # edge b -> a (take b before a)
        graph[b].append(a)
        indeg[a] += 1
    queue = deque(i for i in range(num_courses) if indeg[i] == 0)
    order: list[int] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return order if len(order) == num_courses else []
```

Build a graph from prerequisites to dependents, then Kahn-sort. If a cycle exists, the queue empties before all courses are output and the function returns `[]`.

Walkthrough for `numCourses = 4`, `prereq = [(1,0),(2,0),(3,1),(3,2)]`. Graph: `0 -> [1, 2]`, `1 -> [3]`, `2 -> [3]`. Indegrees: `[0, 1, 1, 2]`.

| Step | Queue   | Pop | After indeg decrement       | Order        |
|------|---------|-----|------------------------------|--------------|
| init | [0]     |     |                              | []           |
| 1    | []      | 0   | indeg=[0,0,0,2] queue=[1,2]  | [0]          |
| 2    | [2]     | 1   | indeg=[0,0,0,1] queue=[2]    | [0, 1]       |
| 3    | []      | 2   | indeg=[0,0,0,0] queue=[3]    | [0, 1, 2]    |
| 4    | []      | 3   | (no outgoing)                | [0, 1, 2, 3] |

Time O(V + E), space O(V + E).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find the Town Judge (LeetCode 997) | https://leetcode.com/problems/find-the-town-judge/ |
| Medium | Course Schedule II (LeetCode 210) | https://leetcode.com/problems/course-schedule-ii/ |
| Hard | Alien Dictionary (LeetCode 269) | https://leetcode.com/problems/alien-dictionary/ |
