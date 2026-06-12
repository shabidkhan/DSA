# Path-based

## Folder structure

```
03-Path-based/
├── README.md
├── 01-Path-sum/README.md
└── 02-Diameter/README.md
```

## What is this

Path-based problems ask questions about *sequences of connected nodes* in a tree rather than the tree as a whole. Two flavours dominate: root-to-leaf paths (which must reach a specific termination) and node-to-node paths that pass through some pivot (which may bend at any internal node). The first is solved by carrying state down; the second is solved by combining children's contributions at every node and tracking a global best.

The unifying idea is that for any path that bends at a node, the path is exactly `(left arm) + node + (right arm)`. So at each node you compute the best single-arm extension and update a global "best path through this node." The function returns the single-arm extension; the bend stays local.

## Why we use

- Captures both straight (root-to-leaf) and bent (any-to-any) path queries with one decomposition.
- The "return the straight extension, track the bent best globally" idiom resolves the classic dual-return problem cleanly.
- Works for sum-like, length-like, and product-like path metrics with the same skeleton.
- Avoids re-traversing the tree: every path through a node is considered exactly once at that node.

## How to implement

```text
best = -infinity   # global bend-here best

function armThroughOrSkip(node):
    if node is null: return 0
    L = max(0, armThroughOrSkip(node.left))    # 0 = skip negative arm
    R = max(0, armThroughOrSkip(node.right))
    best = max(best, node.val + L + R)         # path that bends at node
    return node.val + max(L, R)                # straight extension upward
```

The shape of `max(0, ...)` is path-sum specific; for diameter (counting edges/nodes) drop the gate and use heights directly. For "must end at a leaf" variants, only update `best` when both children are null.

Subpatterns in this folder:

- `01-Path-sum/` — root-to-leaf or any-to-any sum queries; existence, count, max.
- `02-Diameter/` — longest path in the tree measured by edges or nodes.

## Which problems this approach solves in the real world

- Finding the longest critical path in a project dependency tree (longest chain of blocking tasks).
- Identifying the highest-cost route through a decision tree for cost analysis.
- Computing the maximum signal path in a tree-shaped circuit or pipeline.
- Detecting the longest reply chain in a threaded comment tree.
- Finding the most expensive root-to-leaf branch in a tournament bracket.
- Computing the diameter of a hierarchical network for worst-case latency bounds.

## Pros and cons

**Pros**
- One traversal computes both the straight-arm return value and the bend-here best.
- Works on negative weights with a simple `max(0, arm)` gate.
- No global graph search needed — the tree shape forbids the path from revisiting nodes.
- Trivial to adapt to "sum equals K," "longest of length K," etc.

**Cons**
- Requires a non-local accumulator (`best`) which feels un-pure — must be careful in concurrent code.
- The "skip negative arm" trick is wrong when paths must include certain nodes or must span both subtrees.
- Postorder by construction — partial results are unavailable until the whole subtree is processed.
- Diameter and path-sum variants look similar but have subtly different base cases (edges vs. nodes; null vs. leaf).

## Limitations

- Only works on trees where each path is unique; on a DAG/graph use Dijkstra/Bellman-Ford instead.
- Cannot answer "is there ANY path with property X" cheaply if X is non-monotone.
- Carrying multiple path metrics (sum AND length AND product) requires tuple returns and bloats the recursion.
- Skewed trees produce O(n) recursion depth, risking stack overflow without iterative rewriting.
