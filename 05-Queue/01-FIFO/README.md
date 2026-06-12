# FIFO queue processing

## What is this

A FIFO (first-in, first-out) queue processes elements strictly in arrival order. You enqueue at the tail and dequeue at the head; whichever element waited longest leaves next. In Python the canonical implementation is `collections.deque`, whose `append` and `popleft` are both O(1).

This pattern fits any system where order of arrival must be preserved: print queues, task buffers, BFS frontiers (level-order shape but FIFO is the underlying mechanism), producer/consumer pipelines.

## Why we use

- Preserve arrival order without sorting.
- O(1) enqueue and dequeue.
- Natural buffer between asynchronous producers and consumers.
- Underlies BFS and many scheduling algorithms.

## How to implement

```
q = deque()
q.append(x)         # enqueue
y = q.popleft()     # dequeue
```

```python
from collections import deque

def first_unique_char_stream(stream):
    q = deque()
    seen_twice = set()
    in_queue = {}
    out = []
    for c in stream:
        if c in seen_twice:
            pass
        elif c in in_queue:
            seen_twice.add(c)
        else:
            in_queue[c] = True
            q.append(c)
        while q and q[0] in seen_twice:
            q.popleft()
        out.append(q[0] if q else '#')
    return out
```

```python
def producer_consumer(jobs):
    q = deque(jobs)
    while q:
        job = q.popleft()
        # process(job)
```

Never use a Python `list` as a queue — `list.pop(0)` is O(n).

## Which problems this approach solves in the real world

- Print spoolers and ticket queues.
- Message-broker delivery preserving publish order per partition.
- Producer/consumer buffers in pipelines (e.g. log shippers).
- Request queues in front of a thread pool.
- BFS frontier expansion in shortest-path on unweighted graphs.

## Pros and cons

**Pros**
- Trivial mental model and O(1) ops.
- Preserves arrival order for fairness.
- Built into every language's standard library.

**Cons**
- No priority — long jobs block short ones.
- Memory grows with backlog; no built-in back-pressure.
- Cannot peek by position efficiently.

## Limitations

- No random access — index lookups in a deque are O(n).
- Not thread-safe by itself (`queue.Queue` adds locking).
- Loses ordering across multiple queues unless explicitly merged.

## One example

**Problem**: Given a string `s` representing a stream of characters, for each new character output the first non-repeating character so far, or `#` if none exists.

**Input**: `"a"` then `"a"` then `"b"` then `"c"`
**Output**: `["a", "#", "b", "b"]`
**Constraints**: `1 <= len(s) <= 10^5`, lowercase letters.

## Solution explanation

```python
from collections import deque

def first_unique(stream):
    q = deque()
    count = {}
    out = []
    for c in stream:
        count[c] = count.get(c, 0) + 1
        q.append(c)
        while q and count[q[0]] > 1:
            q.popleft()
        out.append(q[0] if q else '#')
    return out
```

Walkthrough on `stream = "aabc"`:

| c | count after | queue after enqueue | drain while head dup | out append |
|---|-------------|--------------------|----------------------|------------|
| a | {a:1}       | [a]                | [a]                  | a          |
| a | {a:2}       | [a, a]             | []                   | #          |
| b | {a:2, b:1}  | [b]                | [b]                  | b          |
| c | {a:2, b:1, c:1} | [b, c]         | [b, c]               | b          |

Time: O(n). Space: O(k) for distinct chars.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Implement Queue using Stacks (LeetCode 232) | https://leetcode.com/problems/implement-queue-using-stacks/ |
| Medium | Design Hit Counter (LeetCode 362) | https://leetcode.com/problems/design-hit-counter/ |
| Hard | Design Snake Game (LeetCode 353) | https://leetcode.com/problems/design-snake-game/ |
