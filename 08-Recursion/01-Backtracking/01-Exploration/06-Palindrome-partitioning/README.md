# Palindrome partitioning

## What is this

Given a string `s`, partition it into contiguous substrings such that **every substring is a palindrome**. Return all possible partitionings. The natural solution is **backtracking**: scan from the current index, for each possible end position try the prefix as the next chunk if it's a palindrome, then recurse on the suffix.

Decision tree shape: at each call, branch over all valid palindromic prefixes of the remaining suffix. Each leaf (when the suffix is empty) corresponds to one valid partitioning.

## Why we use

- Pure backtracking gives a clean enumeration of all partitions — exactly what the problem asks.
- O(1) extra memory per call beyond the path (using choose/unchoose).
- Easy to layer pruning: skip any prefix that isn't a palindrome → entire subtree pruned.
- Can be accelerated with a precomputed `is_palindrome[i][j]` DP table when the input is large or when called many times.

## How to implement

```
def partition(s):
    res, path = [], []
    def dfs(start):
        if start == len(s):
            res.append(path[:])
            return
        for end in start+1..len(s):
            chunk = s[start:end]
            if is_palindrome(chunk):
                path.append(chunk)
                dfs(end)
                path.pop()
    dfs(0)
    return res
```

Python:

```python
def partition(s: str) -> list[list[str]]:
    res: list[list[str]] = []
    path: list[str] = []

    def is_pal(t: str) -> bool:
        return t == t[::-1]

    def dfs(start: int) -> None:
        if start == len(s):
            res.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            chunk = s[start:end]
            if is_pal(chunk):
                path.append(chunk)
                dfs(end)
                path.pop()

    dfs(0)
    return res
```

JavaScript:

```javascript
function partition(s) {
  const res = [], path = [];
  const isPal = (t) => { for (let i = 0, j = t.length - 1; i < j; i++, j--) if (t[i] !== t[j]) return false; return true; };
  function dfs(start) {
    if (start === s.length) { res.push([...path]); return; }
    for (let end = start + 1; end <= s.length; end++) {
      const chunk = s.slice(start, end);
      if (!isPal(chunk)) continue;
      path.push(chunk);
      dfs(end);
      path.pop();
    }
  }
  dfs(0);
  return res;
}
```

Invariant: at the entry of any `dfs(start)`, `path` lists the palindromic chunks that already cover `s[0..start-1]`, in order.

## Optimisation — precompute palindrome table

For longer strings, compute `pal[i][j] = (s[i..j] is palindrome)` once in O(n²) and then `is_pal` becomes O(1):

```python
def partition_fast(s: str) -> list[list[str]]:
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1]):
                pal[i][j] = True

    res, path = [], []
    def dfs(start: int) -> None:
        if start == n:
            res.append(path[:])
            return
        for end in range(start, n):
            if pal[start][end]:
                path.append(s[start:end + 1])
                dfs(end + 1)
                path.pop()
    dfs(0)
    return res
```

## Which problems this approach solves in the real world

- **Text compression**: chunk a stream into palindromic segments for run-length-like encoding.
- **Linguistic analysis**: split a long word into palindromic morphemes.
- **DNA / protein analysis**: find all palindromic substring decompositions (palindromes show up in restriction enzyme recognition sites).
- **Crossword / wordplay generation**: enumerate ways to break a phrase into palindromic chunks for puzzles.
- **Symmetry-based parsing**: find all ways to decompose a sequence into symmetric segments for compression heuristics.

## Pros and cons

**Pros**
- Direct enumeration of all valid partitions.
- O(n) recursion depth, O(n) path memory.
- Pruning via `is_palindrome` early-exit is cheap and effective.
- Easy to convert to "minimum cuts" version (DP) once the structure is understood.

**Cons**
- Worst-case output size is exponential — every position is a potential cut, so for `s = "aaaa…a"` you get 2^(n−1) partitions.
- Naive `is_palindrome` is O(n) per call → O(n³) overall; precomputed table brings it to O(n²) plus enumeration cost.
- Output dominated by long answer lists; consider a generator/yield interface if you stream results.

## Limitations

- Doesn't directly give the *minimum number* of cuts — for that, use a DP `cuts[i] = min(cuts[j] + 1 for all j < i with s[j..i-1] palindrome)`.
- For "K-partitions exactly", you'd add a depth check (`len(path) == k`) and only commit at that depth.
- Not suitable for streaming — needs full string before partitioning.

## One example

**Problem**: Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return **all possible palindrome partitionings** of `s`.
Constraints: `1 ≤ s.length ≤ 16`, `s` consists of lowercase English letters.

**Input**: `s = "aab"`
**Output**: `[["a", "a", "b"], ["aa", "b"]]`

## Solution explanation

```python
def partition(s: str) -> list[list[str]]:
    res, path = [], []
    def is_pal(t): return t == t[::-1]
    def dfs(start):
        if start == len(s):
            res.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            chunk = s[start:end]
            if is_pal(chunk):
                path.append(chunk)
                dfs(end)
                path.pop()
    dfs(0)
    return res
```

Walk-through on `"aab"`:

| call             | start | tries (start..end) | palindrome? | action                          |
|------------------|-------|---------------------|-------------|----------------------------------|
| dfs(0)           | 0     | "a" (0..1)          | yes         | push "a"; dfs(1)                 |
| dfs(1) [path=[a]]| 1     | "a" (1..2)          | yes         | push "a"; dfs(2)                 |
| dfs(2) [path=[a,a]]| 2   | "b" (2..3)          | yes         | push "b"; dfs(3)                 |
| dfs(3) [path=[a,a,b]]| 3 | — (leaf)            | —           | **commit ["a","a","b"]**         |
| back to dfs(2)   | 2     | done                | —           | pop "b"                          |
| back to dfs(1)   | 1     | "ab" (1..3)         | no          | skip                             |
|                  |       | done                | —           | pop "a"                          |
| back to dfs(0)   | 0     | "aa" (0..2)         | yes         | push "aa"; dfs(2)                |
| dfs(2) [path=[aa]]| 2    | "b" (2..3)          | yes         | push "b"; dfs(3)                 |
| dfs(3) [path=[aa,b]]| 3  | — (leaf)            | —           | **commit ["aa","b"]**            |
| back              | —     | …                   | —           | pop, pop, try "aab" (0..3): no   |

Final answer: `[["a","a","b"], ["aa","b"]]`.

Correctness: every partition of `s` corresponds to a choice of cut positions. By trying every valid first chunk and recursing on the remainder, we enumerate every possible cut sequence. The palindrome check at the first chunk prunes invalid branches early.

- **Time**: O(n · 2^n) in the worst case (e.g. `"aaaa…"`) — exponential output dominates.
- **Space**: O(n) recursion + O(n) path + O(output) for the result list.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Valid Palindrome** — basic two-pointer palindrome check; warm-up for the predicate used in this DFS. | https://leetcode.com/problems/valid-palindrome/ |
| Medium | **Palindrome Partitioning** — the canonical problem above. | https://leetcode.com/problems/palindrome-partitioning/ |
| Hard | **Palindrome Partitioning II** — minimum cuts to partition `s` into palindromes; switch from enumeration to DP. | https://leetcode.com/problems/palindrome-partitioning-ii/ |
