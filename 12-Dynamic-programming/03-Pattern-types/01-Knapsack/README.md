# Knapsack DP

## What is this

Knapsack DP solves "pick a subset of items under a capacity constraint to maximize value (or count ways)". The state is `dp[i][w]` = best value using the first `i` items with remaining capacity `w`. Variants include 0/1 knapsack (each item used at most once), unbounded knapsack (each item used any number of times), and bounded knapsack (each item has a per-item limit).

The pattern fits any problem reducible to "choose a subset whose total `weight` is at most `W` and total `value` is maximum", or equivalent counting/feasibility versions like subset-sum and coin change.

## Why we use

- Reduces an exponential subset search to O(n * W)
- Same skeleton handles maximize-value, count-ways, and feasibility problems
- Provides a clean way to enforce a single resource constraint (capacity, budget, time)
- Easy to compress 2D table to 1D by iterating capacity in reverse (0/1) or forward (unbounded)

## How to implement

```
0/1 Knapsack (each item at most once):
  for i in 1..n:
      for w in 0..W:
          dp[i][w] = dp[i-1][w]
          if w >= wt[i]:
              dp[i][w] = max(dp[i][w], dp[i-1][w - wt[i]] + val[i])

Unbounded (each item any number of times):
  for i in 1..n:
      for w in 0..W:
          dp[i][w] = dp[i-1][w]
          if w >= wt[i]:
              dp[i][w] = max(dp[i][w], dp[i][w - wt[i]] + val[i])
```

0/1 knapsack with O(W) space (capacity loops in reverse so each item is used at most once):

```python
def knapsack_01(weights: list[int], values: list[int], W: int) -> int:
    dp = [0] * (W + 1)
    for wt, val in zip(weights, values):
        for w in range(W, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[W]
```

Unbounded knapsack (forward loop allows reusing an item):

```python
def knapsack_unbounded(weights: list[int], values: list[int], W: int) -> int:
    dp = [0] * (W + 1)
    for wt, val in zip(weights, values):
        for w in range(wt, W + 1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[W]
```

Invariant for 0/1: when processing item `i`, `dp[w]` still reflects "best value using items `0..i-1`" before being overwritten, because the inner loop runs from large `w` down to `wt[i]`.

## Which problems this approach solves in the real world

- Cargo loading: pack items in a truck to maximize value within weight limit
- Budget allocation: pick projects within a fixed budget to maximize ROI
- Cutting stock: cut a long rod into pieces with given prices to maximize revenue
- Investment portfolio with discrete share lots and a cash limit
- Resource scheduling: pick jobs whose total CPU time fits a deadline

## Pros and cons

**Pros**
- Pseudo-polynomial O(n * W) is fast when `W` is moderate
- Same code structure handles many variants
- 1D space compression is straightforward

**Cons**
- Time scales with the numeric value of capacity, not its bit length — NP-hard in input size
- Cannot directly handle multiple independent constraints (becomes 3D, 4D, ...)
- Reconstructing the chosen item set requires storing backpointers

## Limitations

- Infeasible when capacity is huge (e.g. 10^9) — needs FPTAS or branch-and-bound
- Multiple resource constraints multiply the table size exponentially
- Fractional knapsack (items divisible) is solved by greedy, not DP

## One example

Problem: Given `weights = [1, 3, 4, 5]`, `values = [1, 4, 5, 7]`, and capacity `W = 7`, find the maximum value of items you can fit (each item used at most once).

```
Input:  weights = [1, 3, 4, 5], values = [1, 4, 5, 7], W = 7
Output: 9    (pick items 1 and 3: weight 3 + 4 = 7, value 4 + 5 = 9)
Constraints: 1 <= n <= 100, 1 <= W <= 10^4, 1 <= weights[i], values[i] <= 100
```

## Solution explanation

```python
def knapsack_01(weights: list[int], values: list[int], W: int) -> int:
    dp = [0] * (W + 1)
    for wt, val in zip(weights, values):
        for w in range(W, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[W]
```

State: `dp[w]` = best value achievable with capacity exactly `w` using items considered so far. Reverse iteration over `w` guarantees that `dp[w - wt]` still represents "without the current item", enforcing the 0/1 rule.

Walkthrough for `weights = [1, 3, 4, 5]`, `values = [1, 4, 5, 7]`, `W = 7`:

| Item processed | dp[0..7]                       |
|----------------|--------------------------------|
| (initial)      | 0 0 0 0 0 0 0 0                |
| (1, 1)         | 0 1 1 1 1 1 1 1                |
| (3, 4)         | 0 1 1 4 5 5 5 5                |
| (4, 5)         | 0 1 1 4 5 6 6 9                |
| (5, 7)         | 0 1 1 4 5 7 8 9                |

Final `dp[7] = 9`. Time O(n * W), space O(W).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Coin Change II | https://leetcode.com/problems/coin-change-ii/ |
| Medium | Partition Equal Subset Sum | https://leetcode.com/problems/partition-equal-subset-sum/ |
| Hard | Target Sum (count assignments) | https://leetcode.com/problems/target-sum/ |
