# Decision DP (multiple options per state)

## What is this

A DP family where, at each state, you choose among **a small number of explicit actions** (buy / sell / hold; rob / skip; transition into one of several "modes") and the state's value is the **best** result over those choices. The state typically includes both a position (index, time) **and** a mode (do I currently hold a stock? am I in cooldown? have I used k of n transactions?). Each transition is one of the discrete decisions.

Canonical example: "Best Time to Buy and Sell Stock with Cooldown / k Transactions" — the state must remember whether you're currently holding a stock or in cooldown.

## Why we use

- Cleanly separates "where am I" (position) from "what mode am I in" (state), which is essential for problems that wouldn't yield to a single-dimensional DP.
- Captures problems with explicit business logic — "you can only sell if you hold", "you can only buy if you're free" — without resorting to a search.
- Each decision is local (O(1) options to enumerate) → O(states) time.

## How to implement

```
dp[mode][i] = best value at index i while in mode `mode`
for each (mode, i):
    for each allowed action a:
        next_mode, gain = effect(mode, a, i)
        dp[mode][i] = max(dp[mode][i], dp[next_mode][i ± 1] + gain)
```

Often easier in **rolling form**: maintain a small number of named variables (`hold`, `cash`, `cooldown`) and update them in lockstep per index.

Python — Best Time to Buy and Sell Stock with Cooldown:

```python
def max_profit_cooldown(prices: list[int]) -> int:
    if not prices:
        return 0
    # three modes: holding a stock, in cooldown (just sold), free (can buy)
    hold = -prices[0]
    cooldown = 0
    free = 0
    for p in prices[1:]:
        new_hold = max(hold, free - p)                    # keep holding, or buy from free
        new_cooldown = hold + p                           # sell today
        new_free = max(free, cooldown)                    # stay free, or come out of cooldown
        hold, cooldown, free = new_hold, new_cooldown, new_free
    return max(free, cooldown)
```

Python — Stock with at-most K transactions:

```python
def max_profit_k(k: int, prices: list[int]) -> int:
    n = len(prices)
    if n == 0 or k == 0:
        return 0
    if k >= n // 2:    # unlimited
        return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))
    # dp[j][0] = max profit on day i with j transactions completed, not holding
    # dp[j][1] = max profit on day i with j transactions, holding a stock
    buy  = [-float('inf')] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j]  = max(buy[j], sell[j - 1] - p)         # buy: spend p, start tx j
            sell[j] = max(sell[j], buy[j] + p)             # sell: earn p, finish tx j
    return sell[k]
```

JavaScript — House Robber (two-mode decision DP):

```javascript
function rob(nums) {
  let take = 0, skip = 0;            // take = max if we take previous; skip = max if we didn't
  for (const x of nums) {
    const newTake = skip + x;        // take current: previous must be skipped
    const newSkip = Math.max(take, skip);  // skip current: take best of previous two states
    take = newTake; skip = newSkip;
  }
  return Math.max(take, skip);
}
```

Invariant: at each iteration, each named variable holds the best value achievable ending at the current index in that specific mode. Transitions strictly use values from the previous iteration's variables, preserving the temporal causality of the DP.

## State-machine view

For **Stock with Cooldown**:

```
       buy (-p)              sell (+p)
[free] ─────────────► [hold] ─────────────► [cooldown]
   ▲                                           │
   │                                           │ next day
   └───────────────────────────────────────────┘
```

Three nodes (modes). Each day, we apply one allowed transition per mode. The DP value at each (day, mode) is the best total profit ending at that node.

## Which problems this approach solves in the real world

- **Algorithmic trading**: discrete buy/sell with cooldown, fees, or transaction limits.
- **Battery management**: charge/discharge modes with capacity and cooldown constraints.
- **Telecom packet scheduling**: send / hold / drop decisions per time slot.
- **Insurance claim processing**: claim now vs. wait for accumulated bonus.
- **HR scheduling**: hire / fire / hold with cooldown periods.
- **Game design**: multi-mode character abilities where each mode has different transitions and rewards.

## Pros and cons

