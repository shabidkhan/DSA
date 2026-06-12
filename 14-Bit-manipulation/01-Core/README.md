# Bit Manipulation Core

## Folder structure

```
01-Core/
├── README.md
├── 01-XOR-pattern/README.md
└── 02-Bit-masking/README.md
```

## What is this

The Core of bit manipulation is the small library of identities that make individual bits — and small fixed-size sets — behave like numbers you can add, subtract, and toggle in O(1). Two ideas matter most: **XOR** as addition modulo 2 (with the magical property `a XOR a = 0` and `a XOR 0 = a`), and the **bitmask**, an integer whose bits represent membership in a set of up to ~30 (or ~62) elements.

XOR collapses pairs to zero, so when one element is unpaired you can find it by XORing everything in a single linear pass. Bitmasks let you encode an entire subset in one machine word, intersect via `&`, union via `|`, complement via `~`, flip a bit via `^`, and isolate the lowest set bit via `x & -x`. Together they unlock O(n) versions of problems that look like they should need a hash map and constant-space versions of problems that look like they need an array.

## Why we use

- Replaces auxiliary structures (hash map, set) with a single integer
- Each primitive (`&`, `|`, `^`, `<<`, `>>`) is one CPU cycle
- XOR trick removes the need to sort or hash when pairing data
- Bitmasks compress state for bitmask DP, where each state is one machine word

## How to implement

```text
# XOR pattern: find the unpaired element
function findUnpaired(nums):
    result = 0
    for x in nums:
        result ^= x
    return result   # all paired x cancel themselves
```

```text
# Bitmask: iterate every subset of {0..n-1}
for mask = 0 .. (1 << n) - 1:
    for i = 0 .. n-1:
        if (mask >> i) & 1:
            element i is in this subset

# Common one-liners
isBitSet(x, i) = (x >> i) & 1
setBit(x, i)   = x | (1 << i)
clearBit(x, i) = x & ~(1 << i)
toggleBit(x,i) = x ^ (1 << i)
lowestBit(x)   = x & -x
popcount(x)    = number of 1 bits in x
```

Subpatterns in this folder:

- **01-XOR-pattern** — pairing-cancellation problems: single number, missing number, two single numbers, swap without temp, subarray XOR equals K
- **02-Bit-masking** — encoding/decoding subsets in an integer; the foundation of subset enumeration and bitmask DP

## Which problems this approach solves in the real world

- Detecting the corrupted packet among matched parity pairs
- Storing presence/absence flags (permissions, feature gates) as one integer
- Constant-space duplicate detection on bounded-range integer streams
- Encoding small game-state in solvers (sliding puzzles, TSP up to ~20 cities)
- Producing fast checksums and hash mixers
- Compressing "have I visited node i?" arrays in graph traversal

## Pros and cons

**Pros**

- O(1) per operation, friendly to CPU pipelines
- Trivial space: one integer can encode a subset of up to ~30 elements
- Composes cleanly with DP, often turning O(n²) state into O(n · 2^n)
- Self-inverse: XORing twice undoes itself, which is useful in toggles

**Cons**

- Off-by-one bit errors are easy and silent
- Signed-integer right shift behaviour varies across languages
- Limited by word width — set elements beyond ~62 needs big-int or multiple words
- Code looks cryptic to readers unfamiliar with the idioms

## Limitations

- Bitmask DP is O(2^n × n) — usable only up to n ≈ 20
- XOR cancellation only finds a specific kind of "unpaired" element, not arbitrary anomalies
- Encoding non-boolean attributes per element requires multiple bits and careful packing
- Hard to debug from a hex dump alone; readable variable names and comments matter more here than elsewhere
