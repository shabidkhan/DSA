# Linked List Patterns

## Folder structure

```
06-Linked-list/
├── README.md
├── 01-Pointer-techniques/
│   ├── README.md
│   ├── 01-Fast-slow/README.md
│   ├── 02-Cycle-detection/README.md
│   └── 03-Find-middle/README.md
├── 02-Reversal/
│   ├── README.md
│   ├── 01-Full-reverse/README.md
│   └── 02-K-group/README.md
└── 03-Merge-lists/README.md
```

## What is this

A linked list is a chain of nodes where each node points to the next (and sometimes the previous). Unlike arrays, you cannot jump to position `i` in O(1), but you can splice, insert, and remove nodes in O(1) given a pointer. Linked-list problems therefore centre on pointer manipulation rather than indexing — and the patterns split cleanly into three families: pointer techniques (fast/slow runners and cycle detection), reversal (full reverse, partial reverse, k-group), and merge (combine two or more sorted/unsorted lists).

Once you've internalised the dummy-node-and-prev/curr template, most linked-list problems collapse into a handful of pointer rewires. The hard part is keeping track of "which pointer points where right now" — drawing the list on paper for one or two iterations is almost always the fastest way to get it right.

## Why we use

- O(1) insert/delete at any known position — much better than array shifts.
- No fixed capacity: lists grow without resizing.
- The slow/fast technique solves cycle and middle-finding in O(1) extra space.
- Reversal patterns are the building blocks for many higher-level algorithms (palindrome check, reorder list).

## How to implement

Pick the subpattern by the operation:

```
pointer techniques  — fast/slow runner, cycle detect, find middle
reversal            — flip pointers in-place; full reverse or partial / k-group
merge               — splice nodes from two lists into a third (dummy head)
```

Subpatterns in this folder:

- **01-Pointer-techniques** — fast-slow (tortoise and hare), cycle detection, find middle.
- **02-Reversal** — full reverse and partial / k-group reverse.
- **03-Merge-lists** — combine two sorted lists into one.

## Which problems this approach solves in the real world

- LRU cache implementation (doubly linked list + hash map).
- Browser history navigation back/forward.
- Music/video playlist with skip and repeat.
- Memory free-lists in allocators.
- Undo/redo chains in editors (sometimes a deque internally).
- Polynomial arithmetic when degrees are sparse.

## Pros and cons

**Pros**
- O(1) insert and delete at known positions.
- No resizing, no copying — append is constant.
- Excellent for in-place reordering (reverse, rotate, merge).
- Memory locality issues aside, the asymptotic cost beats arrays for many ops.

**Cons**
- O(n) random access — indexing is expensive.
- Cache-unfriendly: nodes scatter across memory.
- Extra memory per node for the pointer (sometimes two).
- Pointer-rewire bugs (lost tails, dangling next) are common.

## Limitations

- No O(1) "previous" pointer in singly linked lists.
- Reversal/merge usually require a dummy node and careful prev/curr/next bookkeeping.
- Detecting and breaking cycles needs care to avoid infinite loops.
- Concurrent linked lists are notoriously hard (ABA problem, lock-free designs).
