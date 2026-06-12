# Bit Manipulation Usage

## Folder structure

```
02-Usage/
├── README.md
├── 01-Subset-via-bits/README.md
├── 02-Bit-checks/README.md
└── 03-Prefix-XOR/README.md
```

## What is this

This folder applies the Core bit identities (XOR and bitmasking) to three recurring tasks: **iterating every subset** of a small ground set by treating the integers `0` through `2^n − 1` as bitmasks, **querying or mutating individual bits** to test parity / membership / flag state, and **using a prefix XOR array** to answer subarray-XOR queries in O(1) the same way prefix sums answer subarray-sum queries.

The grouping reflects how these patterns show up in interviews: an algorithm rarely uses bit manipulation in isolation — it borrows a bit primitive in service of a larger search, hash, or scan. So instead of being defined by "what operator are we using", these subpatterns are defined by "what problem-shape lets bit tricks save us a log factor or an entire data structure."

## Why we use

- Lets you replace a `Set<int>` with a single integer when elements are bounded
- O(1) per bit operation; whole-mask operations are still O(1) per word
- Prefix-XOR + hashmap is the canonical O(n) trick for "subarray XOR equals K"
- Subset enumeration via bitmask is shorter and faster than recursion

## How to implement

```text
# Subset enumeration
for mask = 0 .. (1 << n) - 1:
    subset = []
    for i = 0 .. n-1:
        if (mask >> i) & 1:
            subset.append(elements[i])
    process(subset)

# Bit checks
isOdd(x)        = x & 1
isPowerOfTwo(x) = x > 0 and (x & (x - 1)) == 0
countBits(x)    = popcount(x)
lowestSetBit(x) = x & -x

# Prefix XOR for subarray queries
prefix[0] = 0
prefix[i] = prefix[i-1] XOR nums[i-1]
XOR of nums[l..r] = prefix[r+1] XOR prefix[l]

# Subarrays with XOR == K via hashmap
count = 0; seen = {0: 1}; px = 0
for x in nums:
    px ^= x
    count += seen.get(px ^ K, 0)
    seen[px] = seen.get(px, 0) + 1
```

Subpatterns in this folder:

- **01-Subset-via-bits** — enumerate all subsets of an n-element set by iterating masks; bit i represents inclusion of element i
- **02-Bit-checks** — parity, power-of-two detection, lowest-set-bit isolation, popcount, set/clear/toggle on a flag word
- **03-Prefix-XOR** — prefix XOR array + hashmap to count subarrays with a target XOR, or find longest such subarray

## Which problems this approach solves in the real world

- Iterating all combinations of feature toggles in A/B testing
- Computing parity checksums for transmitted bytes
- Reading and updating permission bitfields in OS code (rwx, page-table flags)
- Counting bytes set on a small bitmap (e.g., visited tiles in a game)
- Detecting whether a number is a power of two for memory alignment
- Finding subarrays with target XOR in network log analytics

## Pros and cons

**Pros**

- One integer encodes an entire subset of up to ~30 elements
- Prefix XOR + hashmap is O(n) time, O(n) space
- Bit checks are branchless and CPU-friendly
- Combines naturally with bitmask DP, hashmaps, and sliding window

**Cons**

- Limited to small n — bitmask iteration is O(2^n)
- Off-by-one in bit indices is easy to miss
- Less readable than equivalent set / boolean-array code
- Sign-extension on right shift differs by language

## Limitations

- Doesn't work for elements beyond word width without big-int
- Prefix XOR trick works for XOR specifically; not all aggregates have inverse properties
- Iterating subsets is exponential — not for general-size problems
- Bit-twiddling skills are non-obvious; PR reviewers may push back without explanatory comments
