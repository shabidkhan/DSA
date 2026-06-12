# Bit Checks (Set / Clear / Toggle / Test)

## What is this

Bit checks are the elementary operations that read and mutate individual bits inside an integer treated as a flat array of booleans. The four core operations are: **test** (is bit i set?), **set** (turn bit i on), **clear** (turn bit i off), and **toggle** (flip bit i). Built on those primitives you get **isolate-lowest-bit** (`x & -x`), **drop-lowest-bit** (`x & (x-1)`), and **population count** (Kernighan-style or builtin).

These are the workhorse instructions of bitmask DP, flag fields, Bloom filters, fast sets, and many low-level systems APIs. Because each operation is a single CPU instruction, code that uses bit checks routinely beats logically equivalent boolean-array code by an order of magnitude.

## Why we use

- They compress a vector of booleans into a single integer — vastly cheaper than a list/array.
- All four primitives are one CPU op each; loops over bits are correspondingly tight.
- They compose to give clever tricks: `x & (x-1)` clears the lowest set bit, used in popcount and subset DP.
- They are the canonical interface for flag fields in systems APIs (open flags, mmap protections, permission bits).

## How to implement

```
test:   (x >> i) & 1               # or  (x & (1 << i)) != 0
set:    x |= (1 << i)
clear:  x &= ~(1 << i)
toggle: x ^= (1 << i)

lowest_bit:  x & -x                # isolates the lowest set bit as its own number
drop_lowest: x & (x - 1)           # turns off the lowest set bit
popcount:    while x: x &= x-1; c+=1   # counts set bits in O(#set bits)
```

```python
def is_set(x, i):  return (x >> i) & 1
def set_bit(x, i): return x | (1 << i)
def clear_bit(x, i): return x & ~(1 << i)
def toggle_bit(x, i): return x ^ (1 << i)

def popcount(x):
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c
```

```javascript
const isSet    = (x, i) => ((x >> i) & 1) === 1;
const setBit   = (x, i) => x | (1 << i);
const clearBit = (x, i) => x & ~(1 << i);
const toggleBit= (x, i) => x ^ (1 << i);
```

Invariant: each primitive touches only bit `i`; all other bits are guaranteed unchanged because the mask `1 << i` is non-zero only at position `i`.

## Which problems this approach solves in the real world

- File mode flags in POSIX (`O_RDONLY | O_NONBLOCK`).
- Permission bits for ACLs (read/write/execute).
- Feature flags packed into a configuration integer.
- Bloom-filter membership tests in caches and database indexes.
- Bitmask DP state transitions (mark element i as used).
- Compact hardware register manipulation in embedded firmware.

## Pros and cons

**Pros**
- One CPU instruction per operation — extremely fast.
- 64 booleans fit in one register; cache-friendly.
- Composes well with arithmetic tricks (`x & -x`, `x & (x-1)`).
- Universally supported across CPUs and languages.

**Cons**
- Reading code requires bit-twiddling fluency.
- Off-by-one and signed-shift mistakes are common (especially in C/Java).
- Hard cap: only as many bits as the word width (32 or 64) without big-int.
- JS bitwise ops force to 32-bit signed — beware of values > 2^31.

## Limitations

- Cannot represent more than word-size booleans without big-int or arrays of words.
- Right-shift on signed integers is arithmetic in some languages, logical in others.
- Languages differ on operator precedence; `(x & 1) == 0` vs `x & 1 == 0`.
- Negative integers as bitmasks behave differently in Python (infinite precision) vs JS (32-bit).

## One example

**Problem**: Given an integer `n` (0 <= n <= 2^31 - 1), return the number of `1` bits in its binary representation. This is also known as the Hamming weight.

Constraints: 0 <= n <= 2^31 - 1.

**Input**: `n = 11`  (binary `1011`)

**Output**: `3`

## Solution explanation

```python
def hamming_weight(n):
    count = 0
    while n:
        n &= n - 1     # drop the lowest set bit
        count += 1
    return count
```

For `n = 11 (binary 1011)`:

| Step | n (binary) | n - 1 (binary) | n & (n-1) | count |
|------|-----------|----------------|-----------|-------|
| 1 | 1011 | 1010 | 1010 (=10) | 1 |
| 2 | 1010 | 1001 | 1000 (=8) | 2 |
| 3 | 1000 | 0111 | 0000 (=0) | 3 |
| 4 | 0000 | — | loop ends | 3 |

Correctness: the identity `n & (n - 1)` clears exactly the lowest set bit of `n` because subtracting one flips the lowest set bit to 0 and turns every lower bit on, so ANDing keeps everything above the lowest set bit unchanged and zeros from that bit down. The loop therefore runs exactly once per set bit, giving the popcount.

- **Time**: O(k) where k is the number of set bits (at most 32).
- **Space**: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Number of 1 Bits | https://leetcode.com/problems/number-of-1-bits/ |
| Easy | Power of Two | https://leetcode.com/problems/power-of-two/ |
| Medium | Counting Bits | https://leetcode.com/problems/counting-bits/ |
