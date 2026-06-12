# Cycle detection in undirected graphs (DFS-parent OR Union-Find)

## What is this

In an undirected graph, a cycle is a closed walk of length ≥ 3 using **distinct edges**. Two standard detection algorithms:

1. **DFS + parent tracking**: traverse with DFS; for each neighbour `v` of `u`, if `v` is visited **and** `v` is not the parent of `u`, then `u — v` closes a cycle. The parent check is essential — without it, the edge you just used to arrive at `u` would falsely look like a cycle (since the graph is undirected, the edge appears in both directions).

2. **Union-Find (disjoint set union)**: process edges in any order; for edge `u — v`, if `u` and `v` are already in the same component, the edge closes a cycle; otherwise union them. Conceptually building a spanning forest — a cycle is created the first time an edge would merge two already-connected nodes.

Both run in near-linear time and are equally valid; choice depends on whether you have a list of edges (Union-Find shines) or an adjacency list (DFS shines).

## Why we use

- O(V + E) DFS, O(E α(V)) Union-Find — both effectively linear.
- DFS-parent gives the **actual cycle nodes** if you reconstruct via the parent map.
- Union-Find lets you process edges in a stream — useful when the graph arrives incrementally.
- Both extend to "find all bridges / articulation points" (DFS) and "min spanning forest" (Union-Find with edge weights).

## How to implement

**DFS-parent:**

```
visited = [False] * n
def dfs(u, parent):
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            if dfs(v, u): return True
        elif v != parent:
            return True       # cycle
    return False

for u in 0..n-1:
    if not visited[u] and dfs(u, -1):
        return True
return False
```

**Union-Find:**

```
parent = list(0..n-1)
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False   # already connected → cycle
    parent[ra] = rb
    return True

for (u, v) in edges:
    if not union(u, v):
        return True
return False
```

Python — DFS-parent:

```python
def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    visited = [False] * n

    def dfs(u: int, parent: int) -> bool:
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

JavaScript — Union-Find:

```javascript
function hasCycleUF(n, edges) {
  const parent = Array.from({ length: n }, (_, i) => i);
  const find = (x) => {
    while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
  };
  for (const [u, v] of edges) {
    const ru = find(u), rv = find(v);
    if (ru === rv) return true;
    parent[ru] = rv;
  }
  return false;
}
```

Invariant (DFS): `visited[u] && v != parent` means we've reached `v` via two distinct paths — one through `parent`, the other through `u → v` — which is a cycle. Invariant (UF): at any time, `parent` represents a spanning forest; adding an edge inside an existing tree closes a cycle.

## Visual

Edges: `0—1, 1—2, 2—0, 3—4`.

```
   0 ─── 1
   │     │
   └── 2 ┘

   3 ─── 4
```

DFS from 0:
- Visit 0 (parent=-1); look at 1. Not visited → recurse.
- At 1 (parent=0); look at 0: visited and 0 == parent → ignore. Look at 2: not visited → recurse.
- At 2 (parent=1); look at 1: visited and 1 == parent → ignore. Look at 0: visited and 0 ≠ parent (1) → **cycle!**

Union-Find on the same edges:
- Edge 0—1: union(0, 1) → parent={1,1,2,3,4}.
- Edge 1—2: union(1, 2) → parent={1,2,2,3,4}.
- Edge 2—0: find(2) → 2, find(0) → find(1) → 2; equal → **cycle!**

Both methods detect the same cycle.

## Which problems this approach solves in the real world

- **Network topology**: detect redundant links in a LAN (forms a loop).
- **Social graphs**: find friendship cycles for clustering / community detection.
- **Roadway redundancy**: detect roads that form rings (useful for traffic balancing).
- **Spreadsheet dependency graphs** (undirected version, when ranges link symmetrically).
- **MST construction**: Kruskal's uses Union-Find precisely to *avoid* adding cycle-closing edges.
- **Tree validation**: a graph with `n` nodes is a tree iff it has `n-1` edges **and** no cycle.

## Pros and cons

**Pros**
- Both methods O(V + E) (UF is O(E α(V)) which is effectively constant).
- DFS reveals the structure (cycle nodes available via parent map).
- Union-Find handles streaming edges and merges across DFS traversals.
- Mixes cleanly with other passes: Union-Find for connectivity, DFS for trees vs cycles.

**Cons**
- DFS-parent only checks the *immediate* parent — for multigraphs (two edges between same pair), you must track edge-id, not just node parent.
- Union-Find doesn't tell you *which* edges form the cycle without extra bookkeeping.
- For large graphs, recursive DFS may stack-overflow; iterate.

## Limitations

- Multigraphs (parallel edges) break the simple parent check — two edges between u and v are themselves a cycle in many definitions.
- Self-loops (edge from u to itself) are always a cycle — both methods handle this if you check `u != v` carefully when building adjacency / unioning.
- For weighted "minimum-weight cycle" or "longest cycle", these algorithms don't help directly.

## One example

**Problem**: Given `n` nodes (labeled 0..n-1) and a list of undirected edges, determine if the graph is a **valid tree**. A valid tree must be: (1) connected, (2) contain no cycles, (3) have exactly `n - 1` edges.
Constraints: `1 ≤ n ≤ 2000`, `0 ≤ |edges| ≤ 5000`.

**Input**: `n = 5`, `edges = [[0,1], [0,2], [0,3], [1,4]]`
**Output**: `true` (tree).

**Input**: `n = 5`, `edges = [[0,1], [1,2], [2,3], [1,3], [1,4]]`
**Output**: `false` (cycle 1-2-3-1).

## Solution explanation

Using Union-Find — process each edge, fail on a cycle, then verify connectivity by checking only one root remains:

```python
def valid_tree(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False                # tree must have exactly n-1 edges
    parent = list(range(n))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False            # cycle
        parent[ru] = rv
    return True                     # n-1 edges + no cycle ⇒ connected tree
```

Walk-through on `n=5, edges=[[0,1],[1,2],[2,3],[1,3],[1,4]]`:

| step | edge | find(u), find(v) | same? | union → parent          |
|------|------|------------------|-------|-------------------------|
| 1    | 0,1  | 0, 1             | no    | parent[0]=1 → [1,1,2,3,4]|
| 2    | 1,2  | 1, 2             | no    | parent[1]=2 → [1,2,2,3,4]|
| 3    | 2,3  | 2, 3             | no    | parent[2]=3 → [1,2,3,3,4]|
| 4    | 1,3  | find(1) climbs 1→2→3, find(3)=3 | yes | **cycle → return false** |

Correctness: a graph with exactly `n − 1` edges is a tree if and only if it is acyclic (which then forces connectivity by counting). Union-Find detects the first cycle-closing edge by checking whether the two endpoints already share a root. Path compression keeps `find` near-constant amortised.

- **Time**: O(n + m · α(n)) ≈ O(n + m).
- **Space**: O(n) for the parent array.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Find if Path Exists in Graph** — basic connectivity check, no cycle detection but the same building block. | https://leetcode.com/problems/find-if-path-exists-in-graph/ |
| Medium | **Graph Valid Tree** — the canonical problem above. | https://leetcode.com/problems/graph-valid-tree/ |
| Hard | **Redundant Connection II** — directed version that adds two failure modes (cycle and double-parent); Union-Find with parent tracking. | https://leetcode.com/problems/redundant-connection-ii/ |
