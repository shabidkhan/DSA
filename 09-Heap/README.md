# Heap Patterns

## Folder structure

```
09-Heap/
├── README.md
├── 01-Top-K/README.md
├── 02-Greedy-heap/
│   ├── 01-Task-scheduler/README.md
│   ├── 02-Meeting-rooms/README.md
│   ├── 03-Reorganize-string/README.md
│   └── 04-Huffman-encoding/README.md
├── 03-K-way-merge/README.md
└── 04-Two-heaps/README.md
```

## What is this

A heap (priority queue) is a tree-shaped container that always keeps the smallest (min-heap) or largest (max-heap) element at the root, with O(log n) insertion and removal of that root. The "always the best element on top" property is the secret behind algorithms where you need to repeatedly pull the most urgent / cheapest / smallest item: Top-K problems, scheduling, K-way merge, Dijkstra, Prim, Huffman encoding.

The three subpatterns are: Top K (keep a heap of size k for "k largest/smallest"), Greedy + Heap (repeatedly take the best option for problems like Task Scheduler, Meeting Rooms II, Reorganize String, Huffman), and K-way Merge (merge multiple sorted streams).

## Why we use

- O(log n) per "give me the smallest/largest" is much better than O(n) scans.
- A bounded-size heap (size k) gives O(n log k) Top-K in O(k) memory.
- Plays beautifully with greedy: "always take the best now" needs constant best-of access.
- Pairs with hash maps for efficient Dijkstra and Prim implementations.

## How to implement

Pick by the operation you need on each step:

```
top K              — fixed-size heap; push and pop-once-over-k
greedy + heap      — at each step, pop the best, push new options derived from it
K-way merge        — heap of (value, list_index, element_index) entries
```

Subpatterns in this folder:

- **01-Top-K** — k largest/smallest with a size-k heap.
- **02-Greedy-heap** — task scheduler, meeting rooms II, reorganize string, Huffman.
- **03-K-way-merge** — merge K sorted lists/streams.
- **04-Two-heaps** — running median with a max-heap (lower half) + min-heap (upper half).

## Which problems this approach solves in the real world

- OS process schedulers (CPU/IO priority queues).
- Top-N analytics queries (top spenders, top trending posts).
- Order books and event simulators in finance.
- Dijkstra's algorithm for routing (maps, networks, games).
- Stream-median calculation for monitoring percentiles.
- Huffman encoding in compressors (gzip, JPEG).

## Pros and cons

**Pros**
- O(log n) push and pop; O(1) peek.
- Bounded heap gives constant memory for streaming top-K.
- Array-backed implementation is cache-friendly.
- Pairs naturally with greedy algorithms.

**Cons**
- No fast "find arbitrary element" — only the root is O(1).
- Decrease-key requires extra bookkeeping (often via lazy deletion).
- Wrong heap direction (min vs max) flips your algorithm silently.
- Iteration order is not sorted.

## Limitations

- Cannot replace a sorted container — only the extreme is fast.
- Custom comparators require care to remain a strict weak ordering.
- Memory locality is worse than arrays for very large heaps.
- Concurrent heaps are notoriously hard to scale.
