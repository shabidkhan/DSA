# Memoization (top-down DP)

## What is this

Memoization is **top-down DP**: write the natural recursion that mirrors the problem's recurrence, then **cache** the result of each call by its arguments. Future calls with the same arguments return the cached value instantly. The structure is identical to plain recursion; the only addition is a memo dictionary (or `lru_cache` decorator in Python) keyed by the call's arguments.

It is the lazy, demand-driven counterpart of **tabulation** (bottom-up DP), which fills a table in dependency order whether each cell is needed or not.

## Why we use

- Lets you write the **recurrence** directly — often closer to the problem statement than a tabulation loop.
- Caches each unique subproblem **once**, turning exponential recursion (Fibonacci, knapsack) into polynomial time.
- Computes only the subproblems actually reachable from the original call — saves work on sparse DPs.
- Easy to add to existing recursive code: drop in `@lru_cache(None)` or a manual `dict`.

## How to implement

```
memo = {}
def f(*args):
    if args in memo: return memo[args]
    if base case: return base value
    result = combine(recursive calls...)
    memo[args] = result
    return result
return f(initial_args)
```

Python — Fibonacci with `lru_cache`:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Python — Coin Change (min coins for amount):

```python
from functools import lru_cache

def coin_change(coins: list[int], amount: int) -> int:
    @lru_cache(maxsize=None)
    def dp(rem: int) -> int:
        if rem == 0:
            return 0
        if rem < 0:
            return float('inf')
        return min((dp(rem - c) + 1 for c in coins), default=float('inf'))
    ans = dp(amount)
    return ans if ans != float('inf') else -1
```

JavaScript — Climbing Stairs with manual memo:

```javascript
function climbStairs(n) {
  const memo = new Map();
  function f(i) {
    if (i <= 2) return i;
    if (memo.has(i)) return memo.get(i);
    const v = f(i - 1) + f(i - 2);
    memo.set(i, v);
    return v;
  }
  return f(n);
}
```

Invariant: every memo entry `memo[args]` stores the **final** result of `f(args)` — once written, it is never updated. The first call with a given argument pays full cost; subsequent calls are O(1).

## Memoization vs Tabulation

