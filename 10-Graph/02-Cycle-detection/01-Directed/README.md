# Cycle detection in directed graphs (3-color DFS)

## What is this

In a directed graph, a cycle is a sequence of vertices `v0 → v1 → ... → vk = v0` following edge directions. DFS with **three colours** detects such cycles:

- **White (0)**: not yet visited.
- **Gray (1)**: currently on the DFS recursion stack (in progress).
- **Black (2)**: fully processed (all descendants explored, popped from stack).

A cycle exists if and only if DFS encounters an edge to a **gray** vertex — that's a "back edge" pointing to an ancestor in the current recursion path. An edge to a black vertex is a "cross edge" or "forward edge" — not a cycle.

Kahn's BFS-based topological sort is an alternative: cycles exist iff fewer than `n` vertices can be topologically ordered.

## Why we use

- O(V + E) time — every vertex and every edge is examined once.
- O(V) extra memory for the colour array.
- Pinpoints which vertex closed the cycle — useful for diagnostics.
- The three-colour idea generalises to "find strongly connected components" (Tarjan / Kosaraju) and topological sort.

## How to implement

```
WHITE, GRAY, BLACK = 0, 1, 2
color = [WHITE] * n
def dfs(u):
    color[u] = GRAY
    for v in adj[u]:
        if color[v] == GRAY:   return True           # back edge → cycle
        if color[v] == WHITE and dfs(v): return True
    color[u] = BLACK
    return False

for u in 0..n-1:
    if color[u] == WHITE and dfs(u):
        return True            # cycle found
return False
```

Python:

```python
def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(u: int) -> bool:
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for u in range(n):
        if color[u] == WHITE and dfs(u):
            return True
    return False
```

JavaScript (iterative to avoid stack overflow on large graphs):

```javascript
function hasCycleDirected(n, edges) {
  const adj = Array.from({ length: n }, () => []);
  for (const [u, v] of edges) adj[u].push(v);
  const color = new Int8Array(n);              // 0=W, 1=G, 2=B
  for (let start = 0; start < n; start++) {
    if (color[start] !== 0) continue;
    const stack = [[start, 0]];                // [node, edge index]
    color[start] = 1;
    while (stack.length) {
      const top = stack[stack.length - 1];
      const [u, i] = top;
      if (i < adj[u].length) {
        const v = adj[u][i];
        top[1]++;
        if (color[v] === 1) return true;       // back edge
        if (color[v] === 0) {
          color[v] = 1;
          stack.push([v, 0]);
        }
      } else {
        color[u] = 2;
        stack.pop();
      }
    }
  }
  return false;
}
```

Invariant: at any moment during DFS, the set of GRAY vertices forms a **directed simple path from some root** down to the current vertex. Encountering an edge to a GRAY vertex closes a loop — that's the cycle.

## Visual

Consider edges: `0 → 1 → 2 → 0` plus `3 → 4`.

```
   0 ──→ 1
   ↑     │
   │     ▼
   └──── 2

   3 ──→ 4
```

Run DFS from 0:
- Visit 0 (gray), 1 (gray), 2 (gray).
- From 2, edge `2 → 0`: colour of 0 is **gray** → back edge → cycle found!

If instead the graph were `0 → 1 → 2`, then 3 → 4 (no cycle):

```
   0 ──→ 1 ──→ 2

   3 ──→ 4
```

DFS visits 0, 1, 2 — no neighbour of 2 is gray; 2 turns black, then 1 black, then 0 black. Then DFS from 3 visits 4. No back edge ever encountered → no cycle.

## Which problems this approach solves in the real world

- **Build systems / Makefiles**: detect circular dependencies (gcc → ld → gcc).
- **Spreadsheet formulas**: catch cyclic cell references (A1 = B1 + 1, B1 = A1 + 1).
- **Module imports**: detect import cycles before runtime.
- **Database schema validation**: foreign-key cycles that would prevent integrity checks.
- **Workflow engines**: cycles in task graphs cause infinite scheduling loops.
- **Compiler call-graph analysis**: detect mutual recursion or inline-loops.

