# Z-algorithm

## What is this

The Z-algorithm computes a *Z-array* for a string `s` of length `n`: `z[i]` is the length of the longest substring starting at index `i` that matches a prefix of `s`. Built in O(n) using a sliding "Z-box" `[l, r]` that records the current rightmost prefix match — reusing prior comparisons to skip work.

For pattern matching, run the Z-algorithm on `pattern + "$" + text`; positions where `z[i] == len(pattern)` are matches in the text. Total time O(n + m), single linear pass.

## Why we use

- O(n) construction — strictly linear.
- One single, conceptually clean pass — no separate failure function.
- Z-array enables many substring queries (longest common prefix, count distinct substrings, periodicity).
- Faster constant than KMP in some implementations due to simpler inner loop.

## How to implement

```
z[0] = n
l = r = 0
for i in 1..n-1:
    if i < r: z[i] = min(r - i, z[i - l])
    while i + z[i] < n and s[z[i]] == s[i + z[i]]: z[i] += 1
    if i + z[i] > r: l = i; r = i + z[i]
```

```python
def z_array(s):
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l = i
            r = i + z[i]
    return z

def z_search(text, pat):
    sep = '\x00'
    s = pat + sep + text
    z = z_array(s)
    m = len(pat)
    return [i - m - 1 for i in range(m + 1, len(s)) if z[i] == m]
```

```python
def smallest_period(s):
    z = z_array(s)
    n = len(s)
    for i in range(1, n):
        if i + z[i] == n and n % i == 0:
            return i
    return n
```

The Z-box invariant: when `i < r`, the substring `s[i..r-1]` matches `s[i-l..r-l-1]` (a known prefix segment), so `z[i]` is at least `min(r - i, z[i - l])` for free.

## Which problems this approach solves in the real world

- Substring search with the same O(n + m) guarantee as KMP.
- Computing periodicity / cyclic shift detection.
- "Sum of longest common prefix to s for every suffix" queries.
- Bioinformatics motif scanning.
- Detecting tandem repeats in strings.

## Pros and cons

**Pros**
- O(n + m) worst case.
- Z-array unlocks many string queries beyond substring search.
- Conceptually cleaner than KMP's failure function for some teaches.

**Cons**
- Z-box bookkeeping is subtle.
- Requires a sentinel character that does not appear in text or pattern.
- No native streaming variant.

## Limitations

- Only exact match.
- 2D / fuzzy variants require different algorithms.
- Memory O(n + m) — not as compact as KMP's failure function alone.

## One example

**Problem**: Given strings `haystack` and `needle`, return the first index where `needle` occurs in `haystack`, else -1.

**Input**: `haystack = "abxabcabcaby"`, `needle = "abcaby"`
**Output**: `6`
**Constraints**: `1 <= haystack.length, needle.length <= 10^4`.

## Solution explanation

```python
def strStr(haystack, needle):
    if not needle: return 0
    matches = z_search(haystack, needle)
    return matches[0] if matches else -1
```

Walkthrough on `s = "abcaby" + "$" + "abxabcabcaby"`:

| i | char | z[i] computed | l, r |
|---|------|---------------|------|
| 0 | a    | n             | 0, 0 |
| 1 | b    | 0 (b != a)    | 0, 0 |
| 2 | c    | 0             | 0, 0 |
| 3 | a    | 1 (a==a, b!=b? actually compare to prefix: 1 then mismatch) | 3, 4 |
| ... | ... | (continued)   | ...  |
| 13 | a   | extended      | ...  |
| 13 (in text region) | matches needle prefix of length 6 → z[13] = 6 |

The first `i >= len(needle)+1` with `z[i] == len(needle)` corresponds to text index `i - len(needle) - 1 = 6`.

Time: O(n + m). Space: O(n + m).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find the Index of the First Occurrence in a String (LeetCode 28) | https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/ |
| Medium | Longest Happy Prefix (LeetCode 1392) | https://leetcode.com/problems/longest-happy-prefix/ |
| Hard | Shortest Palindrome (LeetCode 214) | https://leetcode.com/problems/shortest-palindrome/ |