| Aspect                       | Memoization (top-down)                          | Tabulation (bottom-up)                  |
|------------------------------|-------------------------------------------------|------------------------------------------|
| Style                        | Recursive + cache                               | Iterative loop                           |
| Order                        | On demand (driven by what's called)             | Predetermined fill order                 |
| Reaches sparse subproblems   | Only those actually needed                      | All subproblems in the table             |
| Stack risk                   | Recursion depth ≤ longest dep chain             | None                                     |
| Easier to write              | Often, since it mirrors the recurrence          | Sometimes; loops can be subtle           |
| Easier to space-optimise     | Less so                                         | Easier — rolling rows / arrays           |
| Easier to parallelise        | Harder                                          | Easier (layer-by-layer)                  |
| Use when                     | Recurrence is natural, dependency graph sparse  | All subproblems will be needed; speed-critical |

## Same recurrence, two forms

Coin Change top-down:

```python
@lru_cache(maxsize=None)
def dp(rem):
    if rem == 0: return 0
    if rem < 0:  return float('inf')
    return min(dp(rem - c) + 1 for c in coins)
```

Coin Change bottom-up:

```python
dp = [float('inf')] * (amount + 1)
dp[0] = 0
for r in range(1, amount + 1):
    for c in coins:
        if r - c >= 0:
            dp[r] = min(dp[r], dp[r - c] + 1)
```

Both compute the same table values; the tabulation version always fills indices `0..amount`, even if some are unreachable.

## Which problems this approach solves in the real world

- **Compiler / interpreter caches**: same expression in the same scope evaluated once.
- **Game AI search**: cache minimax values of board positions.
- **Path-cost dynamic programming** on irregular graphs where only some nodes matter.
- **Recursive parsers**: cache results of parsing a substring against a non-terminal.
- **Symbolic differentiation**: cache derivatives of subexpressions.
- **Web request handlers**: cache expensive responses keyed by query parameters.

## Pros and cons

**Pros**
- Code structure matches the recurrence — clearer for problem write-ups.
- Sparse computation — only subproblems on the dependency path are touched.
- Trivial to add to existing recursive code.
- Easy to extend with multiple arguments (just `@lru_cache` more dimensions).

**Cons**
- Recursion stack depth bounded by longest dep chain — risky for big inputs.
- Function call overhead is non-trivial in interpreted languages.
- Cache eviction policy (e.g. `maxsize`) can quietly evict needed entries.
- Hard to apply rolling-array space optimisation.

## Limitations

- Doesn't help if every subproblem is needed and recurrence is straightforward — tabulation wins on raw speed.
- Requires args to be **hashable** — list / dict / set args break it. Use tuples.
- For very large state spaces, the cache itself may blow memory.
- Concurrency: must guard the cache if calls happen from multiple threads.

## One example

**Problem**: You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the **fewest number of coins** that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`. You may assume that you have an **infinite number of each kind of coin**.
Constraints: `1 ≤ coins.length ≤ 12`, `1 ≤ coins[i] ≤ 2^31 − 1`, `0 ≤ amount ≤ 10^4`.

**Input**: `coins = [1, 2, 5]`, `amount = 11`
**Output**: `3` — `11 = 5 + 5 + 1`.

## Solution explanation

```python
from functools import lru_cache

def coin_change(coins: list[int], amount: int) -> int:
    @lru_cache(maxsize=None)
    def dp(rem: int) -> int:
        if rem == 0:
            return 0
        if rem < 0:
            return float('inf')
        best = float('inf')
        for c in coins:
            best = min(best, dp(rem - c) + 1)
        return best
    ans = dp(amount)
    return ans if ans != float('inf') else -1
```

Walk-through (showing memo population for `amount = 11`):

| call (rem) | first time? | tries coin                  | recursive results            | result | memo[rem]      |
|------------|-------------|------------------------------|-------------------------------|--------|----------------|
| dp(0)      | yes         | —                            | base                          | 0      | 0              |
| dp(1)      | yes         | 1                            | dp(0)+1 = 1                   | 1      | 1              |
| dp(2)      | yes         | 1→dp(1)+1=2, 2→dp(0)+1=1     | min(2, 1)                     | 1      | 1              |
| dp(3)      | yes         | 1→dp(2)+1=2, 2→dp(1)+1=2     | min(2, 2)                     | 2      | 2              |
| dp(4)      | yes         | 1→dp(3)+1=3, 2→dp(2)+1=2     | min(3, 2)                     | 2      | 2              |
| dp(5)      | yes         | 1→dp(4)+1=3, 2→dp(3)+1=3, 5→dp(0)+1=1 | min(3, 3, 1)        | 1      | 1              |
| ...        | ...         | ...                          | ...                           | ...    | ...            |
| dp(11)     | yes         | 1→dp(10)+1, 2→dp(9)+1, 5→dp(6)+1 | min(...)                | 3      | 3              |

Each `rem` is computed exactly once. Repeated calls to the same `rem` hit the cache.

Correctness: the recurrence "min coins for `rem` = 1 + min over coins of (coins for `rem - c`)" captures every decomposition. Memoisation guarantees each `rem` is solved once, turning the otherwise-exponential recursion into linear-in-amount time.

- **Time**: O(amount · |coins|) — each `rem` from 0 to `amount` is computed once, doing O(|coins|) work.
- **Space**: O(amount) memo + recursion stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Fibonacci Number** — the simplest memoisation drill. | https://leetcode.com/problems/fibonacci-number/ |
| Medium | **Coin Change** — the canonical problem above. | https://leetcode.com/problems/coin-change/ |
| Hard | **Longest Increasing Path in a Matrix** — DFS with memoisation on (i, j); the cache is essential to avoid re-exploring shared sub-paths. | https://leetcode.com/problems/longest-increasing-path-in-a-matrix/ |
