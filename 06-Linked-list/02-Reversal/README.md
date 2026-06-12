# Linked-list Reversal Patterns

## Folder structure

```
02-Reversal/
├── README.md
├── 01-Full-reverse/README.md
└── 02-K-group/README.md
```

## What is this

Reversal flips the direction of `next` pointers in a linked list — either the whole list (Reverse Linked List) or a contiguous segment (Reverse Linked List II, Reverse Nodes in K-Group). The core operation is the three-pointer dance: `prev`, `curr`, `next` — save `next`, point `curr.next` back to `prev`, advance `prev` and `curr`. This O(n) in-place transformation underpins many higher-level linked-list problems (palindrome check, reorder list, swap pairs, k-group reverse).

The two subpatterns here are **full reverse** (the cleanest three-line loop in algorithms) and **partial / k-group reverse** (reverse exactly k nodes at a time, leave the remainder as-is or recurse). Both share the same primitive but differ in bookkeeping for boundaries — the "before" and "after" pointers must be reconnected correctly to avoid lost tails.

## Why we use

- O(n) one-pass in-place reversal — optimal in both time and space.
- O(1) extra space; only three pointer variables.
- The building block for palindrome checks, reorder-list, k-group rotations.
- Mechanical once memorised — three lines per node.

## How to implement

```
full reverse:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev                      # new head

reverse k-group:
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth: return dummy.next
        group_next = kth.next
        prev, curr = group_next, group_prev.next
        for _ in range(k):
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        old_first = group_prev.next
        group_prev.next = kth
        group_prev = old_first
```

Subpatterns in this folder:

- **01-Full-reverse** — flip every node's next pointer.
- **02-K-group** — reverse exactly k consecutive nodes at a time.

## Which problems this approach solves in the real world

- Palindrome verification (reverse second half, compare with first half).
- Reorder-list operations in editors and music playlists.
- Reversing recent N items in an LRU cache for refresh.
- Chunked reversal for batch-flip operations in editors.
- Implementing undo with reversed history pointers.
- Reformatting log streams for chronological replay.

## Pros and cons

**Pros**
- O(n) time, O(1) extra space — optimal.
- Single pass; no length precomputation needed for full reverse.
- Three-pointer skeleton is iconic and easy to recall.
- K-group variant generalises cleanly to arbitrary segment reversals.

**Cons**
- K-group bookkeeping (reconnect before-segment to new head, old head to after-segment) is fiddly.
- Drawing the list on paper for one iteration is almost always required first time.
- Recursive reversal blows the stack on very long lists.
- Easy to lose the tail or create a cycle if pointer order is wrong.

## Limitations

- Singly linked only; doubly linked reversal needs to flip both pointers.
- Cannot run on immutable list representations (functional languages need a new list).
- Concurrent modification during reversal will tangle pointers.
- K-group with partial remainder needs an explicit policy ("leave as-is" vs "reverse anyway").
