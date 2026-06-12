# XOR tricks

## What is this

A family of identities that exploit the algebraic properties of the **XOR** (exclusive-or, `^`) operator: `a ^ a = 0`, `a ^ 0 = a`, and `^` is both commutative and associative. These three facts mean that XORing a value with itself **cancels it out**, leaving any value that appears an odd number of times to "survive" a long XOR-chain. This single insight powers the classic "find the one non-duplicate", "swap without a temporary", "find the missing number", and a surprising variety of low-overhead tricks.

## Why we use

- Solves a class of problems in O(n) time, **O(1) space** — beating any hash-set-based approach in memory.
- The identities are CPU primitives (single-instruction XOR), so the constant factor is tiny.
- XOR is its own inverse: `a ^ b ^ b = a`. This means you can "encrypt" and "decrypt" with the same operation — useful for prefix XORs over arrays.

## How to implement

Core identities:

```
a ^ a = 0
a ^ 0 = a
a ^ b = b ^ a              (commutative)
(a ^ b) ^ c = a ^ (b ^ c)  (associative)
```

Python — single number (every element appears twice except one):

```python
def single_number(nums: list[int]) -> int:
    result = 0
    for x in nums:
        result ^= x
    return result
```

Python — swap two variables without a temporary:

```python
def xor_swap(a: int, b: int) -> tuple[int, int]:
    a ^= b
    b ^= a
    a ^= b
    return a, b
```

Python — find the missing number in `[0..n]` from a length-n array:

```python
def missing_number(nums: list[int]) -> int:
    result = len(nums)
    for i, x in enumerate(nums):
        result ^= i ^ x
    return result
```

Python — prefix-XOR range queries (XOR of any subarray in O(1) after O(n) preprocessing):

```python
def build_prefix_xor(arr: list[int]) -> list[int]:
    prefix = [0] * (len(arr) + 1)
    for i, x in enumerate(arr):
        prefix[i + 1] = prefix[i] ^ x
    return prefix

def range_xor(prefix: list[int], l: int, r: int) -> int:
    return prefix[r + 1] ^ prefix[l]
```

Invariant for "single number": the running XOR after processing the first `k` elements equals the XOR of every value that has appeared an **odd** number of times so far. When every duplicate appears exactly twice, all duplicates cancel and only the singleton survives.

## Which problems this approach solves in the real world

- **Network packet integrity**: simple parity / checksum using cumulative XOR.
- **Inventory reconciliation**: find the one item present in shipped-but-not-received logs when every other item appears in both.
- **One-time pad encryption**: XOR plaintext with a random key, decrypt by XORing with the same key.
- **Compact prefix-XOR range queries**: precompute `prefix[i] = a[0] ^ a[1] ^ ... ^ a[i-1]` for O(1) range XORs.
- **De-duplicating sensor IDs in a stream** where each duplicate must be paired and reported once.

## Pros and cons

**Pros**
- O(n) time, **O(1) space** — beats hash-set solutions on memory.
- Single CPU instruction per step.
- Order-independent: you can XOR elements in any order or in parallel chunks.
- Composes with prefix sums for fast range XOR queries.

**Cons**
- Only handles **specific** structures: "every element appears even times except one odd-count element" or similar. For arbitrary "find the duplicate", XOR alone isn't enough.
- Two distinct missing/extra elements require an extra step (split by a discriminating bit).
- Numerical interpretation only — doesn't work on floats, strings, or arbitrary objects (you'd need to hash them first, defeating the purpose).

## Limitations

- "Find two singletons" requires splitting the XOR result by its lowest set bit — slightly more involved.
- Doesn't generalise to "find the element appearing three times when others appear twice" — that needs a 3-state counter (combine `ones`, `twos`).
- For floats / strings, XOR doesn't apply directly.

## One example

**Problem**: Given a non-empty array of integers `nums`, **every element appears twice except for one**. Find that single one. Solve it with O(n) time and O(1) extra space. Constraints: `1 ≤ nums.length ≤ 3·10^4`.

**Input**: `nums = [4, 1, 2, 1, 2]`
**Output**: `4`

## Solution explanation

```python
def single_number(nums: list[int]) -> int:
    result = 0
    for x in nums:
        result ^= x
    return result
```

Walk-through on `nums = [4, 1, 2, 1, 2]`:

| step | x | result (decimal) | result (binary) | comment           |
|------|---|------------------|-----------------|-------------------|
| 0    | 4 | 4                | 100             | seen 4 once       |
| 1    | 1 | 5                | 101             | seen 1 once       |
| 2    | 2 | 7                | 111             | seen 2 once       |
| 3    | 1 | 6                | 110             | 1 cancels         |
| 4    | 2 | 4                | 100             | 2 cancels → **4** |

XOR's associativity and commutativity mean the final result is `4 ^ 1 ^ 2 ^ 1 ^ 2 = 4 ^ (1 ^ 1) ^ (2 ^ 2) = 4 ^ 0 ^ 0 = 4`. Every duplicate cancels; only the singleton remains. The algorithm makes **one pass** over the array and uses **one integer** of state — far better than a hash set tracking seen elements.

- **Time**: O(n).
- **Space**: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Single Number** — every element appears twice except one. | https://leetcode.com/problems/single-number/ |
| Medium | **Single Number III** — exactly two elements appear once, others twice; XOR all, then split by the lowest set bit. | https://leetcode.com/problems/single-number-iii/ |
| Hard   | **Maximum XOR of Two Numbers in an Array** — greedy bit-by-bit construction using a binary trie. | https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/ |
