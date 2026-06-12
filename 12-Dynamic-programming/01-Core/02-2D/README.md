# 2D dynamic programming

## What is this

2D dynamic programming uses a state indexed by two parameters `(i, j)`, typically representing positions in two sequences, a row and column on a grid, or an index plus an extra dimension like remaining capacity. The answer at `(i, j)` is built from a constant number of previously computed neighbours such as `(i-1, j)`, `(i, j-1)`, or `(i-1, j-1)`.

The pattern fits problems where the decision at one cell depends on choices made in two independent axes — for example, comparing two strings character by character or walking a grid with movement constraints.

## Why we use

- Captures correlated state across two axes that 1D DP cannot model
- Reduces exponential search over two sequences/dimensions to polynomial time
- Provides a natural shape for grid traversal, sequence alignment, and interval problems
- Easy to compress to O(min(m, n)) space when only the previous row matters

## How to implement

```
1. Define dp[i][j] = answer for the subproblem defined by indices i and j
2. Write the recurrence dp[i][j] = f(dp[i-1][j], dp[i][j-1], dp[i-1][j-1], ...)
3. Set base cases for dp[0][*] and dp[*][0]
4. Fill the table row by row (or column by column)
5. Return dp[m][n] (or whichever cell holds the final answer)
```

Unique paths on an `m x n` grid moving only right or down:

```python
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]
```

Minimum path sum on a weighted grid:

```python
def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    return dp[m-1][n-1]
```

Invariant: each `dp[i][j]` is final once all cells above and to the left are finalized, so row-major traversal is safe.

## Which problems this approach solves in the real world

- Sequence alignment in bioinformatics (DNA, protein comparison)
- Spell-checkers and fuzzy search using edit distance
- Image seam carving (content-aware resizing using min-cost grid path)
- Robot navigation on a known grid with weighted cells
- Pricing/discount tables where rows are time periods and columns are inventory levels

## Pros and cons

**Pros**
- Solves problems unreachable by 1D DP
- Recurrence is usually a clean combination of 2-4 neighbours
- Often compressible to O(min(m, n)) space using rolling rows

**Cons**
- O(m * n) memory can be large for big inputs
- Filling order matters — wrong order yields wrong results
- Reconstructing the actual solution path requires extra bookkeeping

## Limitations

- State explosion when more than two dimensions are required
- Not suitable when transitions depend on far-away cells (e.g. arbitrary jumps)
- Pure tabulation wastes time on unreachable states for sparse problems

## One example

Problem: Given two strings `text1` and `text2`, return the length of their longest common subsequence.

```
Input:  text1 = "abcde", text2 = "ace"
Output: 3   (LCS is "ace")
Constraints: 1 <= len(text1), len(text2) <= 1000
```

## Solution explanation

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

State: `dp[i][j]` = length of LCS of `text1[:i]` and `text2[:j]`. If the last characters match, extend the LCS of the shorter prefixes by one; otherwise drop one character from either string and take the max.

Walkthrough for `text1 = "abcde"`, `text2 = "ace"` (only the relevant cells shown):

|     |   | a | c | e |
|-----|---|---|---|---|
|     | 0 | 0 | 0 | 0 |
| a   | 0 | 1 | 1 | 1 |
| b   | 0 | 1 | 1 | 1 |
| c   | 0 | 1 | 2 | 2 |
| d   | 0 | 1 | 2 | 2 |
| e   | 0 | 1 | 2 | 3 |

Time O(m * n), space O(m * n) (compressible to O(n)).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Unique Paths | https://leetcode.com/problems/unique-paths/ |
| Medium | Edit Distance | https://leetcode.com/problems/edit-distance/ |
| Hard | Interleaving String | https://leetcode.com/problems/interleaving-string/ |
