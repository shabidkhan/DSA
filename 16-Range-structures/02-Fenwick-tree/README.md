# Fenwick Tree (Binary Indexed Tree)

## Folder structure

```
02-Fenwick-tree/
├── README.md
└── 01-Prefix-query/README.md
```

## What is this

A Fenwick tree — also known as a Binary Indexed Tree (BIT) — is a 1-indexed array `bit[1..n]` where each position is responsible for a power-of-two-sized range determined by the **lowest set bit** of its index. To query the prefix sum up to index `i`, walk down by subtracting `i & -i` and accumulating; to update, walk up by adding `i & -i` and propagating. Each walk takes O(log n) steps because each step flips one bit, and at most log n bits exist.

The Fenwick tree is the minimalist's segment tree: same O(log n) update and prefix-query complexity, but implemented in a handful of lines using one tight loop and a single `lowbit` trick. It is the right choice whenever the aggregate is **invertible** (sum, XOR, multiplication mod prime), because range queries reduce to two prefix queries. For non-invertible aggregates like min/max, prefer a segment tree.

## Why we use

- Concise: full implementation in ~10 lines
- Memory tight: a single array of size n+1, no node objects
- O(log n) update, O(log n) prefix query, O(log n) range query (two prefixes)
- The `i & -i` step is one CPU instruction; constants are small

## How to implement

```text
# 1-indexed; bit has length n+1, initialized to 0
function update(i, delta):
    while i <= n:
        bit[i] += delta
        i += i & -i           # jump to next responsible index

function prefixSum(i):
    s = 0
    while i > 0:
        s += bit[i]
        i -= i & -i           # peel off lowest set bit
    return s

function rangeSum(l, r):
    return prefixSum(r) - prefixSum(l - 1)

# Build in O(n) instead of O(n log n)
function build(arr):
    for i = 1..n:
        bit[i] += arr[i-1]
        j = i + (i & -i)
        if j <= n: bit[j] += bit[i]
```

Subpatterns in this folder:

- **01-Prefix-query** — point update + prefix/range sum queries, the canonical use; also covers the range-update + point-query inversion trick using a difference array, and the order-statistics trick using a BIT indexed by value

## Which problems this approach solves in the real world

- Counting inversions in a permutation in O(n log n)
- Online order-statistics over an integer-valued stream (k-th smallest seen so far)
- Real-time scoreboard prefix-sum queries (total points up to rank r)
- Dynamic frequency tables in compression and statistics
- Subarray-sum queries with point updates in spreadsheet engines
- Computing 2D rectangle sums via 2D BIT in image and grid processing

## Pros and cons

**Pros**

- Tiny implementation — fewer bugs in interview pressure
- Memory and constants smaller than a segment tree
- Build in O(n) is possible with the propagation trick
- Generalizes cleanly to 2D and difference-array tricks

**Cons**

- Only works for invertible aggregates (sum, XOR, etc.)
- Cannot answer "min/max in range" directly
- 1-indexing is unintuitive in 0-indexed languages
- Range updates with range queries require two BITs and a non-obvious formula

## Limitations

- Not a replacement for segment tree on non-invertible monoids
- Doesn't support inserting / deleting array positions
- Persistent or merge-able variants are awkward
- Reading the code without comments is harder than reading a segment tree
