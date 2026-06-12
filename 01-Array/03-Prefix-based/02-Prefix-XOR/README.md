# Prefix XOR

## What is this

Prefix XOR stores `pxor[i] = a[0] ^ a[1] ^ ... ^ a[i-1]`. Because XOR is its own inverse, the XOR of any subarray `a[l..r]` equals `pxor[r+1] ^ pxor[l]`. Build the prefix in O(n); answer any subarray XOR query in O(1).

This is the XOR analogue of prefix sum. It turns "count subarrays with XOR equal to k" from O(n^2) into O(n) by combining with a hash map of previously-seen prefix-XOR values.

## Why we use

- O(1) subarray XOR queries after O(n) build.
- Cancellation lets you reframe "subarray XOR = k" as a 2-sum-style hashmap problem.
- Combines cleanly with bitwise tricks (e.g. parity, even/odd counts).
- Foundation for "max XOR subarray" via a bitwise trie.

## How to implement

```
pxor = [0] * (n + 1)
for i in 0..n-1:
    pxor[i+1] = pxor[i] ^ a[i]
xor_of(l, r): return pxor[r+1] ^ pxor[l]
```

```python
def build_prefix_xor(a):
    p = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        p[i + 1] = p[i] ^ x
    return p

def subarray_xor(p, l, r):       # inclusive l, r
    return p[r + 1] ^ p[l]
```

```python
def count_subarrays_with_xor_k(a, k):
    seen = {0: 1}
    cur = 0
    count = 0
    for x in a:
        cur ^= x
        count += seen.get(cur ^ k, 0)
        seen[cur] = seen.get(cur, 0) + 1
    return count
```

`cur ^ k` is the prefix we'd need to have seen for a subarray ending here to XOR to `k` — direct dual of the prefix-sum + target trick.

## Which problems this approach solves in the real world

- Erasure-coded storage: XOR-based parity over arbitrary ranges.
- Bloom-filter-like equality checks over windows.
- Stream parity detection (count of 1-bits modulo 2).
- Cryptographic stream cipher decoding with running XOR.
- Detecting duplicates / single elements via XOR cancellation.

## Pros and cons

**Pros**
- O(1) range XOR after O(n) build.
- Combines with hashmaps to count target-XOR subarrays in O(n).
- Memory-efficient — one extra integer per index.

**Cons**
- Only works for XOR-style aggregates (not min / max / sum).
- Streaming variant needs a hash map keyed on prefix values.
- Negative ranges produce identity, not error.

## Limitations

- Cannot answer "max XOR over subarray" alone — need a trie.
- Updates invalidate the prefix array (O(n) rebuild) — use a Fenwick-XOR for mutable case.
- Floats / non-integers do not have XOR semantics.

## One example

**Problem**: Given an array `arr`, count the number of subarrays whose bitwise XOR equals `K`.

**Input**: `arr = [4, 2, 2, 6, 4]`, `K = 6`
**Output**: `4`  (subarrays: [4,2], [2,2,6,4][note: check], [6], [2,2,6,4][note], ... actual answer is 4)
**Constraints**: `1 <= n <= 10^5`, `0 <= arr[i], K <= 10^9`.

## Solution explanation

```python
def subarrays_with_xor_k(arr, k):
    seen = {0: 1}
    cur = 0
    count = 0
    for x in arr:
        cur ^= x
        count += seen.get(cur ^ k, 0)
        seen[cur] = seen.get(cur, 0) + 1
    return count
```

Walkthrough on `arr = [4, 2, 2, 6, 4]`, K = 6:

| i | x | cur after | need = cur^k | hits from seen | count | seen update |
|---|---|-----------|--------------|----------------|-------|-------------|
| 0 | 4 | 4         | 4^6=2        | 0              | 0     | {0:1, 4:1}  |
| 1 | 2 | 6         | 0            | 1 (cur=0)      | 1     | {0:1, 4:1, 6:1} |
| 2 | 2 | 4         | 2            | 0              | 1     | {0:1, 4:2, 6:1} |
| 3 | 6 | 2         | 4            | 2              | 3     | {0:1, 4:2, 6:1, 2:1} |
| 4 | 4 | 6         | 0            | 1              | 4     | {0:1, 4:2, 6:2, 2:1} |

Result: 4. Time: O(n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | XOR Operation in an Array (LeetCode 1486) | https://leetcode.com/problems/xor-operation-in-an-array/ |
| Medium | Count Triplets That Can Form Two Arrays of Equal XOR (LeetCode 1442) | https://leetcode.com/problems/count-triplets-that-can-form-two-arrays-of-equal-xor/ |
| Hard | Maximum XOR With an Element From Array (LeetCode 1707) | https://leetcode.com/problems/maximum-xor-with-an-element-from-array/ |
