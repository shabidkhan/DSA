# Union-Find (Disjoint Set Union)

## What is this

Union-Find (a.k.a. Disjoint Set Union, DSU) is a data structure that maintains a collection of disjoint sets supporting two operations: `find(x)` returns the representative of `x`'s set, and `union(x, y)` merges the two sets containing `x` and `y`. With path compression in `find` and union by rank/size, each operation runs in amortised O(α(n)) where α is the inverse Ackermann function — effectively constant.

DSU shines on connectivity questions over a stream of edges and on Kruskal's minimum spanning tree algorithm. It is also the cleanest way to detect connected components dynamically.

## Why we use

- Near-constant amortised time per operation
- Trivial to implement (two arrays of length n)
- Handles dynamic connectivity (add edges, ask "are u and v connected?")
- Backbone of Kruskal's MST algorithm

## How to implement

```
parent[i] = i
rank[i] = 0

find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x

union(x, y):
    rx, ry = find(x), find(y)
    if rx == ry: return False
    if rank[rx] < rank[ry]: rx, ry = ry, rx
    parent[ry] = rx
    if rank[rx] == rank[ry]: rank[rx] += 1
    return True
```

```python
class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True
```

Invariant: each root represents exactly one connected component. Path compression flattens the tree on every `find`, and union-by-rank keeps trees shallow, jointly bounding the cost to O(α(n)) per op.

## Which problems this approach solves in the real world

- Connectivity in social networks: are two users in the same friend cluster?
- Image segmentation: merge pixels into regions of similar color
- Equivalence-class tracking in compilers (type unification, alias analysis)
- Network reliability: detect when adding a link merges two previously isolated subnets
- Kruskal's algorithm for minimum-cost network design (laying cables / pipes)

## Pros and cons

**Pros**
- Nearly O(1) per operation in practice
- Tiny code: two arrays and ~15 lines
- Streamable: handles edges arriving online

**Cons**
- Does not support efficient deletion of edges (use link-cut trees instead)
- Iteration over a component's members requires extra bookkeeping
- Without path compression / rank, worst-case becomes O(n) per op

## Limitations

- Edge deletions / dynamic disconnection are expensive
- Cannot directly answer queries about the structure of a component (size, depth, members) without auxiliary data
- Not suitable for weighted-edge merges that require choosing a "better" representative beyond rank

## One example

Problem: There are `n` cities labelled `0..n-1` and a list of edges. Two cities are in the same province if connected directly or transitively. Return the number of provinces.

```
Input:  n = 5, edges = [(0, 1), (1, 2), (3, 4)]
Output: 2     ({0, 1, 2} and {3, 4})
Constraints: 1 <= n <= 200, 0 <= len(edges) <= n * (n - 1) / 2
```

## Solution explanation

```python
class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

def count_provinces(n: int, edges: list[tuple[int, int]]) -> int:
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    return dsu.components
```

Each successful `union` reduces the component count by one. The final count is `n - (number of successful unions)`.

Walkthrough for `n = 5`, `edges = [(0,1), (1,2), (3,4)]`. `parent = [0,1,2,3,4]`, `components = 5`.

| Step | Edge   | find(u), find(v) | parent after            | components |
|------|--------|------------------|-------------------------|------------|
| init |        |                  | [0, 1, 2, 3, 4]         | 5          |
| 1    | (0, 1) | 0, 1             | [0, 0, 2, 3, 4]         | 4          |
| 2    | (1, 2) | 0, 2             | [0, 0, 0, 3, 4]         | 3          |
| 3    | (3, 4) | 3, 4             | [0, 0, 0, 3, 3]         | 2          |

Final answer = 2. Time O(E * α(n)), space O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find if Path Exists in Graph (LeetCode 1971) | https://leetcode.com/problems/find-if-path-exists-in-graph/ |
| Medium | Number of Provinces (LeetCode 547) | https://leetcode.com/problems/number-of-provinces/ |
| Hard | Redundant Connection II (LeetCode 685) | https://leetcode.com/problems/redundant-connection-ii/ |
