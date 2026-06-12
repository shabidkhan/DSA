# Shortest Path

## Folder structure

```
04-Shortest-path/
├── README.md
├── 01-Dijkstra/README.md
├── 02-Bellman-Ford/README.md
└── 03-Floyd-Warshall/README.md
```

## What is this

Shortest-path algorithms compute the minimum-cost route from one vertex (or every vertex) to another in a weighted graph. The three classic algorithms cover different settings: Dijkstra for single-source with non-negative weights (O((V+E) log V) with a heap), Bellman-Ford for single-source with possibly negative weights and negative-cycle detection (O(V·E)), and Floyd-Warshall for all-pairs (O(V³)) on dense graphs.

The choice is driven by three knobs: source (one vs all), weight sign (non-negative vs general), and density (sparse vs dense). For sparse graphs with non-negative weights, Dijkstra wins. For graphs with potentially negative edges, only Bellman-Ford (or Johnson's algorithm) is safe. For dense all-pairs queries on small V, Floyd-Warshall is the simplest correct choice.

## Why we use

- Each algorithm is asymptotically optimal in its niche.
- Dijkstra's "relax via a priority queue" pattern is reused everywhere (A*, Prim).
- Bellman-Ford is the only one of the three that handles negative weights or detects negative cycles.
- Floyd-Warshall computes the full V×V distance matrix in a few lines of code.

## How to implement

```text
# Dijkstra (non-negative weights)
function dijkstra(src, adj):
    dist = {v: inf for v}; dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = popMin(pq)
        if d > dist[u]: continue
        for (v, w) in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w; push(pq, (dist[v], v))
    return dist

# Bellman-Ford (handles negative weights)
function bellmanFord(src, V, edges):
    dist = {v: inf for v}; dist[src] = 0
    repeat V-1 times:
        for (u, v, w) in edges:
            if dist[u] + w < dist[v]: dist[v] = dist[u] + w
    for (u, v, w) in edges:
        if dist[u] + w < dist[v]: signal "negative cycle"
    return dist

# Floyd-Warshall (all-pairs)
function floyd(V, w):
    d = copy(w)
    for k in V:
        for i in V:
            for j in V:
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d
```

Subpatterns in this folder:

- `01-Dijkstra/` — heap-based single-source on non-negative weights.
- `02-Bellman-Ford/` — V-1 edge-relaxation rounds; negative cycle detection.
- `03-Floyd-Warshall/` — dynamic-programming all-pairs in O(V³).

## Which problems this approach solves in the real world

- Routing in road networks (OSRM, OSM-based map services).
- Network packet routing (OSPF uses Dijkstra; RIP uses Bellman-Ford).
- Currency arbitrage detection (negative-cycle search via Bellman-Ford on log-prices).
- Min-latency path discovery in service-mesh topologies.
- Game-AI pathfinding (Dijkstra-with-heuristic = A*).
- Precomputing distance tables in dense graphs for O(1) lookup (Floyd-Warshall on small V).

## Pros and cons

**Pros**
- Each algorithm is the right tool for a well-defined setting.
- Dijkstra with a heap is fast in practice on sparse graphs.
- Bellman-Ford uniquely handles negative weights and detects negative cycles.
- Floyd-Warshall is shockingly short to write — three nested loops.

**Cons**
- Dijkstra is wrong on negative edges (silently, no error).
- Bellman-Ford is O(V·E) — slow on dense graphs.
- Floyd-Warshall is O(V³) memory and time — infeasible for V > ~1000.
- Reconstructing paths needs predecessor maps, which doubles memory and complicates code.

## Limitations

- Dijkstra requires non-negative weights — even one negative edge breaks correctness.
- Bellman-Ford slows down on dense graphs; SPFA can be faster in practice but has bad worst case.
- Floyd-Warshall does not scale beyond a few thousand nodes; sparse graphs should use repeated Dijkstra.
- None handle dynamic edges natively — additions/deletions force re-running from scratch.
