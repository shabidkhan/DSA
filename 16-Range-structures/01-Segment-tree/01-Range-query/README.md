# Segment tree range query

## What is this

A segment tree stores aggregate information (sum, min, max, gcd, etc.) over every contiguous range of an array in a balanced binary tree of size O(n). Each leaf holds one element; each internal node holds the aggregate of its two children's ranges. Both `update(i, val)` and `query(l, r)` run in O(log n).

This is the workhorse of competitive programming whenever you need range aggregates with point updates. Variants extend to range updates (lazy propagation), 2D, persistent, and dynamic segment trees.

## Why we use

- O(log n) per query and per point update — strictly better than O(n) brute force.
- Supports any associative operation (sum, min, max, gcd, xor, matrix product).
- Foundation for lazy propagation and merge-sort tree generalizations.
- Compact iterative form fits in ~25 lines.

## How to implement

```
tree[1..2n], leaves at positions n..2n-1
build: for i in n-1..1: tree[i] = op(tree[2i], tree[2i+1])
update(p, v): p += n; tree[p] = v; while p>1: p>>=1; tree[p] = op(tree[2p], tree[2p+1])
query(l, r):
    l += n; r += n + 1; res = identity
    while l < r:
        if l & 1: res = op(res, tree[l]); l += 1
        if r & 1: r -= 1; res = op(res, tree[r])
        l >>= 1; r >>= 1
    return res
```

```python
class SegTree:
    def __init__(self, data, op=lambda a, b: a + b, identity=0):
        self.n = len(data)
        self.op = op
        self.id = identity
        self.t = [identity] * (2 * self.n)
        for i, v in enumerate(data):
            self.t[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.t[i] = op(self.t[2 * i], self.t[2 * i + 1])

    def update(self, p, v):
        p += self.n
        self.t[p] = v
        p //= 2
        while p:
            self.t[p] = self.op(self.t[2 * p], self.t[2 * p + 1])
            p //= 2

    def query(self, l, r):       # [l, r)
        res_l, res_r = self.id, self.id
        l += self.n; r += self.n
        while l < r:
            if l & 1:
                res_l = self.op(res_l, self.t[l]); l += 1
            if r & 1:
                r -= 1; res_r = self.op(self.t[r], res_r)
            l //= 2; r //= 2
        return self.op(res_l, res_r)
```

Keep left and right accumulators separately when the operation is non-commutative (matrix product, affine transform).

## Which problems this approach solves in the real world

- Real-time analytics: rolling sums / min / max over a recent window with point edits.
- Computational geometry sweeps requiring "stabbing count" over intervals.
- Financial systems: range-aggregates of trade volumes per minute bucket.
- Persistent versioning: combine with path-copying to query historical snapshots.
- Game state queries — fastest-route calculations with edge-weight updates.

## Pros and cons

**Pros**
- O(log n) queries and updates.
- Works with any associative op.
- Compact iterative form, no recursion overhead.

**Cons**
- O(n) memory and O(n) build cost.
- Range updates require lazy propagation.
- Indexing arithmetic is error-prone.

## Limitations

- Operations must be associative — averaging requires storing sum + count.
- Coordinate compression needed when index space is sparse.
- 2D extension multiplies memory and constant factors.

## One example

**Problem**: Given an array `nums`, support two operations: `update(index, val)` sets `nums[index] = val`, and `sumRange(l, r)` returns the sum of `nums[l..r]` inclusive.

**Input**: `["NumArray","sumRange","update","sumRange"], [[[1,3,5]], [0,2], [1,2], [0,2]]`
**Output**: `[null, 9, null, 8]`
**Constraints**: `1 <= n <= 3*10^4`, up to 3*10^4 operations.

## Solution explanation

```python
class NumArray:
    def __init__(self, nums):
        self.t = SegTree(nums, op=lambda a, b: a + b, identity=0)

    def update(self, index, val):
        self.t.update(index, val)

    def sumRange(self, left, right):
        return self.t.query(left, right + 1)
```

Walkthrough on `nums = [1, 3, 5]`:

| op                | tree.t (1-indexed)         | result |
|-------------------|-----------------------------|--------|
| build             | [_, 9, 4, 5, 1, 3]          |        |
| sumRange(0, 2)    | full sum                    | 9      |
| update(1, 2)      | [_, 8, 3, 5, 1, 2]          |        |
| sumRange(0, 2)    | full sum                    | 8      |

Time: O(log n) per op. Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Range Sum Query - Immutable (LeetCode 303) | https://leetcode.com/problems/range-sum-query-immutable/ |
| Medium | Range Sum Query - Mutable (LeetCode 307) | https://leetcode.com/problems/range-sum-query-mutable/ |
| Hard | Count of Smaller Numbers After Self (LeetCode 315) | https://leetcode.com/problems/count-of-smaller-numbers-after-self/ |
