# DFS-based topological sort (post-order reversal)

## What is this

A topological order of a DAG can be obtained by running **DFS** and pushing each vertex onto a stack **after all its descendants have finished** (post-order). Reversing the stack at the end yields a valid topological order.

The intuition: a vertex `u` with edge `u → v` cannot finish DFS until `v` finishes. So `v` is pushed to the stack first, and `u` later. After reversing, `u` comes before `v` — exactly what topological order requires.

Cycle detection is folded in using the same **three-colour** machinery as directed-graph cycle detection: a "back edge" (to a vertex still on the recursion stack) signals a cycle and aborts.

## Why we use

- O(V + E) — same as Kahn's, often slightly faster in practice due to better memory access patterns.
- Folds **cycle detection** into the same DFS without an extra pass.
- Concise implementation when recursion is acceptable.
- Reveals structural properties (strongly connected components are a small extension via Tarjan / Kosaraju).

## How to implement

```
WHITE, GRAY, BLACK = 0, 1, 2
color = [WHITE] * n
order = []     # reverse post-order will become topological order
def dfs(u):
    color[u] = GRAY
    for v in adj[u]:
        if color[v] == GRAY: return False     # cycle
        if color[v] == WHITE and not dfs(v): return False
    color[u] = BLACK
    order.append(u)
    return True

for u in 0..n-1:
    if color[u] == WHITE and not dfs(u): return None
return order[::-1]
```

Python:

```python
def topo_sort_dfs(n: int, edges: list[list[int]]) -> list[int] | None:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    order: list[int] = []

    def dfs(u: int) -> bool:
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                return False
            if color[v] == WHITE and not dfs(v):
                return False
        color[u] = BLACK
        order.append(u)
        return True

    for u in range(n):
        if color[u] == WHITE and not dfs(u):
            return None
    return order[::-1]
```

JavaScript — iterative (safer for huge graphs):

```javascript
function topoSortDFS(n, edges) {
  const adj = Array.from({ length: n }, () => []);
  for (const [u, v] of edges) adj[u].push(v);
  const color = new Int8Array(n);     // 0=W, 1=G, 2=B
  const order = [];
  for (let start = 0; start < n; start++) {
    if (color[start] !== 0) continue;
    const stack = [[start, 0]];
    color[start] = 1;
    while (stack.length) {
      const top = stack[stack.length - 1];
      const [u, i] = top;
      if (i < adj[u].length) {
        const v = adj[u][i];
        top[1]++;
        if (color[v] === 1) return null;          // cycle
        if (color[v] === 0) { color[v] = 1; stack.push([v, 0]); }
      } else {
        color[u] = 2;
        order.push(u);
        stack.pop();
      }
    }
  }
  return order.reverse();
}
```

Invariant: when a vertex `u` is appended to `order`, every descendant of `u` is already in `order` (i.e. appended before `u`). After reversing, every descendant appears **after** `u` — the topological order.

## Visual

Edges: `5 → 0, 5 → 2, 4 → 0, 4 → 1, 2 → 3, 3 → 1`.

```
   5 ──→ 0           5 ──→ 2 ──→ 3
   4 ──→ 0           4 ──→ 1
                          3 ──→ 1
```

DFS from 5: visit 0 (gray, no out-edges, → black, push 0); visit 2 (gray); visit 3 (gray); visit 1 (gray, no out-edges, → black, push 1); back to 3 (→ black, push 3); back to 2 (→ black, push 2); back to 5 (→ black, push 5).

DFS from 4 (1 and 0 already black): straight to black, push 4.

`order = [0, 1, 3, 2, 5, 4]`. Reverse: `[4, 5, 2, 3, 1, 0]` — a valid topological order.

## Which problems this approach solves in the real world

- **Build dependency resolution**: same as Kahn's — compile in deps-first order.
- **Workflow scheduling**: tasks must run after their dependencies.
- **Course planning**: take prereqs first.
- **Spreadsheet recalc**: recompute cells in dependency order.
- **Module loading**: import order.
- **Find strongly connected components**: DFS topo sort is the first half of Kosaraju's SCC algorithm.

