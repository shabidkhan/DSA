# Bit Manipulation Patterns

## Folder structure

```
14-Bit-manipulation/
├── README.md
├── 01-Core/
│   ├── 01-XOR-pattern/README.md
│   └── 02-Bit-masking/README.md
└── 02-Usage/
    ├── 01-Subset-via-bits/README.md
    ├── 02-Bit-checks/README.md
    └── 03-Prefix-XOR/README.md
```

## What is this

Bit manipulation treats integers as flat arrays of booleans and uses bitwise operators (AND, OR, XOR, NOT, shifts) to do constant-time work on whole groups of bits at once. This unlocks two superpowers: extremely tight low-level optimisations (set/clear/toggle a single flag in one instruction) and elegant algorithmic tricks (XOR-pair cancellation, subset enumeration via bitmasks, prefix XOR for subarray queries).

The family splits into two halves: **core** (the foundational operations — XOR patterns and bit masking) and **usage** (subset enumeration via bitmasks, bit checks like set/clear/toggle/popcount, and prefix-XOR for subarray problems). Once you internalise the few key identities (`x ^ x = 0`, `x & -x` isolates the lowest set bit, `x & (x-1)` clears it), bit problems become formulaic.

## Why we use

- Bitwise ops are single CPU instructions — orders of magnitude faster than equivalent boolean arrays.
- 64 booleans fit in one register; bitmask DP for n ≤ 20 becomes routine.
- XOR's self-inverse property gives O(n) O(1)-space "find the unique element" solutions.
- Bit checks are the API of choice for flag fields in systems code.

## How to implement

```
test:        (x >> i) & 1
set:         x |= (1 << i)
clear:       x &= ~(1 << i)
toggle:      x ^= (1 << i)
lowest bit:  x & -x
drop lowest: x & (x - 1)
popcount:    while x: x &= x-1; count += 1

XOR identities: x ^ x = 0;  x ^ 0 = x;  XOR is associative + commutative
Prefix XOR:  P[i] = a[0] ^ a[1] ^ ... ^ a[i-1];  sub(l,r) = P[r+1] ^ P[l]
```

Subpatterns in this folder:

- **01-Core** — XOR patterns and bit masking primitives.
- **02-Usage** — subset via bits, bit checks (set/clear/toggle), prefix XOR.

## Which problems this approach solves in the real world

- File mode flags (`O_RDWR | O_NONBLOCK`) in operating systems.
- Permission bits in ACLs.
- Bloom filter membership tests.
- IP routing via bitwise prefix masks.
- Bitmask DP for travelling salesman with n ≤ 20.
- Compact feature flags in configuration systems.

## Pros and cons

**Pros**
- One CPU instruction per operation — extremely fast.
- Compresses 64 booleans into one register.
- XOR gives elegant O(n) O(1)-space algorithms (single number, missing number).
- Subset enumeration via masks is iterative and cache-friendly.

**Cons**
- Bit-twiddling code is hard to read and review.
- Off-by-one in shifts and signed/unsigned mismatches are classic bug sources.
- JavaScript bitwise ops coerce to 32-bit signed — values > 2^31 break silently.
- Limited to word size unless you use big-integer libraries.

## Limitations

- Bitmask DP is exponential in the number of bits — n must be small.
- Can't represent more than word-size booleans without arrays of words.
- XOR tricks only work when each element appears an even number of times (or once).
- Negative-integer bit semantics differ across languages.
