# Pointer Techniques (Linked List)

## Folder structure

```
01-Pointer-techniques/
├── README.md
├── 01-Fast-slow/README.md
├── 02-Cycle-detection/README.md
└── 03-Find-middle/README.md
```

## What is this

Pointer techniques on linked lists use two (or more) pointers moving through the list at different speeds or with different roles to solve problems that would otherwise need extra storage or multiple passes. The three canonical techniques are **fast-slow** (one pointer advances one node, another advances two — used for find-middle), **cycle detection** (Floyd's tortoise and hare detects a cycle in O(1) extra space and finds its entry point with a second phase), and **find middle** (special case of fast-slow that lands the slow pointer on the middle node when the fast pointer falls off).

The unifying idea is that two coordinated pointers running at known speed ratios give you positional information (middle, cycle entry, kth-from-end) without random access. The math behind cycle detection is elegant — when fast meets slow inside the cycle, the head-to-cycle-entry distance equals the meeting-point-to-cycle-entry distance modulo cycle length.

## Why we use

- O(1) extra space — both pointers are just references.
- One pass: no need to know the list length up front.
- Floyd's algorithm finds a cycle and its entry point in two short passes.
- The same skeleton works for find-middle, kth-from-end, and palindrome checks.

## How to implement

```
find middle:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

cycle detection (phase 1):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast: return True       # cycle exists
    return False

cycle entry (phase 2, after phase 1 meeting):
    p = head
    while p != slow:
        p = p.next
        slow = slow.next
    return p                                # cycle entry node

kth from end:
    fast = head
    for _ in range(k): fast = fast.next
    slow = head
    while fast: slow = slow.next; fast = fast.next
    return slow                             # kth-from-end node
```

Subpatterns in this folder:

- **01-Fast-slow** — slow / fast runner with 1x and 2x speeds.
- **02-Cycle-detection** — Floyd's tortoise and hare; phase 1 detects, phase 2 finds entry.
- **03-Find-middle** — special case of fast-slow landing on the middle node.

## Which problems this approach solves in the real world

- Cycle detection in dependency graphs that are linearised as lists.
- Detecting loops in user-navigation history.
- Finding the median of a singly linked list in one pass.
- Detecting infinite loops in iterator-based code.
- Implementing kth-from-end queries in cursor-based pagination.
- Spotting cycles in object-reference chains for garbage collectors.

## Pros and cons

**Pros**
- O(1) extra space — much better than the hash-set alternative.
- Linear time in the worst case.
- Single-pass algorithms; no need to know the list length.
- Mathematically elegant proofs that survive interview scrutiny.

**Cons**
- Cycle math (head-to-entry == meet-to-entry) is non-obvious and easy to mis-derive.
- Off-by-one errors on "fast falls off vs fast.next falls off".
- Odd-length vs even-length middle returns different nodes; choose intentionally.
- Cannot detect a cycle's length in one pass — need a follow-up walk.

## Limitations

- Works only on singly linked lists; doubly linked structures rarely need these tricks.
- Doesn't generalise to non-sequential structures.
- Cycle entry needs the second phase — easy to forget.
- For mutable lists with concurrent modifications, classic Floyd's assumptions break.
