# Advanced DP

## Folder structure

```
04-Advanced/
├── README.md
├── 01-Bitmask/README.md
├── 02-Digit-DP/README.md
└── 03-DP-on-trees/README.md
```

## What is this

Advanced DP covers state shapes that don't fit the linear / grid / decision moulds. Bitmask DP uses a bitmask to encode subsets of a small universe (n ≤ 20 typically), making "what subset has been used so far" a single integer state. Digit DP enumerates numbers by digit position with constraints on tight-bound, leading-zero, and per-digit sums. DP on trees runs a postorder traversal where each node aggregates DP results from its children — turning trees into recursive DP tables.

The unifying property is *exotic state* — the state isn't a simple index or pair of indices, but something structural: a subset, a digit-position-with-flags, or a subtree. Once the state is named correctly, the transition often becomes straightforward.

## Why we use

- Bitmask DP solves NP-looking problems (TSP, assignment) in O(2ⁿ · n) — fast for n ≤ 20.
- Digit DP answers "how many numbers in [L, R] satisfy property P" in O(digits · states) — impossible by brute force.
- Tree DP handles per-subtree aggregations where the answer "rolls up" through the parent.
- Each pattern exposes a hidden Markovian structure that polynomial-time DPs of the basic kind miss.

## How to implement

```text
# Bitmask DP — state = mask of used elements (and optionally last picked)
function bitmaskDP(n):
    f = array of size 1<<n filled with inf
    f[0] = 0
    for mask in 0..(1<<n)-1:
        for i in 0..n-1:
            if mask & (1<<i): continue
            f[mask | (1<<i)] = min(f[mask | (1<<i)], f[mask] + cost(mask, i))
    return f[(1<<n) - 1]

# Digit DP — count numbers ≤ N with property P
function digitDP(digits, pos, tight, leadingZero, otherState):
    if pos == len(digits): return 1 if accept(otherState) else 0
    if memoised: return memo[pos][tight][leadingZero][otherState]
    high = digits[pos] if tight else 9
    total = 0
    for d in 0..high:
        total += digitDP(digits, pos+1, tight and d==high, leadingZero and d==0, update(otherState, d))
    memo[pos][tight][leadingZero][otherState] = total
    return total

# DP on tree — post-order subtree aggregation
function dfs(node, parent):
    state = baseState(node)
    for child in adj[node]:
        if child == parent: continue
        childState = dfs(child, node)
        state = combine(state, childState, edge(node, child))
    return state
```

Subpatterns in this folder:

- `01-Bitmask/` — subset-as-integer state for small universes (assignment, TSP, set cover).
- `02-Digit-DP/` — position-by-position digit enumeration with tight/leading-zero flags.
- `03-DP-on-trees/` — postorder subtree DPs (max independent set on tree, rerooting).

## Which problems this approach solves in the real world

- Vehicle routing for small fleets (bitmask TSP).
- Task assignment to workers under cost matrix (bitmask assignment).
- Counting valid IDs / phone numbers / serials within a range under digit rules (digit DP).
- Subtree-rollup aggregations in org charts (tree DP).
- Optimal placement of relay stations on a tree network (tree DP).
- Set-cover approximations within an exponential cap (bitmask).

## Pros and cons

**Pros**
- Tackles problems that are otherwise NP or unbounded.
- Bitmask DP is short to write once the state is named.
- Digit DP handles ranges up to 10¹⁸ that brute force can't approach.
- Tree DP composes recursively — easy to reason about.

**Cons**
- Bitmask DP is exponential in n; doesn't scale past ~20.
- Digit DP's state space explodes with extra carried information (mod, parity, sum).
- Tree DP that needs "best for all subtrees if X is the root" requires the rerooting trick, which is fiddly.
- Memoisation tables are large; memory becomes the bottleneck before time.

## Limitations

- Bitmask DP is only practical for tiny universes — won't help on n = 100.
- Digit DP assumes the property factors through digit-by-digit construction.
- Tree DP needs the input to actually be a tree — cycles break the postorder.
- These patterns trade one hard problem (the original) for another (designing the right state), which is genuinely creative work.
