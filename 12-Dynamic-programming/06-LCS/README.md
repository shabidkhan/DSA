# Longest Common Subsequence (LCS)

## What is this

The Longest Common Subsequence problem asks for the length (and optionally the content) of the longest sequence of characters that appears in two input strings in the same relative order but not necessarily contiguously. It is solved by 2D DP where `dp[i][j]` is the LCS length of the prefixes `A[:i]` and `B[:j]`.

The pattern generalises to "find the longest order-preserving alignment between two sequences" and underlies edit distance, diff tools, and biological sequence comparison.

## Why we use

- Captures order-preserving similarity between two sequences without requiring contiguity
- Converts an exponential subsequence search into O(m * n) time
- Same recurrence powers edit distance, shortest common supersequence, and diff
- Allows reconstructing the alignment by walking back through the DP table

## How to implement

```
dp[0][*] = dp[*][0] = 0
for i in 1..m:
    for j in 1..n:
        if A[i-1] == B[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
return dp[m][n]
```

LCS length:

```python
def lcs_length(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

Reconstructing the LCS string by walking back:

```python
def lcs_string(a: str, b: str) -> str:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    i, j, out = m, n, []
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:
            out.append(a[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))
```

Invariant: `dp[i][j]` equals the LCS length of the two prefixes; the recurrence is correct because the last characters either both contribute (match) or at least one of them can be dropped without loss.

## Which problems this approach solves in the real world

- `diff` and version-control tools highlighting common lines between file versions
- DNA / protein alignment in computational biology
- Plagiarism detection comparing two documents
- Speech recognition aligning hypothesized words against a reference transcript
- Spell correction by aligning a misspelled word with dictionary entries

## Pros and cons

**Pros**
- Polynomial O(m * n) for an otherwise exponential search
- Recurrence is simple and easy to memoize or tabulate
- Reconstruction step is straightforward

**Cons**
- O(m * n) memory can be huge for long strings (genomes)
- No knowledge of insertion/deletion costs — for that use edit distance
- Without bit-parallelism, slow for very long strings

## Limitations

- Memory-intensive without Hirschberg's algorithm (O(min(m, n)) memory variant)
- Cannot handle wildcards or fuzzy matches without modification
- Pure LCS does not preserve positional information

## One example

Problem: Given two strings `text1` and `text2`, return the length of their longest common subsequence.

```
Input:  text1 = "AGCAT", text2 = "GAC"
Output: 2   (LCS is "AC" or "GC")
Constraints: 1 <= len(text1), len(text2) <= 1000
```

## Solution explanation

```python
def lcs_length(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

State: `dp[i][j]` = LCS of `a[:i]` and `b[:j]`. When characters match, the LCS extends by one; otherwise the best we can do is the LCS without the last character of either string.

Walkthrough for `a = "AGCAT"`, `b = "GAC"`:

|     |   | G | A | C |
|-----|---|---|---|---|
|     | 0 | 0 | 0 | 0 |
| A   | 0 | 0 | 1 | 1 |
| G   | 0 | 1 | 1 | 1 |
| C   | 0 | 1 | 1 | 2 |
| A   | 0 | 1 | 2 | 2 |
| T   | 0 | 1 | 2 | 2 |

Result `dp[5][3] = 2`. Time O(m * n), space O(m * n) (reducible to O(min(m, n))).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Is Subsequence | https://leetcode.com/problems/is-subsequence/ |
| Medium | Longest Common Subsequence | https://leetcode.com/problems/longest-common-subsequence/ |
| Hard | Shortest Common Supersequence | https://leetcode.com/problems/shortest-common-supersequence/ |