## Pros and cons

**Pros**
- O(V + E) total — fast for sparse graphs.
- O(V) memory.
- Reports a cycle *with* a specific edge that closes it — useful for error messages.
- The same DFS pass can produce a topological order (post-order reverse) when no cycle exists.

**Cons**
- Recursive DFS risks stack overflow on huge graphs — iterative version is more verbose.
- The "gray" vs "black" distinction is the source of the most common bug; using just a `visited` set wrongly flags cross edges as cycles.
- For *finding* the cycle's nodes (not just existence), you need a parent map alongside.

## Limitations

- Doesn't directly distinguish between **simple cycle** and longer cycles — it just detects presence.
- For undirected graphs, use the "DFS + parent" or Union-Find variants; the 3-colour rule is specific to directed graphs.
- For graphs with billions of edges, BFS-based Kahn's algorithm is more parallelisable.

## One example

**Problem**: Given `n` courses labeled `0..n-1` and a list of `prerequisites` where `[a, b]` means "to take course `a` you must take course `b` first", decide whether you can finish all `n` courses. Equivalently: does the directed graph (b → a) have no cycle?
Constraints: `1 ≤ n ≤ 2000`, `0 ≤ |prerequisites| ≤ 5000`.

**Input**: `n = 4`, `prerequisites = [[1,0], [2,1], [3,2], [1,3]]`
**Output**: `false` — edges form a cycle 1 → 3 → 2 → 1 (read 1 needs 3, 3 needs 2, 2 needs 1).

Actually let me re-examine: `[1, 0]` means "1 requires 0" → edge **0 → 1**. So edges are `0→1, 1→2, 2→3, 3→1`. There is a cycle `1 → 2 → 3 → 1`. Answer: **false**.

## Solution explanation

```python
def can_finish(n: int, prerequisites: list[list[int]]) -> bool:
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in prerequisites:
        adj[b].append(a)        # b → a edge

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(u: int) -> bool:
        color[u] = GRAY
        for v in adj[u]:
            if color[v] == GRAY: return True
            if color[v] == WHITE and dfs(v): return True
        color[u] = BLACK
        return False

    return not any(color[u] == WHITE and dfs(u) for u in range(n))
```

Walk-through on edges `0→1, 1→2, 2→3, 3→1`:

| step | call          | color before               | action                   | color after                 |
|------|---------------|----------------------------|--------------------------|------------------------------|
| 1    | dfs(0)        | [W,W,W,W]                 | gray 0                   | [G,W,W,W]                   |
| 2    | dfs(1)        | [G,W,W,W]                 | gray 1                   | [G,G,W,W]                   |
| 3    | dfs(2)        | [G,G,W,W]                 | gray 2                   | [G,G,G,W]                   |
| 4    | dfs(3)        | [G,G,G,W]                 | gray 3, look at edge 3→1 → color[1]=G → **back edge, cycle!** | return true |

The function bubbles `true` all the way up. Answer: `false` (cannot finish).

Correctness: an edge `u → v` is a back edge iff `v` is currently gray, which means `v` is an ancestor of `u` on the current DFS path. That gives a directed path `v ⇒ ... ⇒ u` plus the new edge `u → v`, completing a directed cycle. Conversely, if no back edge ever appears, every visit completes (turns black) before its ancestors return — the graph is a DAG.

- **Time**: O(V + E) — each vertex visited once, each edge examined once.
- **Space**: O(V) for the colour array and recursion stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Find Center of Star Graph** — warm-up on adjacency-list construction (no cycles but builds the muscle). | https://leetcode.com/problems/find-center-of-star-graph/ |
| Medium | **Course Schedule** — the canonical directed-cycle detection problem above. | https://leetcode.com/problems/course-schedule/ |
| Hard | **Reconstruct Itinerary** — DFS-based Eulerian path; requires careful cycle handling in a multigraph. | https://leetcode.com/problems/reconstruct-itinerary/ |
