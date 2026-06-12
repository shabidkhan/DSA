# Minimum Spanning Tree

## Folder structure

```
05-Spanning-tree/
├── README.md
├── 01-Kruskal/README.md
└── 02-Prim/README.md
```

## What is this

A minimum spanning tree (MST) of a connected weighted undirected graph is a subset of edges that connects every vertex with the smallest possible total weight, and contains no cycles. Two classic algorithms compute it. Kruskal sorts edges by weight and adds the smallest that does not form a cycle, using Union-Find to check connectivity. Prim grows the tree from a starting vertex one edge at a time, always adding the lightest edge leaving the current tree, using a priority queue.

Both are greedy and both rely on the *cut property*: for any cut of the graph, the lightest edge crossing the cut is in some MST. Kruskal's cuts are implicit (whichever cut separates the two endpoints of the next edge); Prim's cut is explicit (the tree vs. the rest).

## Why we use

- An MST is the minimum-cost way to keep a network connected.
- Both algorithms are provably optimal under the cut property.
- Kruskal pairs naturally with Union-Find, a useful structure on its own.
- Prim runs in O((V+E) log V) with a heap — fast on sparse graphs.

## How to implement

```text
# Kruskal
function kruskal(V, edges):
    sort(edges by weight)
    uf = UnionFind(V)
    mst = []
    for (u, v, w) in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v); mst.add((u, v, w))
    return mst

# Prim
function prim(V, adj, start=0):
    inTree = {start}; pq = [(w, start, v) for v, w in adj[start]]
    mst = []
    while pq and len(inTree) < V:
        w, u, v = popMin(pq)
        if v in inTree: continue
        inTree.add(v); mst.add((u, v, w))
        for (x, w2) in adj[v]:
            if x not in inTree: push(pq, (w2, v, x))
    return mst
```

Subpatterns in this folder:

- `01-Kruskal/` — sort edges, Union-Find to detect cycles. Better when the graph is sparse and edges are pre-sorted.
- `02-Prim/` — grow the tree from a seed via heap of crossing edges. Better when the graph is dense and given as an adjacency list.

## Which problems this approach solves in the real world

- Designing low-cost network topologies (cable, fiber, road).
- Cluster analysis (single-linkage clustering = MST cut).
- Approximation algorithms for TSP (MST gives a 2-approximation).
- Image segmentation via graph cuts.
- Backbone selection in distributed systems to minimize total connection cost.
- Designing utility networks (water, power) under a connectivity constraint.

## Pros and cons

**Pros**
- Greedy yet optimal — easy correctness proofs via the cut property.
- Both run in O(E log V) — fast in practice.
- MST is unique-up-to-ties on graphs with distinct weights.
- Each algorithm gives a useful by-product: Kruskal yields a Union-Find structure; Prim yields a per-vertex parent pointer.

**Cons**
- Kruskal requires sorting all edges — slow when |E| ≫ |V| and edges aren't pre-sorted.
- Prim's heap-based variant requires a decrease-key or lazy deletion.
- Neither handles directed graphs (need Edmonds' algorithm for those).
- MST is undefined for disconnected graphs without picking a spanning forest convention.

## Limitations

- Only works for undirected connected graphs.
- Does not minimize maximum edge or other non-additive objectives.
- Dynamic edge additions/removals require specialized link-cut trees, not these algorithms.
- Cannot handle constraints like "must include this edge" without modification.
