# Queue Patterns

## Folder structure

```
05-Queue/
├── README.md
├── 01-FIFO/README.md
├── 02-Level-wise/README.md
├── 03-Circular-queue/README.md
└── 04-Deque/README.md
```

## What is this

A queue is a FIFO (first-in, first-out) container; a deque is its double-ended generalisation (push/pop from either end). The two are the natural fit for any process where "what arrived first should be handled first" — BFS, level-order traversal, scheduling, buffering, and sliding-window maximum/minimum problems.

The four subpatterns here are: FIFO basic queue (any breadth-first algorithm), level-wise BFS (process all current-level items before next), circular queues (fixed-size ring buffers for streams), and deques (the engine behind monotonic-window O(n) tricks like Sliding Window Maximum).

## Why we use

- BFS over graphs and trees is mechanical once you have a queue.
- Level-order tree problems become single-loop FIFO walks.
- Circular queues give O(1) amortised buffering for streams.
- Monotonic deque solves Sliding Window Maximum in O(n) — impossible without a deque.

## How to implement

Pick by what arrives and how you consume:

```
FIFO          — collections.deque; append right, popleft
level-wise    — snapshot the size at start of each level, loop that many times
circular      — fixed-size buffer + head/tail indices modulo capacity
deque         — append/pop from BOTH ends; ideal for monotonic windows
```

Subpatterns in this folder:

- **01-FIFO** — generic queue: push back, pop front, breadth-first iteration.
- **02-Level-wise** — BFS that processes each level fully before the next.
- **03-Circular** — fixed-size ring buffer for streaming data.
- **04-Deque** — double-ended queue for monotonic-window tricks.

## Which problems this approach solves in the real world

- BFS-based shortest paths in unweighted graphs.
- Print/job queues in operating systems.
- Producer-consumer pipelines and message brokers (Kafka, RabbitMQ).
- Sliding window maximum in financial tick streams.
- Web-server request queues and rate limiters.
- Level-order tree rendering (file browsers, organisation charts).

## Pros and cons

**Pros**
- FIFO matches real-world arrival order: fair and simple.
- O(1) amortised push/pop on both ends with `deque`.
- BFS over a queue finds shortest path in unweighted graphs trivially.
- Circular queues are extremely memory-efficient for streams.

**Cons**
- No random access — only ends are O(1).
- Using a plain list as a queue gives O(n) `pop(0)` — always use `deque`.
- Concurrent producer-consumer queues need careful locking.
- For weighted shortest paths a queue is insufficient (need heap).

## Limitations

- Can't peek the middle or arbitrary positions.
- No native ordering by priority; that's what heaps are for.
- Circular queue overflow needs an explicit policy (drop, overwrite, block).
- BFS memory cost can exceed DFS on broad trees.
