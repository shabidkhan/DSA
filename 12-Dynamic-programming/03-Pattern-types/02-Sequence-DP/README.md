# Sequence DP

## What is this

Sequence DP solves problems on a *single* sequence where the state tracks a prefix and some local property: `dp[i] = best answer using s[0..i]` plus auxiliary fields. Transitions usually consider one or a small number of last-element decisions.

Examples: house robber, paint house, word break, longest valid parentheses, jump-game min-steps, dice-throw paths. The "next element decision" pattern keeps each transition O(1) or O(k), giving O(n) or O(n*k) total.

## Why we use

- Linear or near-linear DP over a sequence.
- State design is straightforward — `dp[i]` for prefix `s[..i]`.
- Composable with bit-state, modular sums, or running max/min.
- Foundation for many "best path" problems through a sequence.

## How to implement

```
dp[0] = base_case
for i in 1..n-1:
    dp[i] = best over previous-step decisions:
            dp[i] = combine(dp[i-1], s[i], ...)
return dp[n-1]
```

```python
def house_robber(nums):
    if not nums: return 0
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

```python
def word_break(s, words):
    word_set = set(words)
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

```python
def longest_valid_parentheses(s):
    dp = [0] * len(s)
    best = 0
    for i in range(1, len(s)):
        if s[i] == ')':
            if s[i - 1] == '(':
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            elif i - dp[i - 1] - 1 >= 0 and s[i - dp[i - 1] - 1] == '(':
                dp[i] = dp[i - 1] + 2 + (dp[i - dp[i - 1] - 2] if i - dp[i - 1] - 2 >= 0 else 0)
            best = max(best, dp[i])
    return best
```

Almost all "best subsequence ending at i" problems collapse to two rolling variables when the transition only depends on `dp[i-1]` and `dp[i-2]`.

## Which problems this approach solves in the real world

- Stream segmentation: best way to chop a sequence under cost constraints.
- Optimal pricing/profit along a sequence of opportunities.
- Speech / NLP token sequence labelling with HMM/Viterbi (sequence DP).
- Resource budgeting across time periods.
- Sequential decision trees: optimal stopping problems.

## Pros and cons

**Pros**
- O(n) or O(n*k) — fast.
- Rolling-variable trick → O(1) space for many variants.
- Easy to extend with extra state dimensions.

**Cons**
- State design requires identifying the right "last decision".
- Extra dimensions (k items, m colors) bloat memory.
- Reconstruction of choices needs backpointers.

## Limitations

- Cannot model "global" constraints (e.g. exactly K elements chosen) cleanly without extra state.
- Streaming DP needs careful memory management.
- Floating-point accumulation may drift in long sequences.

## One example

**Problem**: Longest Valid Parentheses. Given a string containing just `(` and `)`, find the length of the longest valid (well-formed) parentheses substring.

**Input**: `s = ")()())"`
**Output**: `4`  (substring `()()`)
**Constraints**: `0 <= s.length <= 3 * 10^4`.

## Solution explanation

```python
def longestValidParentheses(s):
    n = len(s)
    dp = [0] * n
    best = 0
    for i in range(1, n):
        if s[i] == ')':
            if s[i - 1] == '(':
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            elif (i - dp[i - 1] - 1) >= 0 and s[i - dp[i - 1] - 1] == '(':
                dp[i] = dp[i - 1] + 2 + (dp[i - dp[i - 1] - 2] if (i - dp[i - 1] - 2) >= 0 else 0)
            best = max(best, dp[i])
    return best
```

Walkthrough on `s = ")()())"`:

| i | s[i] | dp[i-1] | rule applied | dp[i] | best |
|---|------|---------|--------------|-------|------|
| 0 | )    | -       | -            | 0     | 0    |
| 1 | (    | -       | not ')'      | 0     | 0    |
| 2 | )    | 0       | s[1]='(' → dp[i-2]=0+2 | 2 | 2 |
| 3 | (    | -       | not ')'      | 0     | 2    |
| 4 | )    | 0       | s[3]='(' → dp[2]+2 = 4 | 4 | 4 |
| 5 | )    | 4       | s[5-4-1]=s[0]=')' fail | 0 | 4 |

Return 4. Time: O(n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | House Robber (LeetCode 198) | https://leetcode.com/problems/house-robber/ |
| Medium | Word Break (LeetCode 139) | https://leetcode.com/problems/word-break/ |
| Hard | Longest Valid Parentheses (LeetCode 32) | https://leetcode.com/problems/longest-valid-parentheses/ |
