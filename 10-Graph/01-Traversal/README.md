# Graph Traversal

## Folder structure

```
01-Traversal/
├── README.md
├── 01-BFS/README.md
└── 02-DFS/README.md
```

## What is this

Traversal is the foundation of every graph algorithm: visit each reachable vertex exactly once while respecting the edges. BFS and DFS are the two canonical orders. BFS uses a FIFO queue and expands the frontier one layer at a time, giving shortest-path-by-edge-count for free. DFS uses a stack (explicit or implicit via recursion) and follows one path to its end before backtracking, exposing structural properties like discovery/finish times, cycles, and topological order.

Almost every higher-level graph problem — shortest path, cycle detection, connectivity, bipartiteness, topological sort, articulation points — is either BFS or DFS plus a small amount of bookkeeping. Picking the right one is mostly about whether you need layered distances (BFS) or structural properties (DFS).

## Why we use

- BFS gives unweighted shortest-path distance in a single sweep — provably optimal.
- DFS exposes structural facts (cycles, components, back-edges, finish order) that BFS hides.
- Both are O(V + E) — linear in the size of the graph.
- Together they cover the vast majority of graph problems with minimal extra machinery.

## How to implement

```text
function bfs(start, adj):
    seen = {start}; q = [start]; dist = {start: 0}
    while q:
        u = q.popLeft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); dist[v] = dist[u] + 1; q.push(v)
    return dist

function dfs(start, adj):
    seen = set(); stack = [start]
    while stack:
        u = stack.pop()
        if u in seen: continue
        seen.add(u); visit(u)
        for v in adj[u]:
            if v not in seen: stack.push(v)
```

Subpatterns in this folder:

- `01-BFS/` — layer-by-layer expansion; unweighted shortest path, level grouping, multi-source spread.
- `02-DFS/` — depth-first walk; component labelling, cycle detection, topological order, tree/back/forward/cross-edge classification.

## Which problems this approach solves in the real world

- Web crawling and link-graph analysis.
- Shortest-hop routing in an unweighted overlay (BFS).
- Detecting circular dependencies in a build system or DI container (DFS).
- Finding all reachable resources from a given starting state (permission graphs, file systems).
- Connected-component labelling for image segmentation.
- Topological ordering of compile units, schema migrations, or task pipelines (DFS post-order).

## Pros and cons

**Pros**
- Both are linear-time in V + E — hard to beat asymptotically.
- The skeletons are tiny and reusable across dozens of problems.
- BFS gives optimal unweighted distances; DFS gives optimal structural classification.
- Easy to extend with extra state (parent pointers, distances, colours, timestamps).

**Cons**
- DFS recursion depth = longest path; stack overflows on adversarial graphs without iterative rewrite.
- BFS memory = width of the widest layer, which can balloon on dense graphs.
- Neither alone handles weighted shortest paths — need Dijkstra/Bellman-Ford.
- Naive `visited` checks miss subtleties on multigraphs and self-loops.

## Limitations

- Not for weighted shortest paths; use Dijkstra (non-negative) or Bellman-Ford (general).
- BFS does not see structural properties like back-edges or strongly connected components — DFS does.
- DFS order on the same graph can differ between adjacency-list orderings; tests must allow it.
- On infinite or implicit graphs (game states), explicit bookkeeping of "visited" can blow up memory.