**Pros**
- Models real business rules directly — the state machine is the spec.
- Often reducible to O(1) per state with rolling variables, giving O(n) total.
- Each decision is local — easy to reason about correctness mode by mode.
- Extensible: adding a new mode (e.g. "discount cooldown") is a small code change.

**Cons**
- The mode space grows multiplicatively with constraints — "k transactions" needs O(k) modes.
- Updating modes "in lockstep" requires using snapshot values (new vs old) — easy to introduce bugs by mixing them.
- For very large mode sets, the DP table can become huge.

## Limitations

- Only works when modes are discrete and few. Continuous decisions need different tools.
- Order of updates matters when a mode self-references (e.g. "stay free" depends on previous free). Compute new values from old values, not mid-update.
- Doesn't model adversarial opponents (use minimax instead).

## One example

**Problem**: Given an array `prices` where `prices[i]` is the price of a stock on day `i`, find the **maximum profit** you can achieve. You may make as many transactions as you want, but after you sell, you have a **one-day cooldown** during which you cannot buy.
Constraints: `1 ≤ n ≤ 5000`, `0 ≤ prices[i] ≤ 1000`.

**Input**: `prices = [1, 2, 3, 0, 2]`
**Output**: `3` — transactions: buy at 1, sell at 2 (profit 1), cooldown day, buy at 0, sell at 2 (profit 2). Total = 3.

## Solution explanation

Three modes per day: `hold`, `cooldown`, `free`. Transitions:

| from \ action | buy            | sell            | wait (do nothing)              |
|---------------|----------------|------------------|--------------------------------|
| free          | → hold (−p)    | (illegal)        | → free                         |
| hold          | (illegal)      | → cooldown (+p) | → hold                         |
| cooldown      | (illegal)      | (illegal)        | → free (next day)              |

```python
def max_profit_cooldown(prices: list[int]) -> int:
    if not prices:
        return 0
    hold = -prices[0]
    cooldown = 0
    free = 0
    for p in prices[1:]:
        new_hold = max(hold, free - p)
        new_cooldown = hold + p
        new_free = max(free, cooldown)
        hold, cooldown, free = new_hold, new_cooldown, new_free
    return max(free, cooldown)
```

Walk-through on `[1, 2, 3, 0, 2]`:

| day | p | hold (in) | cooldown (in) | free (in) | new_hold | new_cooldown | new_free | hold (out) | cooldown (out) | free (out) |
|-----|---|-----------|----------------|------------|----------|---------------|-----------|------------|------------------|-------------|
| 0   | 1 | —         | —              | —          | —        | —             | —         | -1         | 0                | 0           |
| 1   | 2 | -1        | 0              | 0          | max(-1, 0-2)=-1 | -1+2 = 1   | max(0, 0)=0 | -1         | 1                | 0           |
| 2   | 3 | -1        | 1              | 0          | max(-1, 0-3)=-1 | -1+3 = 2   | max(0, 1)=1 | -1         | 2                | 1           |
| 3   | 0 | -1        | 2              | 1          | max(-1, 1-0)=1  | -1+0 = -1  | max(1, 2)=2 | 1          | -1               | 2           |
| 4   | 2 | 1         | -1             | 2          | max(1, 2-2)=1   | 1+2 = 3    | max(2, -1)=2| 1          | 3                | 2           |

Final `max(free, cooldown) = max(2, 3) = 3`.

Correctness: every transition only consults the previous day's mode values (`hold`, `cooldown`, `free`), so causality is preserved. Each mode's update represents the **maximum** profit ending in that mode on the new day. Taking `max(free, cooldown)` at the end captures both "comfortably done trading" and "just sold today" terminal states.

- **Time**: O(n) — one pass.
- **Space**: O(1) — three rolling variables.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Best Time to Buy and Sell Stock** — single transaction; one-shot decision DP. | https://leetcode.com/problems/best-time-to-buy-and-sell-stock/ |
| Medium | **Best Time to Buy and Sell Stock with Cooldown** — the canonical problem above. | https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/ |
| Hard | **Best Time to Buy and Sell Stock IV** — at most K transactions; 2D decision DP `dp[k][i]`. | https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/ |
