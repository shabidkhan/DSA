# Prefix XOR

## What is this

Prefix XOR is the XOR analogue of the prefix-sum technique: define `P[i] = a[0] ^ a[1] ^ ... ^ a[i-1]`, so the XOR of any subarray `a[l..r]` becomes `P[r+1] ^ P[l]`. Because XOR is its own inverse (`x ^ x = 0`) and is associative and commutative, the algebra works out exactly like prefix sums but with XOR replacing addition. The same hashmap trick that gives "count subarrays with sum K" gives "count subarrays with XOR K" in linear time.

Prefix XOR is essential whenever you need a fast lookup over "XOR of any subarray" — for parity, target-XOR counting, longest target-XOR subarray, or fixed-XOR pairs over a stream. Combined with a hashmap of prefix-XOR frequencies it answers most of these queries in O(n).

## Why we use

- It turns any subarray-XOR query into two O(1) lookups via `P[r+1] ^ P[l]`.
- Memory cost is just one extra integer per index — cheap and cache-friendly.
- Pairs naturally with a hashmap for counting subarrays that XOR to a target.
- Same algebra extends to longest, shortest, or boundary-respecting subarray-XOR problems.

## How to implement

```
P[0] = 0
for i in 0..n-1:
    P[i+1] = P[i] ^ a[i]

# subarray-XOR of a[l..r]:
def subarray_xor(l, r):
    return P[r+1] ^ P[l]

# count subarrays with XOR == k:
freq = {0: 1}
prefix = 0
count = 0
for x in a:
    prefix ^= x
    count += freq.get(prefix ^ k, 0)
    freq[prefix] = freq.get(prefix, 0) + 1
```

```python
def count_subarrays_with_xor(arr, k):
    freq = {0: 1}
    prefix = 0
    count = 0
    for x in arr:
        prefix ^= x
        count += freq.get(prefix ^ k, 0)
        freq[prefix] = freq.get(prefix, 0) + 1
    return count
```

```javascript
function countSubarraysWithXor(arr, k) {
    const freq = new Map([[0, 1]]);
    let prefix = 0, count = 0;
    for (const x of arr) {
        prefix ^= x;
        count += freq.get(prefix ^ k) || 0;
        freq.set(prefix, (freq.get(prefix) || 0) + 1);
    }
    return count;
}
```

Invariant: at each step `prefix` equals `P[i+1]`. A previous prefix `q` produces a subarray with XOR `prefix ^ q`; setting `q = prefix ^ k` gives all subarrays ending at `i` with XOR `k`.

## Which problems this approach solves in the real world

- Detecting tampered packet ranges using XOR-based checksums.
- Finding contiguous log spans with a target parity signature.
- Locating gene segments with a target XOR fingerprint in bioinformatics.
- Querying subarray parity in editor undo/redo histories represented as XOR deltas.
- Counting binary strings with a target imbalance in analytics.
- Verifying tape/disk block integrity over arbitrary spans.

## Pros and cons

**Pros**
- O(n) time and O(n) space — optimal for counting / membership queries.
- Single hashmap pass; no double loops.
- Reuses any prefix-sum intuition the reader already has.
- Works for negative numbers too because XOR is bit-defined.

**Cons**
- Subarray XOR != subarray sum; mixing them up is easy.
- The seeding `freq = {0: 1}` is essential and easy to forget.
- For ranges with updates, you need an alternative structure (XOR Fenwick tree).
- Edge case: when `k = 0`, off-by-one in the seed is the classic bug.

## Limitations

- Static arrays only; mutations break the prefix invariant.
- Counting overcounts duplicates of the same XOR value naturally — that's the point, but be aware in unique-pair problems.
- Doesn't directly give the actual subarrays, only counts; reconstruct by tracking indices.
- For 2D arrays you need 2D prefix XOR, which costs O(rows * cols).

## One example

**Problem**: Given an array of integers `nums` and an integer `k`, return the **number of contiguous subarrays whose XOR is exactly k**.

Constraints: 1 <= n <= 10^5, 0 <= nums[i] <= 10^9, 0 <= k <= 10^9.

**Input**: `nums = [4, 2, 2, 6, 4], k = 6`

**Output**: `4`

## Solution explanation

```python
def count_subarrays_with_xor(nums, k):
    freq = {0: 1}
    prefix = 0
    count = 0
    for x in nums:
        prefix ^= x
        count += freq.get(prefix ^ k, 0)
        freq[prefix] = freq.get(prefix, 0) + 1
    return count
```

Walk-through on `nums = [4,2,2,6,4], k = 6`:

| i | x | prefix | want (prefix^k) | freq before | matches | count | freq after |
|---|---|--------|-----------------|-------------|---------|-------|------------|
| 0 | 4 | 4 | 4^6 = 2 | {0:1} | 0 | 0 | {0:1, 4:1} |
| 1 | 2 | 6 | 6^6 = 0 | {0:1, 4:1} | 1 | 1 | {0:1, 4:1, 6:1} |
| 2 | 2 | 4 | 4^6 = 2 | {0:1, 4:1, 6:1} | 0 | 1 | {0:1, 4:2, 6:1} |
| 3 | 6 | 2 | 2^6 = 4 | {0:1, 4:2, 6:1} | 2 | 3 | {0:1, 4:2, 6:1, 2:1} |
| 4 | 4 | 6 | 6^6 = 0 | {0:1, 4:2, 6:1, 2:1} | 1 | 4 | {0:1, 4:2, 6:2, 2:1} |

The 4 subarrays are: `[4,2]`, `[2,2,6,4]`, `[2,6]`, `[6]`. (Note: `[2,6]` and `[2,2,6]^[2] = 6` arise from the two prefix-`4` entries when prefix reaches 2.) Correctness: at each index, `freq[prefix ^ k]` counts every earlier prefix that combines with the current one to form a subarray whose XOR equals `k`; summing across all indices visits every valid subarray exactly once.

- **Time**: O(n) amortised hashmap operations.
- **Space**: O(n) for the frequency map.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Single Number | https://leetcode.com/problems/single-number/ |
| Medium | XOR Queries of a Subarray | https://leetcode.com/problems/xor-queries-of-a-subarray/ |
| Medium | Count Triplets That Can Form Two Arrays of Equal XOR | https://leetcode.com/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/ |
