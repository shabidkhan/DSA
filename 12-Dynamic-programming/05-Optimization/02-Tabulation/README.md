# Tabulation (bottom-up DP)

## What is this

Tabulation is **bottom-up DP**: fill a table iteratively from base cases up to the final answer, in an order that respects the dependency graph. There is no recursion — just nested loops that compute `dp[i]` (or `dp[i][j]`, etc.) by combining values that were filled earlier in the same loop. The structure is the same as memoization (same recurrence), but the control flow is explicit and the function stack is replaced by an array.

The order matters: each cell's dependencies must already be filled when we compute it.

## Why we use

- Avoids recursion overhead and stack risk — pure loops.
- **Predictable memory access** → faster constant factor than memoization in practice.
- Enables **space optimisation**: rolling arrays, single-variable updates, in-place fills.
- Easier to parallelise per "layer" (e.g. fill row `i` in parallel once row `i-1` is done).

## How to implement

```
dp = array (or 2D table) sized by the state space
fill base cases (dp[0], dp[0][?], etc.)
for i in dependency order:
    dp[i] = combine(dp[smaller indices], local cost)
return dp[final state]
```

Python — Fibonacci tabulation (O(n) time, O(1) space):

```python
def fib(n: int) -> int:
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```

Python — Coin Change (bottom-up, min coins):

```python
def coin_change(coins: list[int], amount: int) -> int:
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for r in range(1, amount + 1):
        for c in coins:
            if r - c >= 0:
                dp[r] = min(dp[r], dp[r - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
```

JavaScript — Longest Common Subsequence (2D tabulation):

```javascript
function lcs(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (a[i - 1] === b[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
      else dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
    }
  }
  return dp[m][n];
}
```

Invariant: at the moment we compute `dp[i]` (or `dp[i][j]`), every cell on which `dp[i]` depends is already finalised — guaranteed by the loop order.

## Tabulation vs Memoization (recap)

| Question                                | Pick tabulation                    | Pick memoization                  |
|------------------------------------------|-------------------------------------|------------------------------------|
| Will every subproblem be needed?         | yes                                 | no — only a subset                |
| Is the dependency order obvious?         | yes (e.g. left-to-right)            | not really                         |
| Will the input cause deep recursion?     | doesn't matter                      | risk of stack overflow             |
| Do I need to space-optimise the table?   | yes — rolling arrays trivially      | harder                             |
| Is the recurrence easier to write down recursively? | tabulation harder            | memoisation easier                 |
| Will I parallelise / vectorise?          | yes                                 | hard                               |

## Space optimisation example — rolling row

LCS table only needs the previous row to compute the current row:

```python
def lcs_space_optimised(a: str, b: str) -> int:
    m, n = len(a), len(b)
    if m < n:
        a, b = b, a; m, n = n, m
    prev = [0] * (n + 1)
    cur = [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev, cur = cur, prev
        for j in range(n + 1):
            cur[j] = 0
    return prev[n]
```

This drops space from O(m·n) to O(min(m, n)).

## Which problems this approach solves in the real world

- **Production-grade DP**: when you need maximum speed and predictable memory.
- **Embedded / mobile**: stack-safe, deterministic.
- **GPU / vector code**: bottom-up iteration maps well onto SIMD lanes.
- **Streaming systems**: rolling-window DP where only the last K states matter.
- **Database query optimisers**: bottom-up dynamic programming over join orders.
- **Bioinformatics**: large pairwise alignment matrices.

## Pros and cons

**Pros**
- No recursion overhead.
- Trivially space-optimisable via rolling buffers.
- Cache-friendly memory access patterns.
- Easy to parallelise per layer.

**Cons**
- The loop order may be non-obvious for complex DPs (e.g. interval DP requires "by length").
- Forces every subproblem to be filled, even unreachable ones.
- Less readable than memoization when the recurrence is recursive in nature (e.g. tree DP).

## Limitations

- Doesn't apply when state space is **sparse** — much work wasted on cells that wouldn't be visited.
- Some recurrences (tree DP, DP on irregular graphs) have no natural iterative order; memoization fits better.
- Hard to refactor when the recurrence changes — you must re-derive the loop ordering.

## One example

**Problem**: Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be **segmented** into a space-separated sequence of one or more dictionary words. The same word in the dictionary may be reused multiple times.
Constraints: `1 ≤ s.length ≤ 300`, `1 ≤ wordDict.length ≤ 1000`, `1 ≤ wordDict[i].length ≤ 20`.

**Input**: `s = "leetcode"`, `wordDict = ["leet", "code"]`
**Output**: `true` — `"leet" + "code"`.

## Solution explanation

State: `dp[i]` = true iff `s[0..i-1]` (length-`i` prefix) is segmentable.

Recurrence: `dp[i] = OR over j in 0..i-1 of (dp[j] AND s[j..i] is in wordDict)`.

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]
```

Walk-through on `s = "leetcode"`, `wordDict = {"leet", "code"}`:

| i | considered j and s[j:i]            | dp[i] | reasoning                                            |
|---|--------------------------------------|-------|--------------------------------------------------------|
| 0 | base                                 | T     | empty prefix is segmentable                            |
| 1 | j=0 → "l"                            | F     | "l" not in dict                                        |
| 2 | j=0 → "le"; j=1 dp[1]=F → skip       | F     | none works                                             |
| 3 | "lee", j=1,2 dp=F                    | F     | none works                                             |
| 4 | "leet" (j=0) ∧ dp[0]=T → **true**    | T     | match found                                            |
| 5 | "leetc" (j=0) no; j=4: dp[4]=T but "c" not in dict | F | nothing matches |
| 6 | dp[4]=T, "co" no; others F           | F     | "co" not in dict                                       |
| 7 | dp[4]=T, "cod" no                    | F     |                                                        |
| 8 | dp[4]=T, "code" in dict → **true**   | T     | matches `"leet"` then `"code"`                          |

Final `dp[8] = true`.

Correctness: by induction on `i`. `dp[0] = True` (the empty prefix is trivially segmentable). For `i > 0`, the segmentation must end with some word `s[j..i-1]`; if such a `j` exists with `dp[j] = true` and `s[j..i-1]` in the dictionary, then `dp[i] = true`. Otherwise `dp[i] = false`.

- **Time**: O(n² · L) where L is the max word length (substring slicing). Reducible to O(n²) with sets of fixed lengths.
- **Space**: O(n) for the `dp` array.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Fibonacci Number** — basic linear tabulation; the canonical first DP. | https://leetcode.com/problems/fibonacci-number/ |
| Medium | **Word Break** — the canonical 1D tabulation problem above. | https://leetcode.com/problems/word-break/ |
| Hard | **Edit Distance** — 2D tabulation over string prefix lengths. Practice the rolling-row optimisation. | https://leetcode.com/problems/edit-distance/ |
