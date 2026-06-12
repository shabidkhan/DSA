# Linear DP (1D, fixed-offset transitions)

## What is this

A dynamic programming pattern where the state is **one-dimensional** (`dp[i]`) and each `dp[i]` depends on a **constant number of earlier indices** — usually `dp[i-1]`, `dp[i-2]`, or some `dp[i-k]`. The transitions form a *linear* chain of dependencies, hence the name. Classic examples: Fibonacci, climbing stairs, house robber, decode ways.

The defining trait: the recurrence has constant fan-in (O(1) earlier values per state) and constant fan-out, so the table can be filled in O(n) time. Often the full table isn't needed — you can keep only the last few values, dropping memory to O(1).

## Why we use

- Solves "how many / what's the optimum at position i" problems in **O(n) time, O(1)–O(n) space**.
- The simplest DP shape — perfect for learning the paradigm before tackling 2D, knapsack, or interval DP.
- Easy to verify by hand: write out `dp[0], dp[1], ...` for a small input and inspect.
- Often a key sub-routine inside larger DPs.

## How to implement

```
dp = array of size n
dp[0] = base case
(dp[1] = ...)
for i in some_range:
    dp[i] = combine(dp[i-1], dp[i-2], ..., problem-specific terms)
return dp[n-1]
```

Python — Climbing Stairs (`dp[i] = dp[i-1] + dp[i-2]`):

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2     # dp[1], dp[2]
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
```

Python — House Robber (`dp[i] = max(dp[i-1], dp[i-2] + nums[i])`):

```python
def rob(nums: list[int]) -> int:
    prev_2, prev_1 = 0, 0   # rolling: dp[i-2], dp[i-1]
    for x in nums:
        prev_2, prev_1 = prev_1, max(prev_1, prev_2 + x)
    return prev_1
```

JavaScript — Decode Ways (`dp[i] = (one-char decode) + (two-char decode)`):

```javascript
function numDecodings(s) {
  const n = s.length;
  if (!n || s[0] === '0') return 0;
  let prev2 = 1, prev1 = 1;        // dp[0], dp[1]
  for (let i = 2; i <= n; i++) {
    let cur = 0;
    const one = parseInt(s.substring(i - 1, i));      // s[i-1]
    const two = parseInt(s.substring(i - 2, i));      // s[i-2..i-1]
    if (one >= 1 && one <= 9) cur += prev1;
    if (two >= 10 && two <= 26) cur += prev2;
    prev2 = prev1; prev1 = cur;
  }
  return prev1;
}
```

Invariant: when we compute `dp[i]`, the values `dp[i-1], dp[i-2], ...` already represent the correct answers for prefixes ending at those indices. The transition combines them into the answer at `i`.

## Recurrence pattern

| Problem            | State                                   | Transition                                              |
|--------------------|-----------------------------------------|---------------------------------------------------------|
| Fibonacci          | `dp[i]` = i-th Fibonacci number         | `dp[i] = dp[i-1] + dp[i-2]`                             |
| Climbing Stairs    | `dp[i]` = ways to reach step i          | `dp[i] = dp[i-1] + dp[i-2]`                             |
| House Robber       | `dp[i]` = max loot using houses [0..i]  | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`               |
| Decode Ways        | `dp[i]` = decodings of s[0..i-1]        | `dp[i] = dp[i-1]·[valid 1-digit] + dp[i-2]·[valid 2-digit]` |
| Min Cost Climbing  | `dp[i]` = min cost to reach step i      | `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])` |
| Jump Game (variant)| `dp[i]` = can reach step i              | `dp[i] = OR over j with dp[j] true and j+nums[j] >= i`  |

## Which problems this approach solves in the real world

- **Speech recognition / NLP**: number of valid segmentations of a sequence (decode ways).
- **Robotics path planning**: minimum-cost climbing along a sequence of cost-tagged steps.
- **Investment portfolio**: max profit when alternate-day rules apply (house-robber-style).
- **Genomic alignment scoring**: simple linear DP with affine gap costs.
- **Game design**: number of ways for a character to traverse a fixed sequence of platforms.
- **Compression**: number of valid token-decompositions of a stream.

