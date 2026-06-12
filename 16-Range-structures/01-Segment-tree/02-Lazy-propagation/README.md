# Segment tree with lazy propagation

## What is this

Lazy propagation extends a segment tree to handle **range updates** in O(log n) instead of O(n). Each internal node stores a pending modifier (the "lazy" value) that has *not yet* been pushed to its children. When traversing into a node that has a pending modifier, push it down first, then recurse.

Typical operations: "add v to every element in [l, r]" or "assign v to every element in [l, r]", with mixed range-aggregate queries. Each node keeps both an aggregate value and a pending tag.

## Why we use

- O(log n) for both range update and range query.
- Bulk modifications without touching every covered leaf.
- Foundation for sweep-line and offline interval algorithms.
- Enables interval-DP solvers that mutate large segments.

## How to implement

```
build, query, update are recursive
node t[4n], lazy[4n]
push(node, lo, hi):
    if lazy[node] != 0:
        t[2node]   += lazy[node] * (mid - lo + 1)
        t[2node+1] += lazy[node] * (hi - mid)
        lazy[2node]   += lazy[node]
        lazy[2node+1] += lazy[node]
        lazy[node] = 0
update(node, lo, hi, l, r, v): if [lo,hi] outside [l,r]: return
                                if covered: t[node] += v*(hi-lo+1); lazy[node]+=v; return
                                push; recurse; t[node]=t[2n]+t[2n+1]
query(node, lo, hi, l, r):     symmetric
```

```python
class LazySeg:
    def __init__(self, data):
        n = len(data)
        self.n = n
        self.t = [0] * (4 * n)
        self.lz = [0] * (4 * n)
        self._build(1, 0, n - 1, data)

    def _build(self, node, lo, hi, data):
        if lo == hi:
            self.t[node] = data[lo]; return
        mid = (lo + hi) // 2
        self._build(2*node,   lo,    mid, data)
        self._build(2*node+1, mid+1, hi,  data)
        self.t[node] = self.t[2*node] + self.t[2*node+1]

    def _push(self, node, lo, hi):
        if self.lz[node]:
            mid = (lo + hi) // 2
            v = self.lz[node]
            self.t[2*node]   += v * (mid - lo + 1)
            self.t[2*node+1] += v * (hi - mid)
            self.lz[2*node]   += v
            self.lz[2*node+1] += v
            self.lz[node] = 0

    def range_add(self, l, r, v, node=1, lo=0, hi=None):
        if hi is None: hi = self.n - 1
        if r < lo or hi < l: return
        if l <= lo and hi <= r:
            self.t[node] += v * (hi - lo + 1)
            self.lz[node] += v
            return
        self._push(node, lo, hi)
        mid = (lo + hi) // 2
        self.range_add(l, r, v, 2*node,   lo,    mid)
        self.range_add(l, r, v, 2*node+1, mid+1, hi)
        self.t[node] = self.t[2*node] + self.t[2*node+1]

    def range_sum(self, l, r, node=1, lo=0, hi=None):
        if hi is None: hi = self.n - 1
        if r < lo or hi < l: return 0
        if l <= lo and hi <= r: return self.t[node]
        self._push(node, lo, hi)
        mid = (lo + hi) // 2
        return (self.range_sum(l, r, 2*node,   lo,    mid)
              + self.range_sum(l, r, 2*node+1, mid+1, hi))
```

The lazy tag means: "this subtree's aggregate already reflects this modifier, but the modifier has not been applied to children yet."

## Which problems this approach solves in the real world

- Telemetry rollups: bump every counter in a time window by a constant.
- Bulk price adjustments across an inventory range.
- Range-coloring problems in painting/canvas simulations.
- Interval DP problems with overlapping subproblem updates.
- Maintaining dynamic sums under range-shift operations.

## Pros and cons

**Pros**
- O(log n) for both range update and range query.
- Generalizes to range assign, range affine, range min/max with care.
- Allows composing multiple modifier types.

**Cons**
- Code is significantly more complex than point-update segment trees.
- Lazy tag composition (e.g. add over assign) is bug-prone.
- 4n memory factor.

## Limitations

- Non-associative or non-distributive ops cannot be lazy-propagated.
- Range updates that depend on individual indices break the lazy abstraction.
- Persistent versions multiply memory cost.

## One example

**Problem**: Given an array of zeros of length `n`, apply a list of range-add operations `[l, r, v]`, then return the maximum value in the final array.

**Input**: `length = 5`, `updates = [[1,3,2], [2,4,3], [0,2,-2]]`
**Output**: `3` (final array `[-2, 0, 3, 5, 3]`, max 5 — but problem asks max which equals 5)
**Constraints**: `1 <= n <= 10^5`, `0 <= operations <= 10^5`.

## Solution explanation

```python
def getMax(length, updates):
    seg = LazySeg([0] * length)
    for l, r, v in updates:
        seg.range_add(l, r, v)
    best = max(seg.range_sum(i, i) for i in range(length))
    return best
```

Walkthrough on `length=5, updates=[[1,3,2],[2,4,3],[0,2,-2]]`:

| op            | array state after  |
|---------------|--------------------|
| init          | [0, 0, 0, 0, 0]    |
| range_add(1,3,2)  | [0, 2, 2, 2, 0]|
| range_add(2,4,3)  | [0, 2, 5, 5, 3]|
| range_add(0,2,-2) | [-2, 0, 3, 5, 3]|

Max = 5. Note: for the actual computation we'd use point queries via `range_sum(i, i)`; in production code we'd push everything down once at the end.

Time: O((n + q) log n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Corporate Flight Bookings (LeetCode 1109) | https://leetcode.com/problems/corporate-flight-bookings/ |
| Medium | Range Addition (LeetCode 370) | https://leetcode.com/problems/range-addition/ |
| Hard | Falling Squares (LeetCode 699) | https://leetcode.com/problems/falling-squares/ |
