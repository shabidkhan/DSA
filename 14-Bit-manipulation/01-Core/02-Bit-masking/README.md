# Bitwise tricks

## What is this

A toolkit of constant-time identities for manipulating the **bits of an integer**: setting, clearing, toggling, and checking individual bits; isolating the lowest set bit; counting the number of set bits (popcount); and using bits as flags or as compact representations of small sets. The fundamental operators are AND `&`, OR `|`, XOR `^`, NOT `~`, left shift `<<`, and right shift `>>`. Most tricks combine two of these in a clever way to do in one CPU instruction what a loop would otherwise take O(bits) to do.

## Why we use

- O(1) (single CPU instruction) replacements for many O(log n) or O(n) operations.
- Compact representation: an n-element subset of `[0, 63]` fits in one 64-bit integer.
- Hardware-friendly: bitwise operations are branch-free and cache-free, often pipeline beautifully.
- Foundation for state-compression DP, fast set operations, and many low-level optimisations.

## How to implement

The essential identities (let `x` be an integer and `i` a bit index):

```
set bit i:          x | (1 << i)
clear bit i:        x & ~(1 << i)
toggle bit i:       x ^ (1 << i)
check bit i:        (x >> i) & 1        # → 0 or 1

is x a power of 2:  x > 0 and (x & (x - 1)) == 0
lowest set bit:     x & -x              # → integer with only that bit
clear lowest set:   x & (x - 1)
count set bits:     repeatedly clear lowest set; or use language popcount
all bits below i:   (1 << i) - 1
flip bits up to i:  x ^ ((1 << (i + 1)) - 1)
```

Python — popcount (Brian Kernighan's algorithm):

```python
def popcount(x: int) -> int:
    count = 0
    while x:
        x &= x - 1       # clear the lowest set bit
        count += 1
    return count
```

Python — iterate over set bits one at a time:

```python
def set_bit_indices(x: int) -> list[int]:
    out = []
    while x:
        lowest = x & -x       # isolate lowest set bit
        out.append(lowest.bit_length() - 1)
        x ^= lowest           # clear it
    return out
```

Invariant for `x & (x - 1)`: subtracting 1 from `x` flips the lowest set bit to 0 **and** turns every lower 0-bit into 1. ANDing with the original cancels everything that changed, leaving only the bits that were already set above the lowest. So one application "drops" the lowest set bit deterministically.

## Which problems this approach solves in the real world

- **Permission / flag sets**: AND/OR/XOR for adding, removing, toggling capability bits in a single field.
- **Bloom filters and counting sketches**: set bits via hash, check via mask.
- **Fast modulo by power of two**: `x % 2^k == x & (2^k - 1)` — one cycle vs a division.
- **Compact graph representations**: adjacency rows packed into 64-bit ints for graphs with ≤ 64 nodes.
- **Game state encoding**: a tic-tac-toe board or 8-puzzle position fits in a small bitmask for fast hashing.

## Pros and cons

**Pros**
- Single-instruction operations on the CPU — extremely fast.
- Branch-free: no pipeline stalls, no mispredictions.
- Compact: 64 boolean flags in 8 bytes.
- Composes with DP (bitmask DP) for problems where the "state" is a subset of a small universe.

**Cons**
- Cryptic on first read — operator precedence (`==` binds tighter than `&` in C/Java) and sign extension on `>>` are notorious traps.
- Limited to fixed-width integers in most languages (Python's arbitrary precision saves you, but at a cost).
- Doesn't help when the operation isn't expressible as a simple bit pattern (e.g. multiplication-mod by a non-power-of-two).

## Limitations

- 64-bit ints cap the universe at 64 elements; beyond that you need bit arrays or chunks.
- Bit tricks make code less readable; document the identity used unless the team is bit-fluent.
- Signed right shift `>>` propagates the sign bit in C/Java — use unsigned `>>>` or cast carefully.

## One example

**Problem**: Given a positive integer `n`, return the **number of 1-bits** in its binary representation (also known as the **Hamming weight**). Constraints: the input is an unsigned 32-bit integer, `0 ≤ n ≤ 2^31 - 1`.

**Input**: `n = 11` (binary `1011`)
**Output**: `3`

## Solution explanation

```python
def hamming_weight(n: int) -> int:
    count = 0
    while n:
        n &= n - 1     # clear the lowest set bit
        count += 1
    return count
```

Walk-through on `n = 11` (binary `0000 1011`):

| step | n (binary) | n - 1 (binary) | n & (n - 1) (binary) | count |
|------|------------|----------------|----------------------|-------|
| 0    | 0000 1011  | 0000 1010      | 0000 1010 = 10       | 1     |
| 1    | 0000 1010  | 0000 1001      | 0000 1000 = 8        | 2     |
| 2    | 0000 1000  | 0000 0111      | 0000 0000 = 0        | 3     |
| 3    | 0          | —              | loop ends            | **3** |

The loop runs exactly **once per set bit** — much better than scanning all 32 bits when most are zero. Each iteration is O(1) on the CPU, so the algorithm is O(set bits), with worst case O(32) for a fully-set int.

- **Time**: O(k) where k is the number of set bits (≤ word size).
- **Space**: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Number of 1 Bits** — compute the Hamming weight. | https://leetcode.com/problems/number-of-1-bits/ |
| Medium | **Counting Bits** — return an array `ans[i] = popcount(i)` for `0 ≤ i ≤ n`, in O(n) using `ans[i] = ans[i >> 1] + (i & 1)`. | https://leetcode.com/problems/counting-bits/ |
| Hard   | **Maximum XOR of Two Numbers in an Array** — bit-by-bit greedy + trie. | https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/ |
