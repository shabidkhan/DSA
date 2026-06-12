# DP Transition Type

## Folder structure

```
02-Transition-type/
├── README.md
├── 01-Linear-DP/README.md
├── 02-Grid-DP/README.md
└── 03-Decision-DP/README.md
```

## What is this

Once you have the state, the *transition* describes how f(state) is computed from smaller states. Grouping DP problems by transition shape is more useful than grouping them by topic, because the shape of the transition determines the loop order, the space-optimisation, and the off-by-one risks. Three shapes dominate: linear (f[i] depends on a constant number of preceding indices), grid (f[i][j] depends on its neighbours in a 2D table), and decision (f[i][mode] where `mode` enumerates a small set of choices at each step).

These three shapes cover most non-advanced DP problems. The folder is organised by the transition shape because once you recognise the shape, the implementation pattern is almost mechanical — only the recurrence formula changes.

## Why we use

- Recognising the transition shape early collapses the design space.
- Linear DPs space-optimise to O(1) — keep a constant number of previous values.
- Grid DPs admit a single rolling row, cutting memory from O(rows·cols) to O(cols).
- Decision DPs cleanly model state machines and stock-trading-style problems.

## How to implement

```text
# Linear: f[i] = g(f[i-1], f[i-2], input[i])
function linear(n):
    a, b = base0, base1
    for i in 2..n:
        a, b = b, g(b, a, input[i])
    return b

# Grid: f[i][j] = g(f[i-1][j], f[i][j-1], f[i-1][j-1], inputs)
function grid(rows, cols):
    row = [base for _ in cols]
    for i in 1..rows:
        for j in 1..cols:
            row[j] = g(row[j], row[j-1], prev_diag, inputs)
    return row[cols-1]

# Decision: f[i][mode] for mode in modes
function decision(n, modes):
    dp = {m: baseValue(m) for m in modes}
    for i in 1..n:
        new = {}
        for m in modes:
            new[m] = max over m' of (dp[m'] + transitionGain(m', m, input[i]))
        dp = new
    return max(dp.values())
```

Subpatterns in this folder:

- `01-Linear-DP/` — single index, constant lookback. Examples: house robber, climbing stairs.
- `02-Grid-DP/` — two indices, neighbour lookback. Examples: min path sum, unique paths.
- `03-Decision-DP/` — state index × mode enum. Examples: stock with cooldown, paint-house.

## Which problems this approach solves in the real world

- Sequence-based decision systems (today's value depends on past few steps).
- 2D grid pathfinding for cost minimisation in logistics or robotics.
- Stock-trading strategies with hold/buy/sell modes and cooldowns.
- Game AI evaluating state-machine transitions over a horizon.
- Routing on tiled maps with directional cost differences.
- Resource consumption planning where state = (time, current mode).

## Pros and cons

**Pros**
- Each transition shape has a known space-optimisation trick.
- Code reuses the same loop structure across problems in a shape.
- Off-by-one bugs are easier to catch because the recurrence is local.
- Decision DP cleanly separates "what state you're in" from "what input you're processing."

**Cons**
- Linear DPs with non-constant lookback (e.g., f[i] depends on f[i-k] for varying k) blow up to O(n²).
- Grid DPs miss diagonal moves unless explicitly modelled — easy to forget.
- Decision DPs explode in state count if `modes` is large.
- Misclassifying a transition shape leads to wrong space-optimisation and broken code.

## Limitations

- These shapes assume *fixed* state dimensionality — variable-size states need interval or partition DP.
- Linear/grid optimisations break if you need full history for traceback.
- Decision DPs need careful tie-breaking when multiple modes give the same value.
- Real-world cost functions may not be Markovian; DP requires they be.
