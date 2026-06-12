# Segment Tree

## Folder structure

```
01-Segment-tree/
├── README.md
├── 01-Range-query/README.md
└── 02-Lazy-propagation/README.md
```

## What is this

A segment tree is a binary tree where each node stores an aggregate (sum, min, max, gcd, etc.) of a contiguous segment of an underlying array. Leaves hold single elements; an internal node holds the combined aggregate of its two children's segments. Built once in O(n), it answers any range aggregate query in O(log n) and supports point or range updates in O(log n) by walking from the leaf back up — or, with **lazy propagation**, by stopping at the highest node that fully covers the update range and deferring its push downward until needed.

Segment trees are the structural answer to a deceptively simple question: "What if the aggregate operation isn't invertible (so prefix sums don't help) or the underlying array is being updated between queries?" Prefix sums are O(1) read but O(n) update; a Fenwick tree handles invertible sums elegantly but struggles with min/max; the segment tree handles arbitrary associative aggregates with both reads and writes in logarithmic time.

## Why we use

- Both range query and range update in O(log n)
- Works for any associative operation (min, max, gcd, xor, sum, polynomial composition)
- Lazy propagation makes "range +x" and "range assign" updates also O(log n)
- Beats Fenwick tree on non-invertible operations like min/max

## How to implement

```text
# Iterative or recursive: recursive is clearer for variants
function build(node, l, r):
    if l == r:
        tree[node] = arr[l]
        return
    m = (l + r) / 2
    build(2*node, l, m)
    build(2*node+1, m+1, r)
    tree[node] = combine(tree[2*node], tree[2*node+1])

function query(node, l, r, ql, qr):
    if qr < l or r < ql: return identity
    if ql <= l and r <= qr: return tree[node]
    push_down(node)         # lazy variant only
    m = (l + r) / 2
    return combine(
        query(2*node,   l,   m, ql, qr),
        query(2*node+1, m+1, r, ql, qr)
    )

function update(node, l, r, ul, ur, val):
    if ur < l or r < ul: return
    if ul <= l and r <= ur:
        apply(node, val)    # mark lazy and update node's aggregate
        return
    push_down(node)
    m = (l + r) / 2
    update(2*node,   l,   m, ul, ur, val)
    update(2*node+1, m+1, r, ul, ur, val)
    tree[node] = combine(tree[2*node], tree[2*node+1])
```

Subpatterns in this folder:

- **01-Range-query** — point updates with range aggregate queries; the bread-and-butter form
- **02-Lazy-propagation** — range updates with range queries; each node carries a pending operation that pushes to children only when traversed

## Which problems this approach solves in the real world

- Real-time analytics dashboards over a streaming bucketed metric
- Online judges' range-min / range-sum / range-max queries with updates
- Time-series queries with interval edits (set this hour's data to X)
- 2D segment trees for geographic min/max queries on grid sensor data
- Game-engine collision broadphase via interval skylines
- Polynomial evaluation under range edits in symbolic computation

## Pros and cons

**Pros**

- General: any associative monoid works
- Both read and write in O(log n)
- Lazy propagation extends to range updates with no asymptotic cost
- Each node is small (one aggregate + optional lazy tag)

**Cons**

- Implementation is longer and more error-prone than Fenwick
- Memory usage ~4n (recursive) or 2n (iterative); Fenwick uses n
- Debugging lazy pushes is notoriously tricky
- Constants are larger than prefix-sum / Fenwick variants

## Limitations

- Underlying array is fixed-size; insertions/deletions require a different structure
- Doesn't speed up non-associative operations
- Cache behavior on large trees is worse than a Fenwick array
- 2D / dynamic / persistent variants multiply implementation complexity