## Pros and cons

**Pros**
- O(n) time — fast.
- O(1) space possible with rolling variables — minimal memory footprint.
- Tiny state — easy to debug by printing `dp[0..n]`.
- Linear scan; cache-friendly memory access pattern.

**Cons**
- Only works when the dependency is a **constant offset back** — for longer-range deps, you need a different DP shape.
- The base cases (`dp[0]`, `dp[1]`) are the most error-prone — off-by-one between "ways to reach step 0" vs "we start at step 0".
- Output sometimes requires returning `dp[n]` vs `dp[n-1]` — pick deliberately based on whether `n` is "count" or "index".

## Limitations

- Not suitable when each state depends on *all* earlier states (use Sequence-DP / O(n²) DP).
- Not suitable when state needs more than O(1) extra dimensions (use 2D-DP).
- For very large n with arithmetic on huge numbers, even O(1) memory may need bignum arithmetic.

## One example

**Problem**: You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses are connected to a security system that triggers if **two adjacent houses are robbed on the same night**. Given an array `nums` representing the amount in each house, return the **maximum amount you can rob** without triggering the alarm.
Constraints: `1 ≤ n ≤ 100`, `0 ≤ nums[i] ≤ 400`.

**Input**: `nums = [2, 7, 9, 3, 1]`
**Output**: `12` — rob houses 0, 2, 4 → `2 + 9 + 1 = 12`.

## Solution explanation

State: `dp[i]` = max amount you can rob considering houses `0..i`.
Transition: for house `i` you have two options:
- **Skip** house `i`: take `dp[i-1]`.
- **Rob** house `i`: take `dp[i-2] + nums[i]` (because you can't rob `i-1`).

Take the max. Base cases: `dp[-1] = 0`, `dp[0] = nums[0]`.

```python
def rob(nums: list[int]) -> int:
    prev_2, prev_1 = 0, 0     # dp[-1], dp[-1]; we'll shift in nums[0] as the first iteration
    for x in nums:
        prev_2, prev_1 = prev_1, max(prev_1, prev_2 + x)
    return prev_1
```

Walk-through on `[2, 7, 9, 3, 1]`:

| i | x | prev_2 in (was dp[i-2]) | prev_1 in (was dp[i-1]) | new prev_1 = max(prev_1, prev_2 + x) | dp[i] (=new prev_1) |
|---|---|---------|---------|----------------------------------|---------------|
| 0 | 2 | 0       | 0       | max(0, 0+2) = 2                  | 2             |
| 1 | 7 | 0       | 2       | max(2, 0+7) = 7                  | 7             |
| 2 | 9 | 2       | 7       | max(7, 2+9) = 11                 | 11            |
| 3 | 3 | 7       | 11      | max(11, 7+3) = 11                | 11            |
| 4 | 1 | 11      | 11      | max(11, 11+1) = 12               | 12            |

Final answer: **12**.

Correctness: by induction. Base cases (`dp[-1] = 0` and `dp[-2] = 0`) are trivially correct ("no houses available"). Inductive step: any optimal plan for houses `[0..i]` either skips house `i` (reducing to the optimal plan for `[0..i-1]`) or robs house `i` (forcing skip of `i-1`, then optimal plan for `[0..i-2]` plus `nums[i]`). Taking the max covers both.

- **Time**: O(n) — single pass.
- **Space**: O(1) — two rolling variables.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Climbing Stairs** — Fibonacci-shaped recurrence. The canonical first DP. | https://leetcode.com/problems/climbing-stairs/ |
| Medium | **House Robber** — the canonical problem above. | https://leetcode.com/problems/house-robber/ |
| Hard | **Decode Ways II** — DP with wildcards; same shape, larger transition logic. | https://leetcode.com/problems/decode-ways-ii/ |
