# Grid DP (2D state on a matrix)

## What is this

A DP pattern where the state is **two-dimensional** — `dp[i][j]` typically representing "the answer for the rectangle from `(0, 0)` to `(i, j)`" or "the best path ending at `(i, j)`". Transitions look at **adjacent cells** — usually `dp[i-1][j]` (from above) and `dp[i][j-1]` (from the left), and sometimes `dp[i-1][j-1]` (diagonal). The table is filled in row-major (top-to-bottom, left-to-right) order, with each cell taking O(1) work.

Classic examples: Unique Paths, Minimum Path Sum, Edit Distance (on string pairs treated as a grid), Longest Common Subsequence, Maximal Square.

## Why we use

- Models any "navigate a grid making local choices" problem in **O(m·n) time, O(m·n) space** (often reducible to O(n) with rolling rows).
- The 2D structure visually matches the problem — easy to draw the table on paper and verify.
- Extends naturally to "edit distance" on string pairs by treating one string as rows and the other as columns.

## How to implement

```
dp = (m × n) matrix
dp[0][0] = base case
fill row 0 and column 0 with their base cases
for i in 1..m-1:
    for j in 1..n-1:
        dp[i][j] = combine(dp[i-1][j], dp[i][j-1], dp[i-1][j-1], local cost)
return dp[m-1][n-1]
```

Python — Unique Paths (count paths from top-left to bottom-right of an m × n grid):

```python
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]   # first row and column are 1
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
```

Python — Minimum Path Sum (move only right/down, minimise sum):

```python
def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    return dp[m - 1][n - 1]
```

JavaScript — Maximal Square (largest all-1s square submatrix, side length²):

```javascript
function maximalSquare(matrix) {
  const m = matrix.length, n = matrix[0].length;
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  let best = 0;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (matrix[i - 1][j - 1] === '1') {
        dp[i][j] = Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1;
        best = Math.max(best, dp[i][j]);
      }
    }
  }
  return best * best;
}
```

Invariant: by the time we compute `dp[i][j]`, every cell needed (`dp[i-1][j]`, `dp[i][j-1]`, `dp[i-1][j-1]`) is already filled — guaranteed by row-major traversal.

## Visual — Unique Paths on a 3×3 grid

```
1 1 1
1 2 3
1 3 6
```

`dp[2][2] = 6`: there are 6 distinct right/down paths from top-left to bottom-right.

Each cell counts: sum of cell above + cell to the left (each path enters via exactly one of those).

## Which problems this approach solves in the real world

- **Robot pathfinding** on a grid with movement costs (warehouse pick routes).
- **Dynamic image stitching**: minimum-energy seam between overlapping photos (seam carving).
- **Edit distance / diff**: minimum operations to transform one string into another — table over (i, j) for prefix lengths.
- **Maze navigation**: count paths, find shortest, etc.
- **Game design**: number of ways to traverse a board satisfying movement rules.
- **OCR alignment**: best matching path between scanned image rows and reference rows.

## Pros and cons

**Pros**
- O(m·n) time — fast for typical inputs (≤ 10⁶ cells).
- Often reducible to O(n) space using a rolling row.
- Tabular form is easy to debug — print the table.
- Pattern generalises to 3D (`dp[i][j][k]`) for problems like "edit distance with k extra deletes".

**Cons**
- O(m·n) memory in the naive form — can be heavy for huge grids.
- Base cases for row 0 and column 0 are usually distinct from the general recurrence and easy to forget.
- Direction choices (right/down vs all 8) change the recurrence shape — pick deliberately.

## Limitations

- Doesn't handle problems where the path can revisit cells (use BFS / shortest-path).
- Not suited for grids with diagonal-only moves on top of axis moves without rethinking the table shape.
- For problems with obstacle propagation or rolling updates, rolling-row optimisation breaks — keep the full table.

## One example

**Problem**: Given an `m × n` grid filled with non-negative integers, find a path from the **top-left** to the **bottom-right** which **minimises the sum** of all numbers along the path. You may move only **right or down**.
Constraints: `1 ≤ m, n ≤ 200`, `0 ≤ grid[i][j] ≤ 200`.

**Input**:
```
grid = [[1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]]
```
**Output**: `7` — path `1 → 3 → 1 → 1 → 1` sums to 7.

## Solution explanation

```python
def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
    return dp[m - 1][n - 1]
```

Walk-through filling `dp`:

| (i,j) | dp[i-1][j] | dp[i][j-1] | grid[i][j] | dp[i][j]     |
|-------|------------|-------------|-------------|---------------|
| (0,0) | —          | —           | 1           | 1             |
| (0,1) | —          | 1           | 3           | 4             |
| (0,2) | —          | 4           | 1           | 5             |
| (1,0) | 1          | —           | 1           | 2             |
| (1,1) | 4          | 2           | 5           | 5 + min(4,2) = 7 |
| (1,2) | 5          | 7           | 1           | 1 + min(5,7) = 6 |
| (2,0) | 2          | —           | 4           | 6             |
| (2,1) | 7          | 6           | 2           | 2 + min(7,6) = 8 |
| (2,2) | 6          | 8           | 1           | 1 + min(6,8) = 7 |

Final table:
```
1 4 5
2 7 6
6 8 7
```
Answer: `dp[2][2] = 7`.

Correctness: any path to `(i, j)` arrives from either `(i-1, j)` (going down) or `(i, j-1)` (going right). The minimum-sum path to `(i, j)` therefore extends the minimum-sum path to one of those two cells, plus `grid[i][j]`. Base cases at row 0 and column 0 have only one way to reach them — accumulate.

- **Time**: O(m · n).
- **Space**: O(m · n) — reducible to O(n) by keeping only the previous row.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Unique Paths** — count R/D paths from top-left to bottom-right. Simplest grid DP. | https://leetcode.com/problems/unique-paths/ |
| Medium | **Minimum Path Sum** — the canonical problem above. | https://leetcode.com/problems/minimum-path-sum/ |
| Hard | **Edit Distance** — 2D DP over string prefix lengths (rows = `s1`, cols = `s2`); transitions for insert / delete / replace. | https://leetcode.com/problems/edit-distance/ |
