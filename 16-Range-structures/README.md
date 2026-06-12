# Range Structures

## Folder structure

```
16-Range-structures/
├── README.md
├── 01-Segment-tree/
│   ├── 01-Range-query/README.md
│   └── 02-Lazy-propagation/README.md
└── 02-Fenwick-tree/
    └── 01-Prefix-query/README.md
```

## What is this

Range structures answer queries about contiguous subranges of an array — sum, min, max, XOR, or any associative function — in O(log n) per query, while supporting point or range updates in similar time. The two workhorses here are **segment trees** (most flexible, supports lazy propagation for range updates) and **Fenwick trees** (also called BITs — Binary Indexed Trees: simpler, smaller, faster constants, but limited to prefix-aggregatable operations).

When the array is static, prefix-based arrays give O(1) queries with no updates. When updates are needed, range structures step in. The family is the answer to "I need fast range aggregates AND point/range updates" — without them, every update would invalidate any prefix-sum cache and force O(n) work.

## Why we use

- O(log n) for both query and update — vastly better than O(n) per update with prefix sums.
- Segment trees support lazy propagation: range updates in O(log n).
- Fenwick trees use less memory (one array of size n+1) and have tiny constants.
- Composable: any associative operation (sum, min, gcd, matrix multiply) works.

## How to implement

Pick by operation and updates:

```
static array, only queries        — prefix sum/XOR/min (O(1) query, no updates)
point update + range query        — Fenwick tree (sum, XOR, etc.)
range update + range query        — segment tree with lazy propagation
non-prefix-aggregatable ops       — segment tree (min, max, gcd)
2D updates / queries              — 2D Fenwick or 2D segment tree
```

Subpatterns in this folder:

- **01-Segment-tree** — flexible range queries; lazy propagation for range updates.
- **02-Fenwick-tree** — compact prefix-aggregate structure for point updates and prefix queries.

## Which problems this approach solves in the real world

- Real-time analytics over moving time windows.
- Order-book aggregate queries (volume above price X).
- Range-count queries in databases with frequent updates.
- Geographic information systems (range-min/max queries over coordinates).
- Inventory aggregations with frequent restocks.
- Range-sum / k-th-element queries in competitive programming.

## Pros and cons

**Pros**
- O(log n) query and update — unmatched for dynamic range aggregates.
- Lazy propagation unlocks O(log n) range updates.
- Fenwick trees are tiny and extremely fast in practice.
- Generalise to many associative operations.

**Cons**
- Implementation is non-trivial; off-by-one errors are common.
- Segment trees use ~4n memory; Fenwick uses n+1.
- Lazy propagation logic is error-prone.
- Fenwick can't easily handle non-prefix-aggregatable operations (min, max).

## Limitations

- Operations must be associative; non-associative needs different structures.
- 2D variants are memory-heavy.
- Persistent variants are advanced and rarely needed in interviews.
- For pure static arrays, prefix arrays are simpler and faster.
