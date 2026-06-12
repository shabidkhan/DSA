# DP Optimization

## Folder structure

```
05-Optimization/
├── README.md
├── 01-Memoization/README.md
└── 02-Tabulation/README.md
```

## What is this

Memoization and tabulation are the two implementation styles of dynamic programming. They compute the same DP table — they differ in *direction*. Memoization is top-down: write the recursive definition naturally and cache results in a hash map or array, computing states lazily as the recursion reaches them. Tabulation is bottom-up: iterate over the state space in dependency order and fill the table directly.

Top-down is easier to discover because it mirrors the recurrence. Bottom-up is easier to space-optimise (rolling arrays) because the iteration order is explicit. Real codebases pick based on language idioms and constraints: Python with `@lru_cache` makes memoization frictionless; C++ with tight memory budgets makes tabulation the default.

## Why we use

- Memoization lets you write the recurrence in its natural form — minimal mental gymnastics.
- Tabulation makes iteration order explicit, enabling rolling-array space optimisation.
- Both compute every reachable state exactly once — same asymptotic time.
- Switching between them is a useful refactor when memory or stack depth becomes a problem.

## How to implement

```text
# Memoization (top-down)
memo = {}
function f(state):
    if isBase(state): return baseValue(state)
    if state in memo: return memo[state]
    result = combine(f(sub1(state)), f(sub2(state)), ...)
    memo[state] = result
    return result
return f(initialState)

# Tabulation (bottom-up)
function fTable(N):
    table = sized array; fill base cases
    for state in topologicalOrderOfStates:
        table[state] = combine(table[sub1(state)], table[sub2(state)], ...)
    return table[finalState]
```

The "topological order of states" in tabulation is the order in which dependencies are filled before reads — usually a nested for-loop sweep. Memoization figures this out implicitly via recursion.

Subpatterns in this folder:

- `01-Memoization/` — recursive top-down with `@lru_cache` or hand-rolled hash maps.
- `02-Tabulation/` — iterative bottom-up with array/matrix and explicit loop order.

## Which problems this approach solves in the real world

- Long-running services that cache expensive recursive computations (build systems, evaluators).
- Memory-bounded embedded code that must fit DP in a fixed array.
- Memoisation for cleaner test fixtures (declarative state → answer mapping).
- Bottom-up DP in compiled kernels where loop order matters for cache locality.
- Streaming compute where partial DP tables are reused across requests.
- Educational settings where the natural recursive definition needs to be preserved.

## Pros and cons

**Pros**
- Memoization keeps the recursive definition pristine — easier to verify against the math.
- Tabulation enables rolling-array space cuts and explicit cache-friendly loop order.
- Memoization computes only *reachable* states — avoids wasted work on sparse problems.
- Tabulation runs without recursion — no stack-overflow risk.

**Cons**
- Memoization adds hash-map overhead and risks `RecursionError` on deep recursions.
- Tabulation requires figuring out a valid iteration order — easy to get wrong on multi-dimensional states.
- Memoization with mutable state (lists, dicts) needs careful hashing.
- Tabulation with rolling arrays loses traceback information — solution reconstruction needs extra storage.

## Limitations

- Memoization can't trivially space-optimise to O(1) — the cache holds everything.
- Tabulation requires the state space to be enumerable in some order; sparse spaces waste loops.
- Tabulation in languages without dense N-dimensional arrays is awkward (Python lists of lists, etc.).
- Both struggle when states are continuous; you must discretize.
