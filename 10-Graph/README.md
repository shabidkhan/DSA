# Graph Patterns

## Folder structure

```
10-Graph/
├── README.md
├── 01-Traversal/
│   ├── 01-BFS/README.md
│   └── 02-DFS/README.md
├── 02-Cycle-detection/
│   ├── README.md
│   ├── 01-Directed/README.md
│   └── 02-Undirected/README.md
├── 03-Topological-sort/
│   ├── README.md
│   ├── 01-Kahn/README.md
│   └── 02-DFS-based/README.md
├── 04-Shortest-path/
│   ├── 01-Dijkstra/README.md
│   ├── 02-Bellman-Ford/README.md
│   └── 03-Floyd-Warshall/README.md
├── 05-Spanning-tree/
│   ├── 01-Kruskal/README.md
│   └── 02-Prim/README.md
├── 06-Union-find/README.md
├── 07-Bipartite/README.md
├── 08-Multi-source-BFS/README.md
└── 09-0-1-BFS/README.md
```

## What is this

A graph is a set of vertices connected by edges, and almost every "relationship" problem is a graph problem in disguise: roads between cities, friendships, dependencies between tasks, web links, citation networks, electrical circuits. Graph problems split into nine recurring families: traversal (BFS/DFS), cycle detection (directed/undirected), topological sort (Kahn / DFS-based), shortest path (Dijkstra / Bellman-Ford / Floyd-Warshall), spanning trees (Kruskal / Prim), union-find, bipartiteness, multi-source BFS, and 0-1 BFS.

The hardest part of graph problems is usually modelling — turning the prose into vertices and edges — and choosing the right algorithm for the edge-weight structure (unweighted? non-negative weights? negative weights? bidirectional?). Once the model is right, the algorithm is usually mechanical.

## Why we use

- Real-world relationships almost always form a graph.
- Each algorithm has a sharp specialisation (BFS for unweighted shortest path, Dijkstra for non-negative weights, etc.).
- Topological sort solves dependency resolution (build systems, course scheduling).
- Union-find gives near-O(1) connectivity queries.

## How to implement

Pick by edge-weight semantics:

```
unweighted shortest      — BFS
non-negative weights     — Dijkstra (heap)
negative weights allowed — Bellman-Ford
all-pairs                — Floyd-Warshall
dependency ordering      — topological sort (Kahn or DFS)
connectivity / MST       — union-find / Kruskal / Prim
two-colorability         — bipartite check via BFS
multiple sources         — multi-source BFS
0/1 edge weights         — 0-1 BFS (deque)
```

Subpatterns in this folder:

- **01-Traversal** — BFS and DFS.
- **02-Cycle-detection** — directed (3-color DFS) and undirected (DFS-parent or union-find).
- **03-Topological-sort** — Kahn (BFS) and DFS-based.
- **04-Shortest-path** — Dijkstra, Bellman-Ford, Floyd-Warshall.
- **05-Spanning-tree** — Kruskal and Prim.
- **06-Union-find** — disjoint-set union.
- **07-Bipartite** — two-coloring check.
- **08-Multi-source-BFS** — start from many sources simultaneously.
- **09-0-1-BFS** — 0/1 weight shortest path with a deque.

## Which problems this approach solves in the real world

- GPS routing (Dijkstra over road networks).
- Build systems (topological sort of compile dependencies).
- Social network analytics (BFS for "degrees of separation").
- Network reliability (union-find, min-cut).
- Cycle detection in compilers (deadlocks, import cycles).
- Recommendation systems via graph embeddings (preprocessed by these algorithms).

## Pros and cons

**Pros**
- Each subpattern has a tight, well-understood complexity bound.
- Adjacency lists scale to millions of vertices on commodity hardware.
- Algorithms compose: shortest path uses BFS, MST uses union-find.
- Many problems collapse to "BFS/DFS with a clever visited rule".

**Cons**
- Modelling errors (missed edges, wrong weights) dominate bug reports.
- Dense vs sparse representation choice matters: list vs matrix.
- Many algorithms have edge cases for disconnected components.
- Negative weights and cycles need specialised algorithms (Bellman-Ford).

## Limitations

- Dijkstra fails with negative edges (it produces wrong results, not just slow ones).
- BFS doesn't work for weighted shortest path.
- Topological sort exists only for DAGs.
- Distributed graphs (web-scale) need fundamentally different algorithms (Pregel/Giraph).