## Pros and cons

**Pros**
- Concise recursive implementation (5-line core).
- Folds cycle detection into the same DFS.
- Slightly better cache behaviour than queue-based BFS in many cases.
- Naturally extends to "longest path in DAG" via DP over the post-order.

**Cons**
- Recursion depth = longest path → risk of stack overflow on deep DAGs (use iterative version).
- Produces just **one** valid topo order; for lexicographically smallest order, prefer Kahn's with a min-heap.
- "Push after subtree" is one of the most easy-to-misremember details — push *after* recursive calls, not before.

## Limitations

- Doesn't work on graphs with cycles — must detect and abort.
- For very wide DAGs (millions of independent vertices), Kahn's parallelises better.
- Doesn't tell you the cycle's nodes without extra bookkeeping (parent map).

## One example

**Problem**: There are `numCourses` courses you have to take, labeled `0..numCourses-1`. Some courses have prerequisites, given by `prerequisites[i] = [a, b]` meaning "to take course `a` you must first take course `b`". Return any valid order in which you should take the courses. If it is impossible to finish all courses, return an empty array.
Constraints: `1 ≤ numCourses ≤ 2000`, `0 ≤ prerequisites.length ≤ 5000`.

**Input**: `numCourses = 4`, `prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]`
**Output**: e.g. `[0, 2, 1, 3]` or `[0, 1, 2, 3]` (any valid topological order).

## Solution explanation

```python
def find_order(num_courses: int, prereqs: list[list[int]]) -> list[int]:
    adj: list[list[int]] = [[] for _ in range(num_courses)]
    for a, b in prereqs:
        adj[b].append(a)        # edge b → a (prereq before dependent)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_courses
    order: list[int] = []

    def dfs(u: int) -> bool:
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                return False
            if color[v] == WHITE and not dfs(v):
                return False
        color[u] = BLACK
        order.append(u)
        return True

    for u in range(num_courses):
        if color[u] == WHITE and not dfs(u):
            return []
    return order[::-1]
```

Walk-through on edges `0→1, 0→2, 1→3, 2→3` (so adj[0]=[1,2], adj[1]=[3], adj[2]=[3], adj[3]=[]):

| call         | color before              | action                 | order after     | color after                |
|--------------|---------------------------|------------------------|------------------|-----------------------------|
| dfs(0)       | [W,W,W,W]                | gray 0                 | []               | [G,W,W,W]                  |
| dfs(1)       | [G,W,W,W]                | gray 1                 | []               | [G,G,W,W]                  |
| dfs(3)       | [G,G,W,W]                | gray 3, no out-edges   | [3]              | [G,G,W,B]                  |
| pop to 1     | —                         | black 1, push          | [3, 1]           | [G,B,W,B]                  |
| pop to 0; next: 2 | [G,B,W,B]            | dfs(2)                 | —                | —                          |
| dfs(2)       | [G,B,W,B]                | gray 2, look 3: black → skip | —          | [G,B,G,B]                  |
| pop to 2     | —                         | black 2, push          | [3, 1, 2]        | [G,B,B,B]                  |
| pop to 0     | —                         | black 0, push          | [3, 1, 2, 0]     | [B,B,B,B]                  |

All other vertices already black. Reverse `order` → `[0, 2, 1, 3]`.

Correctness: when DFS finishes processing `u` (about to mark it black), every vertex reachable from `u` has already finished — so it precedes `u` in `order`. Thus in `order`, every successor of `u` comes before `u`. Reversing gives "every predecessor before its successor", which is the topological condition.

- **Time**: O(V + E) — each vertex and edge touched once.
- **Space**: O(V) for colour + recursion + order list.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Find the Town Judge** — degree analysis warm-up; no topo, but builds graph-construction muscle. | https://leetcode.com/problems/find-the-town-judge/ |
| Medium | **Course Schedule II** — the canonical topological-sort problem above. | https://leetcode.com/problems/course-schedule-ii/ |
| Hard | **Parallel Courses III** — longest-path DP on a topo-ordered DAG; perfect follow-up. | https://leetcode.com/problems/parallel-courses-iii/ |
