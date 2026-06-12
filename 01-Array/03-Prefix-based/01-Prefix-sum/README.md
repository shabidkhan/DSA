# Prefix sum

## What is this

A precomputation technique: from an array `arr` of length `n`, build a `prefix` array of length `n + 1` where `prefix[i] = arr[0] + arr[1] + ... + arr[i-1]` (with `prefix[0] = 0`). After O(n) preprocessing, any range sum `arr[l..r]` is answered in **O(1)** as `prefix[r+1] - prefix[l]`. The same idea extends to 2D (prefix-sum matrix for submatrix queries), to prefix XOR, prefix max/min, and to "count of values ≤ k" via a hashed prefix-count.

## Why we use

- Range-sum queries collapse from O(n) per query to O(1) per query after one O(n) preprocessing pass.
- Combined with a hash map, prefix sums solve "count subarrays with sum k" / "longest subarray with sum k" in O(n) — a famous interview pattern.
- Extends cleanly to 2D for submatrix sums (O(1) per query after O(r·c) preprocessing).

## How to implement

```
prefix[0] = 0
for i in 0..n-1:
    prefix[i + 1] = prefix[i] + arr[i]

range_sum(l, r) = prefix[r + 1] - prefix[l]
```

Python — 1D prefix sum:

```python
def build_prefix(arr: list[int]) -> list[int]:
    prefix = [0] * (len(arr) + 1)
    for i, x in enumerate(arr):
        prefix[i + 1] = prefix[i] + x
    return prefix

def range_sum(prefix: list[int], l: int, r: int) -> int:
    return prefix[r + 1] - prefix[l]
```

Python — subarray sum equals K (the hash-map trick):

```python
def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    count = 0
    running = 0
    seen = {0: 1}        # empty prefix has sum 0, occurring once
    for x in nums:
        running += x
        count += seen.get(running - k, 0)
        seen[running] = seen.get(running, 0) + 1
    return count
```

Invariant: `prefix[i]` is the sum of the first `i` elements. So `prefix[r+1] - prefix[l]` "cancels" the first `l` elements and leaves the sum of `arr[l..r]`. In the hash-map variant, every "running sum value" we've seen is a candidate left boundary for a subarray ending at the current index.

## Which problems this approach solves in the real world

- **Time-series range aggregates**: precompute prefix sums of daily revenue / page views to answer "total in range [a, b]" in O(1).
- **2D image processing**: integral images (summed-area tables) let you compute the sum of any sub-rectangle in O(1) — used in face detection (Haar features) and box blurs.
- **Subarray-with-target-sum analytics**: counting how many time windows sum exactly to a threshold (e.g. exact-budget months).
- **Sliding aggregates on streams**: when window endpoints can be arbitrary, prefix sums beat a deque.
- **Cumulative quotas / counters**: precompute prefix counts of categorical events for fast range-count queries.

## Pros and cons

**Pros**
- O(n) preprocessing, O(1) per range query.
- Generalises to XOR, AND, OR, max via different "inverse" operations (XOR is its own inverse → range XOR works the same way).
- The hash-map variant solves "count subarrays summing to k" in O(n) — far better than O(n²) brute force.
- 2D extension is also O(1) per submatrix query after O(r·c) preprocessing.

**Cons**
- Extra O(n) space for the prefix array.
- Doesn't support range **updates** in O(1) — if updates are frequent, use a Fenwick tree or segment tree instead.
- Floating-point prefix sums accumulate rounding error; for high-precision needs use Kahan summation or integers.
- For min/max, prefix-based queries don't work directly (no inverse operation) — use a sparse table or segment tree.

## Limitations

- Static-array assumption: if the underlying array changes, the prefix array must be rebuilt (O(n)) or maintained with a Fenwick tree.
- Doesn't apply when the aggregate isn't invertible (max, min, gcd over arbitrary ranges).
- 2D prefix sums require O(r·c) memory — can be prohibitive for very large matrices.

## One example

**Problem**: Given an integer array `nums` and an integer `k`, return the **total number of subarrays** whose sum equals `k`. Constraints: `1 ≤ nums.length ≤ 2·10^4`, `-10^3 ≤ nums[i] ≤ 10^3`, `-10^7 ≤ k ≤ 10^7`.

**Input**: `nums = [1, 2, 3]`, `k = 3`
**Output**: `2` (subarrays `[1, 2]` and `[3]`)

## Solution explanation

```python
def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    count = 0
    running = 0
    seen = {0: 1}
    for x in nums:
        running += x
        count += seen.get(running - k, 0)
        seen[running] = seen.get(running, 0) + 1
    return count
```

Walk-through on `nums = [1, 2, 3]`, k = 3:

| i | nums[i] | running | running - k | seen[running-k] (before update) | count | seen (after update) |
|---|---------|---------|-------------|----------------------------------|-------|----------------------|
| 0 | 1       | 1       | -2          | 0                                | 0     | {0:1, 1:1}           |
| 1 | 2       | 3       | 0           | 1                                | 1     | {0:1, 1:1, 3:1}      |
| 2 | 3       | 6       | 3           | 1                                | 2     | {0:1, 1:1, 3:1, 6:1} |

The key identity: a subarray `nums[l+1..r]` sums to `k` iff `prefix[r+1] - prefix[l] = k`, i.e. `prefix[l] = prefix[r+1] - k`. So at each right endpoint `r`, we count how many earlier left-prefix values equal `running - k`. The seed `{0: 1}` accounts for subarrays starting from index 0 (an empty prefix has sum 0).

- **Time**: O(n) — one pass, O(1) hash operations expected.
- **Space**: O(n) — hash map of distinct prefix sums.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Running Sum of 1d Array** — return the prefix-sum array. | https://leetcode.com/problems/running-sum-of-1d-array/ |
| Medium | **Subarray Sum Equals K** — count subarrays summing to `k` using prefix sum + hash map. | https://leetcode.com/problems/subarray-sum-equals-k/ |
| Hard   | **Maximum Sum of Rectangle No Larger Than K** — 2D prefix sums + sorted set per row pair. | https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/ |
