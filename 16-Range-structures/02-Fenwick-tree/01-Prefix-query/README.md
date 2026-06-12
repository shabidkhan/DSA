# Fenwick tree (BIT) prefix query

## What is this

A Fenwick tree (binary indexed tree, BIT) supports point update + prefix-sum query, each in O(log n), using a single 1-indexed array of size n+1. The structure exploits the binary expansion of an index: index `i` is responsible for the range of size `i & -i` ending at `i`.

It's the most compact O(log n) range-prefix structure: about 10 lines of code, ~2x faster constant than a segment tree, and uses exactly n+1 memory cells.

## Why we use

- O(log n) per point update and prefix-sum query.
- Single array of size n+1 — half the memory of a segment tree.
- Trivial to extend to range queries via `prefix(r) - prefix(l-1)`.
- Tight constant factor; fewer cache misses than segment trees.

## How to implement

```
update(i, v):
    while i <= n: bit[i] += v; i += i & -i
prefix(i):
    s = 0
    while i > 0: s += bit[i]; i -= i & -i
    return s
range_sum(l, r): return prefix(r) - prefix(l - 1)
```

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.b = [0] * (n + 1)

    def update(self, i, v):       # 1-indexed
        while i <= self.n:
            self.b[i] += v
            i += i & -i

    def prefix(self, i):
        s = 0
        while i > 0:
            s += self.b[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):    # inclusive 1-indexed
        return self.prefix(r) - self.prefix(l - 1)
```

```python
def build_from_array(a):
    bit = BIT(len(a))
    for i, v in enumerate(a, 1):
        bit.update(i, v)
    return bit
```

The trick `i & -i` isolates the lowest set bit; subtracting it strips it. That's the only bit math the structure needs.

## Which problems this approach solves in the real world

- Real-time leaderboards with frequent score updates and prefix queries.
- Inversion counting in O(n log n) via coordinate compression.
- Frequency-table prefix queries in online analytics.
- Order statistics in sorted-set wrappers (find k-th element).
- Range-frequency queries in offline algorithms.

## Pros and cons

**Pros**
- Compact: ~10 lines, single array.
- Faster constant than segment trees.
- Easy to extend to range queries on prefixes.

**Cons**
- Only supports invertible aggregates (sum, xor, count) directly.
- Min / max queries need a different "fenwick min tree" structure.
- Range updates need a two-BIT trick.

## Limitations

- Cannot directly do non-invertible aggregates (min, max, gcd).
- 1-indexed convention causes off-by-one bugs.
- 2D extensions are O(log^2 n).

## One example

**Problem**: Count smaller numbers after self. Given `nums`, return `counts` where `counts[i]` is the number of `j > i` with `nums[j] < nums[i]`.

**Input**: `nums = [5, 2, 6, 1]`
**Output**: `[2, 1, 1, 0]`
**Constraints**: `1 <= n <= 10^5`, `-10^4 <= nums[i] <= 10^4`.

## Solution explanation

```python
def countSmaller(nums):
    sorted_unique = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_unique)}  # 1-indexed
    bit = BIT(len(sorted_unique))
    out = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        r = rank[nums[i]]
        out[i] = bit.prefix(r - 1)
        bit.update(r, 1)
    return out
```

Walkthrough on `nums = [5, 2, 6, 1]`. Ranks: 1→1, 2→2, 5→3, 6→4.

| i | nums[i] | rank | prefix(rank-1) before update | bit state after update |
|---|---------|------|------------------------------|------------------------|
| 3 | 1       | 1    | prefix(0) = 0 → out[3]=0     | rank1 inc              |
| 2 | 6       | 4    | prefix(3) = 1 → out[2]=1     | rank4 inc              |
| 1 | 2       | 2    | prefix(1) = 1 → out[1]=1     | rank2 inc              |
| 0 | 5       | 3    | prefix(2) = 2 → out[0]=2     | rank3 inc              |

Result `[2, 1, 1, 0]`. Time: O(n log n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Running Sum of 1d Array (LeetCode 1480) | https://leetcode.com/problems/running-sum-of-1d-array/ |
| Medium | Range Sum Query - Mutable (LeetCode 307) | https://leetcode.com/problems/range-sum-query-mutable/ |
| Hard | Count of Smaller Numbers After Self (LeetCode 315) | https://leetcode.com/problems/count-of-smaller-numbers-after-self/ |
