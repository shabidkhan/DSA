# Kahn's algorithm (BFS topological sort)

## What is this

Kahn's algorithm produces a **topological order** of a DAG (directed acyclic graph) — a linear ordering of vertices such that for every directed edge `u → v`, `u` appears before `v` in the ordering. It's a **BFS** approach:

1. Compute `in_degree[v]` (the number of incoming edges) for every vertex.
2. Push every vertex with `in_degree == 0` into a queue — these have no prerequisites.
3. Repeatedly pop a vertex `u`, append it to the order, and for each neighbour `v`, decrement `in_degree[v]`; if it reaches 0, push `v`.
4. If the final order has fewer than `n` vertices, the graph has a **cycle**.

## Why we use

- O(V + E) time — touches each vertex and edge once.
- Naturally also acts as a **cycle detector** for directed graphs (if `|order| < n`, cycle exists).
- BFS-based — naturally produces a "layer-by-layer" order (all roots first, then their direct dependents, etc.).
- Easier to reason about than recursive DFS-topo-sort; no stack-overflow risk.

## How to implement

```
in_deg = [0] * n
for (u, v) in edges:
    in_deg[v] += 1

queue = deque(v for v in 0..n-1 if in_deg[v] == 0)
order = []
while queue:
    u = queue.popleft()
    order.append(u)
    for v in adj[u]:
        in_deg[v] -= 1
        if in_deg[v] == 0:
            queue.append(v)

return order if len(order) == n else None    # None means cycle
```

Python:

```python
from collections import deque

def topo_sort_kahn(n: int, edges: list[list[int]]) -> list[int] | None:
    adj: list[list[int]] = [[] for _ in range(n)]
    in_deg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        in_deg[v] += 1
    q = deque(v for v in range(n) if in_deg[v] == 0)
    order: list[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                q.append(v)
    return order if len(order) == n else None
```

JavaScript:

```javascript
function topoSortKahn(n, edges) {
  const adj = Array.from({ length: n }, () => []);
  const inDeg = Array(n).fill(0);
  for (const [u, v] of edges) { adj[u].push(v); inDeg[v]++; }
  const queue = [];
  for (let v = 0; v < n; v++) if (inDeg[v] === 0) queue.push(v);
  const order = [];
  while (queue.length) {
    const u = queue.shift();
    order.push(u);
    for (const v of adj[u]) {
      if (--inDeg[v] === 0) queue.push(v);
    }
  }
  return order.length === n ? order : null;
}
```

Invariant: every vertex in the queue has all its prerequisites already in `order`. We never emit a vertex before its prerequisites — the resulting list is a valid topological order.

## Visual

Edges: `0→1, 0→2, 1→3, 2→3` (small DAG).

```
   0 ──→ 1
   │     │
   ▼     ▼
   2 ──→ 3
```

Initial `in_deg = [0, 1, 1, 2]`. Queue starts with `[0]`.

- Pop 0 → order=[0]; decrement in_deg of 1 (→0, enqueue) and 2 (→0, enqueue). Queue=[1, 2].
- Pop 1 → order=[0,1]; decrement in_deg of 3 (→1). Queue=[2].
- Pop 2 → order=[0,1,2]; decrement in_deg of 3 (→0, enqueue). Queue=[3].
- Pop 3 → order=[0,1,2,3]. Queue=[].

Valid order: `[0, 1, 2, 3]`. (Also `[0, 2, 1, 3]` if we'd processed 2 before 1.)

## Which problems this approach solves in the real world

- **Build / dependency resolution**: order to compile source files such that each compiles after its imports.
- **University course planning**: order to take courses such that prerequisites are completed first.
- **Spreadsheet recalculation**: order in which to recompute cells.
- **Pipeline scheduling**: data-processing stages with input dependencies.
- **Task batching / job ordering**: cron-style jobs with deps.
- **Cycle detection** in directed graphs (as a side effect).

## Pros and cons

**Pros**
- O(V + E) — linear time.
- Iterative — no recursion-stack risk.
- Detects cycles as a free side-effect.
- Easy to extend to "all valid topo orders" (with backtracking on choices) or "lexicographically smallest topo order" (replace queue with min-heap).

**Cons**
- Requires knowing in-degree up-front — needs a full pass before starting.
- Produces only **one** valid order — picking a different start changes the output. Not always what you want.
- Uses an explicit queue — slightly more code than DFS post-order.

## Limitations

- Doesn't work on graphs with cycles — returns "incomplete" but doesn't tell you *which* edges form the cycle.
- For very dense graphs, the `decrement + enqueue` cost dominates linearly; no shortcut.
- Doesn't compute longest path / critical path on its own — you'd extend with a DP over the topo order.

## One example

**Problem**: There are `numCourses` courses you have to take, labeled `0..numCourses-1`. You are given `prerequisites` where `prerequisites[i] = [a, b]` means "to take course `a` you must take course `b` first". Return any **valid order** in which you should take the courses. If it is impossible to finish all courses, return an empty array.
Constraints: `1 ≤ numCourses ≤ 2000`, `0 ≤ prerequisites.length ≤ 5000`.

**Input**: `numCourses = 4`, `prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]`
**Output**: `[0, 1, 2, 3]` or `[0, 2, 1, 3]` (any valid topo order).

## Solution explanation

```python
from collections import deque

def find_order(num_courses: int, prereqs: list[list[int]]) -> list[int]:
    adj: list[list[int]] = [[] for _ in range(num_courses)]
    in_deg = [0] * num_courses
    for a, b in prereqs:
        adj[b].append(a)      # b is a prereq of a → edge b → a
        in_deg[a] += 1
    q = deque(v for v in range(num_courses) if in_deg[v] == 0)
    order: list[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []
```

Walk-through on edges `[[1,0],[2,0],[3,1],[3,2]]` (interpreted as edges `0→1, 0→2, 1→3, 2→3`):

| step | queue start | pop | in_deg after decrements          | queue end | order so far     |
|------|-------------|-----|----------------------------------|-----------|------------------|
| init | [0]         | —   | [0, 1, 1, 2]                     | [0]       | []               |
| 1    | [0]         | 0   | [0, 0, 0, 2] (1 and 2 enqueued)  | [1, 2]    | [0]              |
| 2    | [1, 2]      | 1   | [0, 0, 0, 1] (3's in_deg=1)      | [2]       | [0, 1]           |
| 3    | [2]         | 2   | [0, 0, 0, 0] (3 enqueued)        | [3]       | [0, 1, 2]        |
| 4    | [3]         | 3   | [0, 0, 0, 0]                     | []        | [0, 1, 2, 3]     |

`|order| == n` → valid. Answer: `[0, 1, 2, 3]`.

Correctness: by induction, when vertex `u` is dequeued, all its prerequisites have already been dequeued (because they decremented `in_deg[u]` to 0). So appending `u` after all its prereqs preserves topological order. If a cycle exists, every vertex in the cycle keeps a non-zero in-degree (waiting for another cycle member to be emitted first) — none gets enqueued, so `|order| < n` and we return failure.

- **Time**: O(V + E) — single pass each.
- **Space**: O(V + E) for adj + in-degree + queue.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Find Center of Star Graph** — adjacency / degree warm-up; no topo, but builds the intuition. | https://leetcode.com/problems/find-center-of-star-graph/ |
| Medium | **Course Schedule II** — the canonical Kahn's-algorithm problem above. | https://leetcode.com/problems/course-schedule-ii/ |
| Hard | **Alien Dictionary** — derive ordering edges from comparing adjacent words, then topo-sort. | https://leetcode.com/problems/alien-dictionary/ |
