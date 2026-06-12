# Reverse nodes in k-group

## What is this

Reverse a linked list `k` nodes at a time, leaving any trailing fewer-than-k nodes in their original order. Walk the list in groups of `k`; within each group, reverse the local segment in place by rewiring `next` pointers; then splice the reversed segment back into the prior tail.

This is the most representative "partial reversal" problem — proves you understand both the reversal primitive and pointer rewiring at boundaries.

## Why we use

- O(n) time, O(1) extra memory (iterative version).
- Generalizes both "reverse whole list" (k = n) and "no-op" (k = 1).
- Building block for chunked stream processors that need block-reversed order.
- Standard interview test for pointer manipulation discipline.

## How to implement

```
sentinel.next = head
group_prev = sentinel
while True:
    kth = walk k nodes from group_prev
    if kth is None: break
    group_next = kth.next
    # reverse [group_prev.next ... kth]
    prev, cur = group_next, group_prev.next
    while cur is not group_next:
        nxt = cur.next; cur.next = prev
        prev = cur; cur = nxt
    new_head_of_group = kth
    new_tail_of_group = group_prev.next
    group_prev.next = new_head_of_group
    group_prev = new_tail_of_group
return sentinel.next
```

```python
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val; self.next = nxt

def reverse_k_group(head, k):
    sentinel = ListNode(0, head)
    group_prev = sentinel

    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return sentinel.next
        group_next = kth.next

        prev, cur = group_next, group_prev.next
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        tmp = group_prev.next
        group_prev.next = kth
        group_prev = tmp
```

```python
def reverse_segment(head, tail_next):
    prev, cur = tail_next, head
    while cur is not tail_next:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev          # new head of reversed segment
```

A sentinel (dummy) node simplifies the "first group" splice — no special-case for the head.

## Which problems this approach solves in the real world

- Block-wise reversal of streaming events for analytics windows.
- Chunked file processing where each block is reversed for de-interleaving.
- Reverse-order pagination at fixed page sizes.
- Reordering message frames in protocols that interleave block sequences.
- Foundation for "rotate every k nodes" patterns.

## Pros and cons

**Pros**
- O(n) time, O(1) memory iterative.
- Generalizes whole-list and chunk-wise reversal.
- Single sentinel cleanly handles the head boundary.

**Cons**
- Pointer rewiring is bug-prone — easy to lose tail references.
- Edge case for the final partial group is the most common bug.
- Recursive variant has O(n/k) stack depth.

## Limitations

- Singly-linked only; doubly-linked needs extra `prev` updates.
- Mutating shared lists concurrently is unsafe without locks.
- Cannot be done in less than O(n) — every node is rewired.

## One example

**Problem**: Given the head of a linked list, reverse the nodes `k` at a time and return the modified list. Nodes at the end that do not form a full group of `k` remain as they are.

**Input**: `head = [1, 2, 3, 4, 5]`, `k = 2`
**Output**: `[2, 1, 4, 3, 5]`
**Constraints**: `1 <= n <= 5000`, `1 <= k <= n`.

## Solution explanation

`reverse_k_group` above. Walkthrough on `[1, 2, 3, 4, 5]`, k=2:

| iter | group_prev | kth | group covered | after reverse + splice |
|------|------------|-----|---------------|------------------------|
| 1    | sentinel   | node(2) | [1, 2] | sentinel -> 2 -> 1 -> 3 -> 4 -> 5 |
| 2    | node(1)    | node(4) | [3, 4] | sentinel -> 2 -> 1 -> 4 -> 3 -> 5 |
| 3    | node(3)    | walk fails after 1 step | — | return list as-is |

Final: `[2, 1, 4, 3, 5]`.

Time: O(n). Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Reverse Linked List (LeetCode 206) | https://leetcode.com/problems/reverse-linked-list/ |
| Medium | Reverse Linked List II (LeetCode 92) | https://leetcode.com/problems/reverse-linked-list-ii/ |
| Hard | Reverse Nodes in k-Group (LeetCode 25) | https://leetcode.com/problems/reverse-nodes-in-k-group/ |
