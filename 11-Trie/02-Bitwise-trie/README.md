# Bitwise trie

## What is this

A bitwise trie (binary trie) stores integers as fixed-width bitstrings, one bit per edge. For 32-bit integers, each path from root to leaf has length 32 and the leaf represents one number. Insert and search are O(W) where W is the bit width — *constant* in practice.

The signature use is "maximum XOR of any two numbers in an array": for each candidate, walk the trie greedily preferring the *opposite* bit at every level. That maximizes XOR in O(W).

## Why we use

- O(W) insert and query — constant for fixed-width ints.
- Greedy bit-by-bit decisions match XOR semantics exactly.
- Enables max-XOR pair queries that are O(n^2) by brute force.
- Composable with prefix-XOR for subarray-XOR problems.

## How to implement

```
class Node: children = [None, None]

insert(x):
    n = root
    for b in bits_high_to_low(x):
        n.children[b] = n.children[b] or Node()
        n = n.children[b]

max_xor_with(x):
    n = root
    out = 0
    for b in bits_high_to_low(x):
        want = 1 - b
        if n.children[want]:
            out |= (1 << shift)
            n = n.children[want]
        else:
            n = n.children[b]
    return out
```

```python
class BitTrie:
    def __init__(self, W=31):
        self.root = [None, None]
        self.W = W

    def insert(self, x):
        n = self.root
        for i in range(self.W, -1, -1):
            b = (x >> i) & 1
            if n[b] is None:
                n[b] = [None, None]
            n = n[b]

    def max_xor_with(self, x):
        n = self.root
        out = 0
        for i in range(self.W, -1, -1):
            b = (x >> i) & 1
            want = 1 - b
            if n[want] is not None:
                out |= (1 << i)
                n = n[want]
            else:
                n = n[b]
        return out

def maximumXOR(nums):
    t = BitTrie()
    best = 0
    for x in nums:
        t.insert(x)
    for x in nums:
        best = max(best, t.max_xor_with(x))
    return best
```

Bit order matters — walking MSB first lets greedy choices maximize the higher-order bits.

## Which problems this approach solves in the real world

- IP routing tables (longest-prefix match on binary trie).
- Fast approximate-nearest-neighbor under Hamming distance.
- Cryptographic key compaction / lookup.
- Subarray XOR maximization in stream analytics.
- Detecting bit-pattern duplicates in fingerprinting systems.

## Pros and cons

**Pros**
- Truly constant-time per query at fixed bit-width.
- Greedy bit choices align with XOR's bitwise independence.
- Easy to combine with prefix-XOR for subarray problems.

**Cons**
- Memory grows linearly with number of inserted keys * W.
- Code is bit-fiddly; off-by-one on bit width is common.
- Not useful for non-XOR queries.

## Limitations

- Range-XOR queries need extra subtree-count bookkeeping.
- Floats / arbitrary objects need encoding before insertion.
- Pure XOR semantics only — does not generalize to other operations.

## One example

**Problem**: Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]` for any `i != j`.

**Input**: `nums = [3, 10, 5, 25, 2, 8]`
**Output**: `28`  (25 XOR 5 = 28)
**Constraints**: `1 <= n <= 2 * 10^5`, `0 <= nums[i] <= 2^31 - 1`.

## Solution explanation

```python
def findMaximumXOR(nums):
    t = BitTrie(W=30)
    best = 0
    for x in nums:
        t.insert(x)
    for x in nums:
        best = max(best, t.max_xor_with(x))
    return best
```

Walkthrough on `nums = [3, 10, 5, 25, 2, 8]`, focusing on `x = 5` after all inserts (binary: 00101, padded to 6 bits):

| bit (msb..lsb) | b | want=1-b | exists? | next path | out so far |
|----------------|---|----------|---------|-----------|------------|
| 16             | 0 | 1        | yes (25)| go 1      | 16         |
| 8              | 0 | 1        | yes     | go 1      | 24         |
| 4              | 1 | 0        | yes     | go 0      | 28         |
| 2              | 0 | 1        | no      | go 0      | 28         |
| 1              | 1 | 0        | no      | go 1      | 28         |

Result: 28. Time: O(n * W). Space: O(n * W).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | XOR Operation in an Array (LeetCode 1486) | https://leetcode.com/problems/xor-operation-in-an-array/ |
| Medium | Maximum XOR of Two Numbers in an Array (LeetCode 421) | https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/ |
| Hard | Maximum XOR With an Element From Array (LeetCode 1707) | https://leetcode.com/problems/maximum-xor-with-an-element-from-array/ |
