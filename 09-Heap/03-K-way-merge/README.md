# Merge K sorted streams (heap)

## What is this

Given `k` sorted streams (lists, arrays, linked lists, or iterators), produce one fully sorted output stream. A min-heap of size `k` tracks the next-smallest element of each stream. Pop the minimum, append it to output, then push the next element from the same source. The result is a sorted sequence of all elements.

This pattern is the heap-based answer to "external sort", "merge K sorted lists", and "k-way merge step" in mergesort and database engines.

## Why we use

- O(N log k) where N is total elements, k is number of streams
- Streaming-friendly: only one element per stream is in memory at a time
- Easily handles infinite streams if you only need the first N items
- Foundation for external sort, distributed merge, log-merge in DBs

## How to implement

```
heap = min-heap of (value, stream_index, internal_index)
push first element of each non-empty stream
while heap not empty:
    val, si, idx = pop
    emit val
    if streams[si] has element at idx + 1:
        push (streams[si][idx + 1], si, idx + 1)
```

```python
import heapq

def merge_k_sorted(streams: list[list[int]]) -> list[int]:
    heap: list[tuple[int, int, int]] = []
    for i, s in enumerate(streams):
        if s:
            heapq.heappush(heap, (s[0], i, 0))
    out: list[int] = []
    while heap:
        val, i, idx = heapq.heappop(heap)
        out.append(val)
        if idx + 1 < len(streams[i]):
            heapq.heappush(heap, (streams[i][idx + 1], i, idx + 1))
    return out
```

Linked-list variant (LeetCode 23 style):

```python
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class HeapItem:
    val: int
    idx: int
    node: object = field(compare=False)

class ListNode:
    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt

def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    heap: list[HeapItem] = []
    for i, head in enumerate(lists):
        if head is not None:
            heapq.heappush(heap, HeapItem(head.val, i, head))
    dummy = ListNode(0)
    tail = dummy
    while heap:
        item = heapq.heappop(heap)
        tail.next = item.node
        tail = tail.next
        nxt = item.node.next  # type: ignore[attr-defined]
        if nxt is not None:
            heapq.heappush(heap, HeapItem(nxt.val, item.idx, nxt))
    return dummy.next
```

Invariant: the heap always contains exactly one (current-front) element from each non-exhausted stream. Popping the min yields the next element of the merged output globally.

## Which problems this approach solves in the real world

- External sort: merge sorted runs that don't fit in RAM
- Log file merge across distributed servers preserving timestamp order
- LSM-tree compaction in storage engines (LevelDB, RocksDB)
- Database `MERGE JOIN` final step combining sorted partitions
- Multi-source event stream consolidation (e.g. Kafka topic merges)

## Pros and cons

**Pros**
- O(N log k) — fast when k << N
- Streaming-compatible memory: O(k)
- Generalises trivially to any iterable streams

**Cons**
- Heap operations dominate runtime; if k is small, simple loop is faster
- Linked list version needs custom heap items because nodes aren't comparable
- Cache-unfriendly: each pop chases a pointer to a different stream

## Limitations

- Doesn't beat O(N) for k = 2 (use a simple merge)
- Heap entries must be totally ordered — ties on value need stable secondary keys
- For very large k, consider tournament trees or divide-and-conquer merge

## One example

Problem: Given `k` sorted linked lists, merge them all into one sorted linked list.

```
Input:  lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
Output: [1, 1, 2, 3, 4, 4, 5, 6]
Constraints: 0 <= k <= 10^4, 0 <= total nodes <= 10^4
```

## Solution explanation

```python
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class HeapItem:
    val: int
    idx: int
    node: object = field(compare=False)

class ListNode:
    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt

def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    heap: list[HeapItem] = []
    for i, head in enumerate(lists):
        if head is not None:
            heapq.heappush(heap, HeapItem(head.val, i, head))
    dummy = ListNode(0)
    tail = dummy
    while heap:
        item = heapq.heappop(heap)
        tail.next = item.node
        tail = tail.next
        nxt = item.node.next  # type: ignore[attr-defined]
        if nxt is not None:
            heapq.heappush(heap, HeapItem(nxt.val, item.idx, nxt))
    return dummy.next
```

Push each list's head into a heap keyed by value with the list index as a stable tiebreaker. Pop the smallest, append to the output, push the popped node's next.

Walkthrough for `lists = [[1,4,5], [1,3,4], [2,6]]`. Heap entries are `(value, list_idx)`:

| Step | Heap (sorted)            | Pop      | Output           | Push next |
|------|--------------------------|----------|------------------|-----------|
| init | [(1,0), (1,1), (2,2)]    |          | []               |           |
| 1    | [(1,1), (2,2), (4,0)]    | (1,0)    | [1]              | (4,0)     |
| 2    | [(2,2), (4,0), (3,1)]    | (1,1)    | [1,1]            | (3,1)     |
| 3    | [(3,1), (4,0), (6,2)]    | (2,2)    | [1,1,2]          | (6,2)     |
| 4    | [(4,0), (6,2), (4,1)]    | (3,1)    | [1,1,2,3]        | (4,1)     |
| 5    | [(4,0), (4,1), (6,2)]    | (4,0)    | [1,1,2,3,4]      | (5,0)     |
| 6    | [(4,1), (5,0), (6,2)]    | (4,1)    | [1,1,2,3,4,4]    | (none)    |
| 7    | [(5,0), (6,2)]           | (5,0)    | [1,1,2,3,4,4,5]  | (none)    |
| 8    | [(6,2)]                  | (6,2)    | [1,1,2,3,4,4,5,6]| (none)    |

Time O(N log k), space O(k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Merge Two Sorted Lists (LeetCode 21) | https://leetcode.com/problems/merge-two-sorted-lists/ |
| Medium | Smallest Range Covering Elements from K Lists (LeetCode 632) | https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/ |
| Hard | Merge k Sorted Lists (LeetCode 23) | https://leetcode.com/problems/merge-k-sorted-lists/ |
