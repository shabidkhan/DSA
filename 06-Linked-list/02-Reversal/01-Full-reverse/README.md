# Reverse linked list

## What is this

Reversing a singly linked list rewrites every `next` pointer to point at the predecessor. The iterative version walks three pointers — `prev`, `curr`, `nxt` — flipping links in a single pass without allocating new nodes. The recursive version mirrors the same logic by unwinding the call stack.

The same primitive underpins many compound linked-list operations: reverse a sublist between two positions, reverse in groups of `k`, and palindrome checks that compare a reversed half to the original.

## Why we use

- O(n) time, O(1) memory (iterative)
- Pointer-only rewrite — no node allocation, GC pressure low
- Building block for "reverse in groups of k", "reorder list", and palindrome detection
- Essential preprocessing for stack-free DFS / traversal tricks

## How to implement

```
prev = None
curr = head
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
return prev   # new head
```

```python
class ListNode:
    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt

def reverse(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

Recursive variant (uses O(n) stack):

```python
def reverse_recursive(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head     # the next node now points back
    head.next = None
    return new_head
```

Reverse a sublist `[left, right]` (1-indexed) in one pass:

```python
def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, head)
    prev_left = dummy
    for _ in range(left - 1):
        prev_left = prev_left.next        # type: ignore[assignment]
    curr = prev_left.next                  # first node of the segment
    for _ in range(right - left):
        nxt = curr.next                    # type: ignore[union-attr]
        curr.next = nxt.next               # type: ignore[union-attr]
        nxt.next = prev_left.next          # type: ignore[union-attr]
        prev_left.next = nxt
    return dummy.next
```

Invariant for the iterative full reverse: at the start of each loop iteration, the list from `head` through the predecessor of `curr` has been reversed, with `prev` pointing at its head.

## Which problems this approach solves in the real world

- Stack-free traversal of singly linked structures by temporarily reversing and restoring
- Implementing undo stacks where most-recent action is at the front
- Reverse a queue's content for replay in opposite order
- Palindromic message detection in network streams represented as linked frames
- Reordering linked-list snippets in text editors that use rope-style structures

## Pros and cons

**Pros**
- O(1) memory iterative form
- Three-line core logic; easy to recall in interviews
- Easily composes with split/merge to solve harder problems

**Cons**
- Recursive version risks stack overflow on long lists
- Mutates input — destructive on the caller's list
- Cannot be done in O(1) extra memory on singly linked lists *while preserving original*

## Limitations

- For non-destructive reverse, you must copy nodes (O(n) memory)
- Doubly linked list reverse needs to also flip `prev` pointers
- Reversing across multi-threaded access requires locking

## One example

Problem: Reverse a singly linked list and return the new head.

```
Input:  1 -> 2 -> 3 -> 4 -> 5
Output: 5 -> 4 -> 3 -> 2 -> 1
Constraints: 0 <= len(list) <= 5000, -5000 <= node.val <= 5000
```

## Solution explanation

```python
def reverse(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

For every node, save its next link, point it backwards, advance both pointers.

Walkthrough for `1 -> 2 -> 3 -> 4 -> 5`:

| Step | prev | curr | nxt  | curr.next set to | After: list visible from prev |
|------|------|------|------|-------------------|--------------------------------|
| init | None | 1    |      |                   |                                |
| 1    | 1    | 2    | 2    | None              | 1 -> None                      |
| 2    | 2    | 3    | 3    | 1                 | 2 -> 1 -> None                 |
| 3    | 3    | 4    | 4    | 2                 | 3 -> 2 -> 1 -> None            |
| 4    | 4    | 5    | 5    | 3                 | 4 -> 3 -> 2 -> 1 -> None       |
| 5    | 5    | None | None | 4                 | 5 -> 4 -> 3 -> 2 -> 1 -> None  |

Return `prev = 5`. Time O(n), space O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Reverse Linked List (LeetCode 206) | https://leetcode.com/problems/reverse-linked-list/ |
| Medium | Reverse Linked List II (LeetCode 92) | https://leetcode.com/problems/reverse-linked-list-ii/ |
| Hard | Reverse Nodes in k-Group (LeetCode 25) | https://leetcode.com/problems/reverse-nodes-in-k-group/ |
