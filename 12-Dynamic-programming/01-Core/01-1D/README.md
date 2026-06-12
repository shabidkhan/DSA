# 1D dynamic programming

## What is this

1D dynamic programming solves a problem by defining a state that depends on a single index `i` (or a single scalar parameter), then computing answers for all indices in order. Each state `dp[i]` is built from a constant number of previously computed states, usually `dp[i-1]`, `dp[i-2]`, or a small window behind `i`.

The pattern applies when the optimal answer at position `i` can be expressed as a function of optimal answers at positions before `i`. You either tabulate bottom-up (loop from `0` to `n-1`) or memoize top-down with recursion.

## Why we use

- Avoids exponential recomputation by caching subproblem answers
- Turns a recursive blow-up (e.g. naive Fibonacci is O(2^n)) into O(n) time
- Lets you compress space to O(1) when only the last few states matter
- Gives a clean recurrence that is easy to reason about and prove correct

## How to implement

```
1. Define dp[i] = the answer for the prefix/subproblem ending at index i
2. Write the recurrence dp[i] = f(dp[i-1], dp[i-2], ..., a[i])
3. Set base cases dp[0], dp[1]
4. Fill the table from i=0 to i=n-1
5. Return dp[n-1] (or max/min over dp[])
```

Climbing stairs (number of ways to reach step `n` taking 1 or 2 steps at a time):

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
```

House robber (max sum from a list without picking two adjacent values):

```python
def rob(nums: list[int]) -> int:
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

The invariant for `rob`: after processing index `i`, `prev1` holds the best answer including index `i` as the last considered, and `prev2` holds the best answer for the prefix one step behind.

## Which problems this approach solves in the real world

- Counting valid sequences (PIN codes, valid SMS decodings, climbing patterns)
- Maximum profit from non-overlapping intervals (stock trading with cooldown)
- Minimum cost to reach the end of a 1D track (gas stations, jump games)
- DNA mutation cost when only insertions/deletions to a fixed reference are allowed
- Optimal scheduling of single-machine tasks with deadlines and rewards

## Pros and cons

**Pros**
- Linear time, linear (or constant) space
- Simple to code once the recurrence is found
- Easy to prove correctness by induction on `i`

**Cons**
- Requires identifying the right state — wrong state shape gives wrong answers
- Hard to debug when the recurrence is subtly off-by-one
- Does not handle problems where future input affects past decisions

## Limitations

- Cannot model multi-dimensional state (use 2D DP instead)
- Cannot handle constraints across non-contiguous positions in a single dimension
- Online problems where input arrives mid-computation may need different state shape
- Memory-bound when storing extra metadata (e.g. reconstructing the choice path)

## One example

Problem: Given a list of non-negative integers representing house values along a street, return the maximum amount you can rob without robbing two adjacent houses.

```
Input:  nums = [2, 7, 9, 3, 1]
Output: 12   (rob houses 0, 2, 4 -> 2 + 9 + 1 = 12)
Constraints: 1 <= len(nums) <= 100, 0 <= nums[i] <= 400
```

## Solution explanation

```python
def rob(nums: list[int]) -> int:
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

State: `dp[i]` = max money robbed considering houses `0..i`. Recurrence: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` — either skip house `i` (take `dp[i-1]`) or rob it (take `dp[i-2] + nums[i]`). Since only the last two states matter, we keep two variables.

Walkthrough for `nums = [2, 7, 9, 3, 1]`:

| i | nums[i] | prev2 (before) | prev1 (before) | new prev1 = max(prev1, prev2 + nums[i]) |
|---|---------|----------------|----------------|------------------------------------------|
| 0 | 2       | 0              | 0              | max(0, 0+2) = 2                          |
| 1 | 7       | 0              | 2              | max(2, 0+7) = 7                          |
| 2 | 9       | 2              | 7              | max(7, 2+9) = 11                         |
| 3 | 3       | 7              | 11             | max(11, 7+3) = 11                        |
| 4 | 1       | 11             | 11             | max(11, 11+1) = 12                       |

Time O(n), space O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Climbing Stairs | https://leetcode.com/problems/climbing-stairs/ |
| Medium | House Robber II | https://leetcode.com/problems/house-robber-ii/ |
| Hard | Best Time to Buy and Sell Stock IV | https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/ |
