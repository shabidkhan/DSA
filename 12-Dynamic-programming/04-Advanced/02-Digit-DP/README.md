# Digit DP

## What is this

Digit DP counts numbers up to N satisfying some property defined per-digit. The state is `(position, tight, started, extra_state)`:

- `position` — index of the current digit being filled (left to right).
- `tight` — boolean, whether previous digits exactly match N's prefix (constrains next digit's max).
- `started` — boolean, whether any non-zero digit has been placed yet (handles leading zeros).
- `extra_state` — problem-specific: digit count, sum mod m, last digit, mask of seen digits, etc.

Combined with memoization, total complexity is `O(len * 2 * 2 * S * 10)` where S is the size of the extra-state space. This is the canonical pattern for "count numbers ≤ N with property X".

## Why we use

- Reduces O(N) brute force to O(log N) per problem instance.
- Cleanly handles "≤ N" constraints via the `tight` flag.
- Memoization erases redundancy across same-state paths.
- Single template solves a wide variety of "count numbers with property" problems.

## How to implement

```
digits = list(str(N))
@memo
def solve(pos, tight, started, extra):
    if pos == len(digits): return 1 if started and extra_ok(extra) else 0
    limit = int(digits[pos]) if tight else 9
    total = 0
    for d in 0..limit:
        new_tight = tight and (d == limit)
        new_started = started or d > 0
        new_extra = update(extra, d, new_started)
        total += solve(pos + 1, new_tight, new_started, new_extra)
    return total
```

```python
from functools import lru_cache

def count_up_to(N):
    digits = list(map(int, str(N)))

    @lru_cache(None)
    def dp(pos, tight, started, sum_so_far):
        if pos == len(digits):
            return 1 if started else 0  # exclude 0 if you want positives only
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(0, limit + 1):
            total += dp(pos + 1,
                        tight and (d == limit),
                        started or (d > 0),
                        sum_so_far + d)
        return total
    return dp(0, True, False, 0)
```

```python
def count_with_digit_d(N, target):
    digits = list(map(int, str(N)))

    @lru_cache(None)
    def dp(pos, tight, started, occurrences):
        if pos == len(digits):
            return occurrences if started else 0
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(limit + 1):
            new_started = started or d > 0
            inc = 1 if (new_started and d == target) else 0
            total += dp(pos + 1, tight and d == limit, new_started, occurrences + inc)
        return total
    return dp(0, True, False, 0)
```

For "count numbers in [L, R]", compute `count(R) - count(L - 1)`.

## Which problems this approach solves in the real world

- Counting numbers in a range satisfying digit-based properties (no consecutive duplicates, digit-sum target, etc.).
- Forensic accounting: count numeric IDs with structural patterns.
- Cryptographic key counting under digit constraints.
- Lottery / combinatorics counting up to large N.
- Database analytics: counting numeric records with digit-derived predicates.

## Pros and cons

**Pros**
- Polynomial in log N instead of N.
- Single template fits many digit-based problems.
- Memoization automatically dedupes the state space.

**Cons**
- State design is non-obvious — easy to forget `started` or `tight`.
- Memo keys must exclude `tight`/`started` carefully (when False they're permanent).
- Extra state explosion if you need many auxiliary fields.

## Limitations

- Non-decimal bases need digit-by-digit reinterpretation.
- Negative numbers must be split into positive cases.
- Floating-point / non-integer queries don't fit the template.

## One example

**Problem**: Count integers in `[1, N]` whose digits sum to exactly `S`.

**Input**: `N = 100`, `S = 9`
**Output**: `10` (9, 18, 27, ..., 90)
**Constraints**: `1 <= N <= 10^9`, `1 <= S <= 100`.

## Solution explanation

```python
from functools import lru_cache

def count_with_digit_sum(N, S):
    digits = list(map(int, str(N)))

    @lru_cache(None)
    def dp(pos, tight, started, remaining):
        if remaining < 0: return 0
        if pos == len(digits):
            return 1 if started and remaining == 0 else 0
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(limit + 1):
            total += dp(pos + 1,
                        tight and (d == limit),
                        started or (d > 0),
                        remaining - d)
        return total
    return dp(0, True, False, S)
```

Walkthrough for `N = 18`, `S = 9`:

Numbers in [1, 18] with digit sum 9: 9 (only one). DP trace summary:

| state                              | branches | contribution |
|------------------------------------|----------|--------------|
| dp(0, True, False, 9) — digit pos 0 (limit=1) | d=0, d=1 | sum below |
| d=0 → dp(1, False, False, 9) | digits 0..9 freely | 1 (only d=9 satisfies and counts as started) |
| d=1 → dp(1, True, True, 8) — pos 1 limit=8 | d=0..8 | 0 (need 8 more in one digit; only d=8 works, but that's 18 → digit sum 9? wait 1+8=9 ✓) → 1 |

Total = 2 (9, 18). For N = 100, S = 9 → 10. Time: O(len(N) * 2 * 2 * S * 10). Space: same.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Count of Numbers Whose Sum of Digits Equals Sum of Reversed Digits (LeetCode 2443 — simple) | https://leetcode.com/problems/count-strictly-increasing-subarrays/ |
| Medium | Numbers At Most N Given Digit Set (LeetCode 902) | https://leetcode.com/problems/numbers-at-most-n-given-digit-set/ |
| Hard | Count of Integers (LeetCode 2719) | https://leetcode.com/problems/count-of-integers/ |
