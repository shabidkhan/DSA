# Find middle (slow/fast pointer)

## What is this

Finding the middle of a singly-linked list with a single pass uses two pointers: `slow` moves one step at a time, `fast` moves two. When `fast` reaches the end of the list, `slow` is at the middle. For even-length lists, `slow` lands on the *second* middle node (the upper median) — the conventional choice for "split list in half".

This is a building block for merge-sort on linked lists, palindrome checks, and "delete the middle".

## Why we use

- Single pass, O(n) time, O(1) extra memory.
- No need to know list length in advance.
- Composes with merge sort to split a list in half cheaply.
- Trivial to convert to "delete the middle" — keep `prev` of slow.

## How to implement

```
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow
```

```python
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val; self.next = nxt

def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

```python
def find_middle_lower(head):
    """Return the lower middle on even-length lists."""
    if not head: return None
    slow = head
    fast = head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

The difference between "upper" and "lower" middle is the initial offset of `fast`.

## Which problems this approach solves in the real world

- Splitting a linked list into halves for merge sort.
- Implementing palindrome checks on linked lists.
- Deleting the median node from a queue-like structure.
- Cycle detection (extends to Floyd's algorithm).
- Finding the k-th node from the end via two-pointer offset.

## Pros and cons

**Pros**
- O(n) time, O(1) memory.
- Single pass — no length precomputation needed.
- Easy to adapt for "delete middle" by tracking `prev`.

**Cons**
- Returns upper middle by default — easy to confuse with lower.
- Requires careful null handling at the head and end.
- Not random-access — every element must be walked.

## Limitations

- Linked-list only — not for arrays (O(1) `len // 2` is direct).
- Mutation-aware: if other code modifies the list during traversal, results are undefined.
- Not directly meaningful on cyclic lists — combine with cycle detection.

## One example

**Problem**: Given the head of a singly linked list, return the middle node. If there are two middle nodes, return the second one.

**Input**: `head = [1, 2, 3, 4, 5]`
**Output**: node containing `3` (and its tail `[3, 4, 5]`)
**Constraints**: `1 <= n <= 100`, `1 <= Node.val <= 100`.

## Solution explanation

```python
def middleNode(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

Walkthrough on `head = [1, 2, 3, 4, 5]`:

| iter | slow.val | fast.val |
|------|----------|----------|
| 0    | 1        | 1        |
| 1    | 2        | 3        |
| 2    | 3        | 5        |
| 3 (loop exits, fast.next is None) | 3 | 5 |

Return node with value 3. On `[1, 2, 3, 4, 5, 6]`, the same algorithm returns node with value 4 (upper middle).

Time: O(n). Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Middle of the Linked List (LeetCode 876) | https://leetcode.com/problems/middle-of-the-linked-list/ |
| Medium | Delete the Middle Node of a Linked List (LeetCode 2095) | https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/ |
| Hard | Reorder List (LeetCode 143) | https://leetcode.com/problems/reorder-list/ |
