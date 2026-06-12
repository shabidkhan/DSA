# Radix sort

## What is this

Radix sort sorts integers (or fixed-length strings) digit by digit, using a stable counting sort per digit. LSD radix sort starts with the least-significant digit; MSD starts from the most significant. After D passes the array is sorted by all D digits. Total time is O(D * (n + b)) where b is the digit base.

When integers have a bounded width (e.g. 32-bit), radix sort runs in linear time on n for a small constant D = ceil(W / log b).

## Why we use

- Linear time on fixed-width integers and strings.
- Stable (because the digit-level sort is counting sort).
- Beats O(n log n) comparison sorts on long-key, large-n workloads.
- Cache-friendly when written carefully.

## How to implement

```
LSD radix on base 10:
    for d in 0..D-1:
        counting_sort_by_digit(a, d)
```

```python
def radix_sort(a):
    if not a: return a
    mx = max(a)
    exp = 1
    while mx // exp > 0:
        a = _counting_by_digit(a, exp)
        exp *= 10
    return a

def _counting_by_digit(a, exp):
    counts = [0] * 10
    for x in a:
        counts[(x // exp) % 10] += 1
    for i in range(1, 10):
        counts[i] += counts[i - 1]
    out = [0] * len(a)
    for x in reversed(a):
        d = (x // exp) % 10
        counts[d] -= 1
        out[counts[d]] = x
    return out
```

Use base 256 or higher in performance code — fewer passes at the cost of larger counts arrays.

## Which problems this approach solves in the real world

- Sorting fixed-length identifiers (UUID prefixes, phone numbers).
- IP-address sorting via four-pass base-256 radix.
- Database integer-key indexing.
- Suffix-array construction (DC3 / SA-IS variants).
- Image / pixel-value sorting when values are bounded.

## Pros and cons

**Pros**
- Linear time when D is small.
- Stable.
- Excellent for long-key + large-n workloads.

**Cons**
- O(D * (n + b)) memory pressure on the counts arrays.
- Negative integers require an offset or sign-bit handling.
- Variable-length keys complicate the algorithm.

## Limitations

- Only works on keys that can be decomposed into ordered digits.
- Floats need IEEE-754 trick (sort by bit pattern with sign flip).
- Base choice trades passes vs counts-array size.

## One example

**Problem**: Sort a positive-integer array `nums` in non-decreasing order using LSD radix sort base 10.

**Input**: `nums = [170, 45, 75, 90, 802, 24, 2, 66]`
**Output**: `[2, 24, 45, 66, 75, 90, 170, 802]`
**Constraints**: `1 <= n <= 5 * 10^4`, `0 <= nums[i] <= 10^9`.

## Solution explanation

`radix_sort` from above. Walkthrough on the input across three passes:

| pass | digit position | order produced                             |
|------|----------------|--------------------------------------------|
| 1    | ones           | [170, 90, 802, 2, 24, 45, 75, 66]          |
| 2    | tens           | [802, 2, 24, 45, 66, 170, 75, 90]          |
| 3    | hundreds       | [2, 24, 45, 66, 75, 90, 170, 802]          |

Each pass is a stable counting sort by that digit. After the most-significant digit, the array is fully sorted.

Time: O(D * (n + 10)). Space: O(n + 10).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Sort Array By Parity (LeetCode 905) | https://leetcode.com/problems/sort-array-by-parity/ |
| Medium | Maximum Gap (LeetCode 164) | https://leetcode.com/problems/maximum-gap/ |
| Hard | Sum of Floored Pairs (LeetCode 1862) | https://leetcode.com/problems/sum-of-floored-pairs/ |
