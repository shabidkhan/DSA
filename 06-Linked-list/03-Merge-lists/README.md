# Merge linked lists

## What is this

The merge pattern combines two (or more) sorted linked lists into a single sorted linked list by splicing pointers — no new nodes are allocated for the data. A `dummy` head simplifies edge cases, and a `tail` pointer always points to the last node already in the merged result.

The technique extends to mergesort on a linked list (split with fast/slow then merge) and to `k`-way merges with a heap.

## Why we use

- O(n + m) two-list merge with O(1) extra memory
- No data copying — only pointer manipulation, cache-friendly relative to array merging
- Building block for mergesort on linked lists (stable, O(n log n))
- Generalises to `k` lists via min-heap (see Merge-K)

## How to implement

```
dummy = ListNode(0)
tail = dummy
while a and b:
    if a.val <= b.val:
        tail.next = a; a = a.next
    else:
        tail.next = b; b = b.next
    tail = tail.next
tail.next = a if a else b
return dummy.next
```

```python
class ListNode:
    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt

def merge_two_sorted(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    dummy = ListNode(0)
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next
```

Recursive variant (uses O(n + m) stack — fine for small inputs):

```python
def merge_recursive(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    if a is None:
        return b
    if b is None:
        return a
    if a.val <= b.val:
        a.next = merge_recursive(a.next, b)
        return a
    b.next = merge_recursive(a, b.next)
    return b
```

Invariant: at each step `tail` is the last node of the merged-so-far prefix, and that prefix is sorted in non-decreasing order; the choice of `a.val <= b.val` preserves stability between equal keys.

## Which problems this approach solves in the real world

- Merging two sorted log streams (each is a singly linked list of events)
- Combining sorted insertion-order linked lists from different threads
- Merging segments in skip-list / mergesort implementations
- Stitching two ordered task queues without copying tasks
- Sorted concatenation of immutable persistent lists in functional languages

## Pros and cons

**Pros**
- O(1) extra memory in iterative form
- Stable: preserves order between equal keys when using `<=`
- Pure pointer rewiring — no allocation cost

**Cons**
- Doesn't work on doubly linked lists without extra `prev` updates
- Recursive variant blows Python's recursion limit for long lists
- Cannot easily resume mid-merge after partial reads (stateful)

## Limitations

- Only useful when inputs are already sorted
- Tail traversal is O(length of result) — not parallelisable
- Cannot insert nodes that don't exist; not for set-like deduplication

## One example

Problem: Merge two sorted singly linked lists and return the head of the merged list.

```
Input:  a = 1 -> 2 -> 4
        b = 1 -> 3 -> 4
Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4
Constraints: 0 <= |a|, |b| <= 50, -100 <= node.val <= 100
```

## Solution explanation

```python
def merge_two_sorted(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    dummy = ListNode(0)
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next
```

Walk both inputs in lockstep, always appending the smaller front node, then attach the leftover tail of whichever list isn't exhausted.

Walkthrough for `a = 1 -> 2 -> 4`, `b = 1 -> 3 -> 4`. `dummy -> ?`, `tail = dummy`.

| Step | a.val | b.val | Choice (<=) | tail.next after | a after | b after |
|------|-------|-------|-------------|-----------------|---------|---------|
| 1    | 1     | 1     | a (tie)     | a(1)            | 2 -> 4  | 1 -> 3 -> 4 |
| 2    | 2     | 1     | b           | b(1)            | 2 -> 4  | 3 -> 4 |
| 3    | 2     | 3     | a           | a(2)            | 4       | 3 -> 4 |
| 4    | 4     | 3     | b           | b(3)            | 4       | 4 |
| 5    | 4     | 4     | a (tie)     | a(4)            | None    | 4 |
| End  |       |       | append b(4) |                 |         |   |

Result `dummy.next = 1 -> 1 -> 2 -> 3 -> 4 -> 4`. Time O(n + m), space O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Merge Two Sorted Lists (LeetCode 21) | https://leetcode.com/problems/merge-two-sorted-lists/ |
| Medium | Sort List (mergesort on linked list) (LeetCode 148) | https://leetcode.com/problems/sort-list/ |
| Hard | Merge k Sorted Lists (LeetCode 23) | https://leetcode.com/problems/merge-k-sorted-lists/ |
