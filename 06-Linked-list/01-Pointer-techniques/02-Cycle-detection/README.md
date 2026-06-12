# Cycle detection (Floyd's tortoise and hare)

## What is this

Floyd's cycle detection — popularly **tortoise and hare** — uses two pointers traversing a linked list at different speeds. The "slow" pointer (tortoise) moves one node at a time; the "fast" pointer (hare) moves two nodes at a time. If a cycle exists, the fast pointer will eventually lap the slow one inside the cycle, and the two will meet. If no cycle exists, the fast pointer reaches `null` first.

There's a second phase: once they meet, restart one pointer at the head and move both one-by-one — they will meet again exactly at the **cycle entry**. This is a consequence of the algebra of the cycle.

## Why we use

- Detects a cycle in a linked list (or any "next-pointer" structure) using **O(1) extra memory** — no visited set, no hashing.
- Time is O(n) — the slow pointer traverses each node at most once before being caught.
- Finds the **start of the cycle** with the same O(1) memory.
- Works for any iterable structure with a `next` function — also used to detect "happy number" cycles, function-iteration fixed points, etc.

## How to implement

```
# Phase 1: detect cycle
slow = head
fast = head
while fast is not None and fast.next is not None:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:
        break
else:
    return None    # no cycle

# Phase 2: find cycle entry
slow = head
while slow is not fast:
    slow = slow.next
    fast = fast.next
return slow        # cycle entry
```

Python:

```python
class ListNode:
    def __init__(self, x: int, next: "ListNode | None" = None) -> None:
        self.val = x
        self.next = next

def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            # Phase 2
            slow = head
            while slow is not fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

JavaScript:

```javascript
function detectCycle(head) {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) {
      slow = head;
      while (slow !== fast) {
        slow = slow.next;
        fast = fast.next;
      }
      return slow;
    }
  }
  return null;
}
```

Invariant: after the first phase, both pointers are inside the cycle, at the same node. After the second phase, both arrive at the cycle's entry node simultaneously.

## Why Phase 2 works (the algebra)

Let:
- L = length from head to cycle entry,
- C = length of the cycle,
- d = distance inside the cycle from the entry to the meeting point.

When they meet, slow has walked `L + d` steps; fast has walked `2(L + d)`. Fast has also walked `L + d + k·C` for some integer `k` (it went around `k` extra times). So:
`2(L + d) = L + d + k·C` → `L + d = k·C` → `L = k·C − d`.

Starting one pointer at the head and one at the meeting point and walking both at speed 1, they each travel `L` steps to converge — meeting precisely at the cycle entry.

## Which problems this approach solves in the real world

- **Memory leak diagnosis**: detect cycles in object reference graphs without a hash table of seen pointers.
- **File system / link analysis**: spot symlink loops without storing every traversed inode.
- **Cryptographic hash collision search**: Pollard's rho factorisation uses tortoise-and-hare on `x → f(x)` sequences.
- **Random number generator analysis**: find the period of a pseudo-random sequence using constant memory.
- **Event loop diagnostics**: detect infinitely recurring callback chains.
- **Dependency resolution**: detect cycles in build graphs when memory is at a premium.

## Pros and cons

**Pros**
- O(1) extra memory — uses only two pointers regardless of list length.
- O(n) time — slow pointer makes at most one full pass before being caught.
- Phase 2 also gives the cycle entry "for free".
- Generalises to any functional iteration `x → f(x)`, not just linked lists.

**Cons**
- Subtle to derive — Phase 2's correctness isn't obvious without the algebra.
- Requires that following `next` is cheap (e.g. pointer dereference); doesn't apply to expensive lookups without modification.
- Doesn't directly give cycle length — but you can compute it by keeping `slow` fixed and walking `fast` until they meet again, counting steps.

## Limitations

- For doubly linked or arbitrary graph cycles, this technique alone is insufficient — you need DFS with visit colouring.
- If the underlying iteration changes during traversal (concurrent modification), the algorithm gives no useful guarantee.
- For very short cycles in very long tails, the constant factor is still optimal but you may prefer hashing if memory isn't tight.

## One example

**Problem**: Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return `null`. The position of the tail's `next` pointer (the cycle entry index, `pos`) is *not* given as a parameter — you must discover it.
Constraints: `0 ≤ length ≤ 10^4`, `-10^5 ≤ Node.val ≤ 10^5`, `pos = -1` (no cycle) or a valid index.

**Input**: `head = [3, 2, 0, -4]`, tail's `next` points to index 1 (node with value 2).

**Output**: the node with value `2`.

## Solution explanation

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

Walk-through on `[3 → 2 → 0 → -4 → (back to 2)]` (so L = 1, C = 3):

Phase 1:

| step | slow | fast |
|------|------|------|
| 0    | 3    | 3    |
| 1    | 2    | 0    |
| 2    | 0    | 2    |
| 3    | -4   | -4   |

They meet at node `-4`. `d = 2` (distance from cycle entry `2` to meeting node `-4` going forward).

Phase 2: start `slow` at head (`3`), keep `fast` at `-4`. Each step:

| step | slow | fast |
|------|------|------|
| 0    | 3    | -4   |
| 1    | 2    | 2    |

They meet at node `2` — the **cycle entry**. Return it.

Check the algebra: `L = 1`, `C = 3`, `d = 2`, `k = 1`, so `L = k·C − d = 3 − 2 = 1`. Matches.

- **Time**: O(n) — Phase 1 ≤ n iterations (slow can't lap itself); Phase 2 ≤ L iterations.
- **Space**: O(1) — two pointers only.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Linked List Cycle** — return true/false whether a cycle exists. Just Phase 1. | https://leetcode.com/problems/linked-list-cycle/ |
| Medium | **Linked List Cycle II** — find the node where the cycle begins. The canonical problem above. | https://leetcode.com/problems/linked-list-cycle-ii/ |
| Hard | **Find the Duplicate Number** — given `n+1` ints from `[1, n]` with exactly one duplicate, find it using Floyd's on the function `i → nums[i]`. | https://leetcode.com/problems/find-the-duplicate-number/ |
