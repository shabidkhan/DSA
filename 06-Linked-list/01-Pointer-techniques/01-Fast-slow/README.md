# Fast/slow pointers (linked list)

## What is this

The fast/slow pointer (a.k.a. tortoise and hare) technique walks two pointers down a linked list at different speeds — typically `slow` moves one step and `fast` moves two. The relative motion exposes properties of the list that a single-pointer walk cannot detect in one pass: cycle existence, cycle entry point, middle node, and Nth-from-end node.

The algorithm uses O(1) extra memory and a single traversal, so it is the standard tool for linked-list interview problems.

## Why we use

- O(n) time, O(1) memory — beats hash-set-based cycle detection
- One-pass middle / Nth-from-end without computing length first
- Detects cycles and finds the cycle's start (Floyd's algorithm)
- Composable with other linked-list manipulations (reverse, merge)

## How to implement

```
Cycle detection:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast: cycle detected

Find cycle start (Floyd):
    after meeting, set fast = head; advance both by 1 step
    they meet at the cycle entry

Find middle:
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow   # mid for odd length, right-of-mid for even
```

```python
class ListNode:
    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt

def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def cycle_start(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            slow2 = head
            while slow2 is not slow:
                slow2 = slow2.next      # type: ignore[union-attr]
                slow = slow.next        # type: ignore[union-attr]
            return slow2
    return None

def middle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # type: ignore[union-attr]
        fast = fast.next.next
    return slow
```

Invariant for cycle detection: if a cycle of length `L` exists, after `k` steps `fast` is `k` ahead of `slow` modulo `L`. Eventually `fast` laps `slow` and they coincide.

## Which problems this approach solves in the real world

- Cycle detection in memory-managed object graphs (mark-and-sweep variants)
- Loop checks in dependency lists at runtime where the data is already a linked structure
- Detecting infinite loops in functional iterators (e.g. PRNG cycle length)
- Finding the middle of a singly linked list to split it for mergesort
- Removing the Nth-from-end node in singly linked structures

## Pros and cons

**Pros**
- O(n) time, O(1) memory
- Single pass — no precomputed length needed
- Algorithmically elegant; cycle-start derivation is a classic result

**Cons**
- Only works on linked structures, not random-access arrays (where index math is simpler)
- Subtle: choosing wrong starting offset between pointers can break correctness
- Doesn't handle non-cyclic infinite streams

## Limitations

- Requires `next` pointers — useless on doubly linked lists' backward traversal
- Cycle-length detection needs a second pass after finding the meeting point
- Not parallelisable

## One example

Problem: Given the `head` of a singly linked list, return the node where the cycle begins. If there is no cycle, return `None`.

```
Input:  list = 3 -> 2 -> 0 -> -4 -> (back to node with value 2)
Output: node with value 2
Constraints: 0 <= len(list) <= 10^4, -10^5 <= node.val <= 10^5
```

## Solution explanation

```python
def cycle_start(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            entry = head
            while entry is not slow:
                entry = entry.next        # type: ignore[union-attr]
                slow = slow.next          # type: ignore[union-attr]
            return entry
    return None
```

Phase 1 detects the cycle by Floyd's "meeting". Phase 2 uses the fact that resetting one pointer to head and advancing both at the same speed makes them meet at the cycle's entry node.

Walkthrough for the cyclic list `3 -> 2 -> 0 -> -4 -> 2 (back to second node)`. Index nodes 0..3 for clarity; cycle entry index is 1.

Phase 1 (find meeting):

| Step | slow.idx | fast.idx |
|------|----------|----------|
| 0    | 0        | 0        |
| 1    | 1        | 2        |
| 2    | 2        | 1        |
| 3    | 3        | 3        |  meet at idx 3

Phase 2 (find entry; reset `entry = head`, advance both by 1):

| Step | entry.idx | slow.idx |
|------|-----------|----------|
| 0    | 0         | 3        |
| 1    | 1         | 1        |  meet at idx 1 -> cycle start (value 2)

Time O(n), space O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Linked List Cycle (LeetCode 141) | https://leetcode.com/problems/linked-list-cycle/ |
| Medium | Linked List Cycle II (LeetCode 142) | https://leetcode.com/problems/linked-list-cycle-ii/ |
| Hard | Find the Duplicate Number (LeetCode 287) | https://leetcode.com/problems/find-the-duplicate-number/ |
