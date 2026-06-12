# Circular queue

## What is this

A circular queue (ring buffer) stores up to `k` elements in a fixed-size array indexed modulo `k`. Two pointers track the head and tail; when either reaches the end it wraps to position 0. Enqueue, dequeue, peek, and full/empty checks are all O(1) with no allocation after construction.

It is used wherever bounded buffering is needed: audio/video frame buffers, network packet queues, telemetry sliding windows, lock-free single-producer/single-consumer queues.

## Why we use

- Fixed memory: never grows beyond `k`, predictable footprint.
- O(1) operations with no shifting.
- Excellent cache behavior — contiguous array, no allocations.
- Naturally models a bounded window of recent items.

## How to implement

```
buf = [None] * k
head = tail = size = 0

enqueue(x):
    if size == k: return False
    buf[tail] = x
    tail = (tail + 1) % k
    size += 1

dequeue():
    if size == 0: return None
    x = buf[head]
    head = (head + 1) % k
    size -= 1
    return x
```

```python
class CircularQueue:
    def __init__(self, k):
        self.buf = [None] * k
        self.head = self.tail = self.size = 0
        self.cap = k

    def enqueue(self, x):
        if self.size == self.cap: return False
        self.buf[self.tail] = x
        self.tail = (self.tail + 1) % self.cap
        self.size += 1
        return True

    def dequeue(self):
        if self.size == 0: return None
        x = self.buf[self.head]
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return x

    def front(self): return None if self.size == 0 else self.buf[self.head]
    def is_full(self):  return self.size == self.cap
    def is_empty(self): return self.size == 0
```

Tracking `size` explicitly avoids the "head == tail ambiguity" (could mean empty or full).

## Which problems this approach solves in the real world

- Audio/video frame buffers in real-time pipelines.
- Network packet queues at NIC drivers.
- Recent-N event windows in metrics dashboards.
- Round-robin task scheduling in operating systems.
- Lock-free SPSC queues in concurrent systems.

## Pros and cons

**Pros**
- O(1) ops, no per-operation allocation.
- Bounded memory — back-pressure built in.
- Excellent cache locality.

**Cons**
- Fixed capacity — overflow must be handled explicitly.
- Index arithmetic (modulo) is error-prone.
- Resizing requires a copy of all elements.

## Limitations

- Bad fit when workload spikes exceed capacity unpredictably.
- Not directly thread-safe without atomic operations or locks.
- No priority — strictly FIFO within the ring.

## One example

**Problem**: Design your circular queue implementation. It should support `enQueue`, `deQueue`, `Front`, `Rear`, `isEmpty`, `isFull`. Capacity `k` is given at construction.

**Input**: `MyCircularQueue(3); enQueue(1); enQueue(2); enQueue(3); enQueue(4); Rear(); isFull(); deQueue(); enQueue(4); Rear();`
**Output**: `[null, true, true, true, false, 3, true, true, true, 4]`
**Constraints**: `1 <= k <= 1000`.

## Solution explanation

The class above implements the LeetCode 622 contract exactly. Walkthrough of the example with `k = 3` (buffer cells labeled 0,1,2):

| op           | buf            | head | tail | size | return |
|--------------|----------------|------|------|------|--------|
| ctor(3)      | [_, _, _]      | 0    | 0    | 0    |        |
| enQ(1)       | [1, _, _]      | 0    | 1    | 1    | True   |
| enQ(2)       | [1, 2, _]      | 0    | 2    | 2    | True   |
| enQ(3)       | [1, 2, 3]      | 0    | 0    | 3    | True   |
| enQ(4)       | [1, 2, 3]      | 0    | 0    | 3    | False  |
| Rear()       | -              | -    | -    | -    | 3      |
| isFull()     | -              | -    | -    | -    | True   |
| deQ()        | [1, 2, 3]      | 1    | 0    | 2    | True   |
| enQ(4)       | [4, 2, 3]      | 1    | 1    | 3    | True   |
| Rear()       | -              | -    | -    | -    | 4      |

Time: O(1) per op. Space: O(k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Design Circular Queue (LeetCode 622) | https://leetcode.com/problems/design-circular-queue/ |
| Medium | Design Circular Deque (LeetCode 641) | https://leetcode.com/problems/design-circular-deque/ |
| Hard | Design Hit Counter (LeetCode 362) | https://leetcode.com/problems/design-hit-counter/ |
