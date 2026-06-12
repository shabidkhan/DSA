# Subarray with given XOR / sum

## What is this

This pattern counts (or finds) all contiguous subarrays whose aggregate (XOR or sum) equals a target `k`. The unified trick: as you scan, maintain a running prefix aggregate. Then "subarray ending here aggregates to k" ↔ "an earlier prefix value of `cur (op) k` was seen". A hash map keyed by previously-seen prefixes turns the inner search into O(1).

For sums: `seen[cur - k]`. For XOR: `seen[cur ^ k]`. The structure is identical — only the inverse operation differs.

## Why we use

- O(n) time, O(n) space — beats O(n^2) brute pair check.
- Single template covers sum, XOR, and any invertible group operation.
- Naturally extends to "longest" / "count" / "exists" variants.
- Streaming-friendly: keep a single dict and a running aggregate.

## How to implement

```
cur = 0
seen = {0: 1}            # empty prefix already accounts for one occurrence
count = 0
for x in a:
    cur = cur OP x       # OP = + for sum, ^ for XOR
    count += seen.get(inverse(cur, k), 0)
    seen[cur] = seen.get(cur, 0) + 1
return count
```

```python
def subarrays_with_sum_k(a, k):
    cur, count = 0, 0
    seen = {0: 1}
    for x in a:
        cur += x
        count += seen.get(cur - k, 0)
        seen[cur] = seen.get(cur, 0) + 1
    return count
```

```python
def subarrays_with_xor_k(a, k):
    cur, count = 0, 0
    seen = {0: 1}
    for x in a:
        cur ^= x
        count += seen.get(cur ^ k, 0)
        seen[cur] = seen.get(cur, 0) + 1
    return count
```

Seeding `seen = {0: 1}` accounts for prefixes that themselves equal `k` (the subarray starts at index 0).

## Which problems this approach solves in the real world

- Telemetry: count windows that sum to a target SLA value.
- Cryptographic / forensic: count ranges whose XOR equals a known signature.
- Financial: count contiguous periods with net change equal to a target amount.
- Parity check: count subarrays with an even number of odd elements (XOR with 1-bit).
- Pattern alignment in streams of integer codes.

## Pros and cons

**Pros**
- O(n) — strictly better than brute pair enumeration.
- Same template for sum, XOR, count-of-bit-parities.
- Trivial to extend to "longest" by storing first-seen index.

**Cons**
- O(n) memory for the hash map.
- Floating-point sums cause rounding mismatches.
- Doesn't apply to non-invertible aggregates (min, max, gcd).

## Limitations

- Cannot retrieve all subarrays in O(n) — only count or one example.
- Streaming variant has unbounded memory if prefix values are very diverse.
- Negative numbers + sum work, but zero-sum subarrays need the `{0:1}` seed.

## One example

**Problem**: Given an array of integers `nums` and an integer `k`, return the total number of continuous subarrays whose sum equals to `k`.

**Input**: `nums = [1, 1, 1]`, `k = 2`
**Output**: `2`
**Constraints**: `1 <= n <= 2 * 10^4`, `-1000 <= nums[i] <= 1000`.

## Solution explanation

```python
def subarraySum(nums, k):
    cur, count = 0, 0
    seen = {0: 1}
    for x in nums:
        cur += x
        count += seen.get(cur - k, 0)
        seen[cur] = seen.get(cur, 0) + 1
    return count
```

Walkthrough on `nums = [1, 1, 1]`, k = 2:

| i | x | cur after | need = cur - k | seen.get(need, 0) | count | seen after        |
|---|---|-----------|----------------|-------------------|-------|-------------------|
| 0 | 1 | 1         | -1             | 0                 | 0     | {0:1, 1:1}        |
| 1 | 1 | 2         | 0              | 1                 | 1     | {0:1, 1:1, 2:1}   |
| 2 | 1 | 3         | 1              | 1                 | 2     | {0:1, 1:1, 2:1, 3:1} |

Result: 2 (subarrays `[1,1]` at indices 0-1 and 1-2).

Time: O(n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Subarray Sum Equals K (LeetCode 560) — easier variant counts | https://leetcode.com/problems/subarray-sum-equals-k/ |
| Medium | Contiguous Array (LeetCode 525) | https://leetcode.com/problems/contiguous-array/ |
| Hard | Subarray Sums Divisible by K (LeetCode 974) | https://leetcode.com/problems/subarray-sums-divisible-by-k/ |
