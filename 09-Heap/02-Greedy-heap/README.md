# Greedy + Heap

## Folder structure

```
02-Greedy-heap/
├── README.md
├── 01-Task-scheduler/README.md
├── 02-Meeting-rooms/README.md
├── 03-Reorganize-string/README.md
└── 04-Huffman-encoding/README.md
```

## What is this

This family combines a greedy decision rule with a heap that always exposes the locally-best candidate. The heap's job is to answer the question "what is the most-urgent / longest / most-frequent thing right now?" in O(log n) so the greedy step doesn't need to scan the entire workload. Together they turn quadratic naive solutions into log-linear ones.

The pattern shows up wherever the optimum is built one decision at a time and each decision depends on the current state of the world. Task schedulers pop the highest-frequency task that's allowed right now. Meeting-room planners pop the room that frees up earliest. Huffman encoders pop the two lightest nodes to merge. The greedy proof says the decision is safe; the heap makes the decision cheap.

## Why we use

- The greedy rule reduces decision-making to "take the locally-best thing" — provably optimal for these problems.
- The heap answers "what is locally-best" in O(log n), turning O(n²) scans into O(n log n).
- Naturally handles streaming workloads where you process one event at a time.
- Composes cleanly with "cooldown" constraints (push back to heap after a delay) and "two heaps" patterns.

## How to implement

```text
function greedyHeap(items):
    heap = buildHeap(items)         # priority defined by problem
    while heap not empty:
        x = popBest(heap)
        decision = useFor(x)
        recordOrEmit(decision)
        for produced in followups(x):
            push(heap, produced)
```

Per-problem priority:
- Task scheduler: max-heap on remaining frequency; push back after cooldown idle slots.
- Meeting rooms: min-heap on end time; pop if next meeting's start ≥ heap top.
- Reorganize string: max-heap on char frequency; pop two distinct chars per step.
- Huffman: min-heap on weight; pop two lightest, push their sum.

Subpatterns in this folder:

- `01-Task-scheduler/` — cooldown-constrained scheduling with max-heap by frequency.
- `02-Meeting-rooms/` — minimum-rooms-needed via min-heap of end times.
- `03-Reorganize-string/` — distance-2 placement via max-heap by frequency.
- `04-Huffman-encoding/` — optimal prefix-free code via repeated min-merge.

## Which problems this approach solves in the real world

- CPU job schedulers respecting per-job cooldowns or priority levels.
- Conference-room booking and resource allocation against overlapping bookings.
- Text-to-speech sequencing where identical phonemes must be spaced out.
- File-compression encoding (Huffman / arithmetic) for storage efficiency.
- Streaming top-K dashboards where the leaderboard is updated event-by-event.
- Network packet schedulers that must dispatch the highest-priority frame each tick.

## Pros and cons

**Pros**
- Greedy + heap is often the optimal asymptotic solution: O(n log n) is hard to beat.
- Memory is O(n) — the heap doesn't grow beyond the active workload.
- Handles streaming events: you can push and pop as events arrive.
- Each problem in the family shares the same skeleton — quick to implement once familiar.

**Cons**
- Proving the greedy choice is safe is problem-specific and not always obvious.
- Heaps don't support "decrease-key" cheaply in most language stdlibs — you may need lazy deletion.
- Tie-breaking matters: same priority can lead to different valid outputs; tests may expect a specific one.
- The wrong priority key silently produces non-optimal answers; bugs are hard to detect.

## Limitations

- Not all greedy problems have a heap-friendly priority — some need monotonic queues or segment trees.
- Doesn't apply when decisions are *interdependent* (one choice constrains future feasibility non-locally) — that's DP/flow.
- Heap-based solutions don't lend themselves to easy parallelism — the heap is a serialization point.
- Bounded heaps (top-K) are subtly different from full heaps and use a min-heap for max-K.
