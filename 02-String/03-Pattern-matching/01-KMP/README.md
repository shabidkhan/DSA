# KMP (Knuth-Morris-Pratt)

## What is this

KMP matches a pattern `p` of length `m` against a text `t` of length `n` in O(n + m) by avoiding redundant comparisons. It precomputes a *failure function* (also called LPS — longest proper prefix that is also a suffix) for the pattern: `lps[i]` is the length of the longest proper prefix of `p[0..i]` that equals a suffix of `p[0..i]`.

When a mismatch occurs after matching some prefix of length `j`, instead of restarting at the next text position, KMP slides the pattern so that the matched prefix's longest "self-suffix" overlaps with the text — skipping work it has already verified.

## Why we use

- Worst-case O(n + m) — independent of alphabet and content.
- Preprocesses only the pattern (O(m)); reusable across many texts.
- Deterministic — no hashing collisions to defend against.
- Foundation for periodicity detection (smallest period = m - lps[m-1] if it divides m).

## How to implement

```
build_lps(p):
    lps = [0] * m
    length = 0; i = 1
    while i < m:
        if p[i] == p[length]: length += 1; lps[i] = length; i += 1
        elif length: length = lps[length - 1]
        else:        lps[i] = 0; i += 1
    return lps

kmp_search(t, p):
    lps = build_lps(p)
    i = j = 0
    while i < n:
        if t[i] == p[j]: i += 1; j += 1; if j == m: yield i - m; j = lps[j-1]
        elif j:           j = lps[j - 1]
        else:             i += 1
```

```python
def build_lps(p):
    m = len(p)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if p[i] == p[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text, pat):
    if not pat: return [0]
    lps = build_lps(pat)
    out = []
    i = j = 0
    while i < len(text):
        if text[i] == pat[j]:
            i += 1; j += 1
            if j == len(pat):
                out.append(i - j)
                j = lps[j - 1]
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return out
```

The text index `i` never moves backward — that's the whole point.

## Which problems this approach solves in the real world

- grep / Boyer-Moore-Horspool family substring search.
- DNA sequence motif discovery (small alphabet, exact match).
- Plagiarism detection — locate shared substrings.
- Network IDS signature matching against streams.
- Detect string periodicity / smallest period via the lps array.

## Pros and cons

**Pros**
- O(n + m) worst case.
- No hashing, no false positives.
- LPS array unlocks period analysis.

**Cons**
- LPS construction is subtle and bug-prone.
- Cache-less probing on long patterns underperforms SIMD-accelerated alternatives.
- Multi-pattern needs Aho-Corasick generalization.

## Limitations

- Only exact matching — no wildcards, no fuzzy.
- Slower in practice than Boyer-Moore on large alphabets.
- 2D / k-mismatch variants are non-trivial extensions.

## One example

**Problem**: Given two strings `haystack` and `needle`, return the index of the first occurrence of `needle` in `haystack`, or -1 if not found. If `needle` is empty, return 0.

**Input**: `haystack = "sadbutsad"`, `needle = "sad"`
**Output**: `0`
**Constraints**: `1 <= haystack.length, needle.length <= 10^4`, lowercase letters.

## Solution explanation

```python
def strStr(haystack, needle):
    if not needle: return 0
    lps = build_lps(needle)
    i = j = 0
    while i < len(haystack):
        if haystack[i] == needle[j]:
            i += 1; j += 1
            if j == len(needle):
                return i - j
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return -1
```

Walkthrough on `needle = "ababc"`. LPS construction:

| i | char | length before | match? | lps[i] | length after |
|---|------|---------------|--------|--------|--------------|
| 1 | b    | 0             | b!=a   | 0      | 0            |
| 2 | a    | 0             | a==a   | 1      | 1            |
| 3 | b    | 1             | b==b   | 2      | 2            |
| 4 | c    | 2             | c!=a (after fallback to lps[1]=0) | 0 | 0 |

lps = [0, 0, 1, 2, 0]. Search on `haystack = "abababc"`:

| i | j | t[i] | p[j] | action |
|---|---|------|------|--------|
| 0 | 0 | a    | a    | match, i=1, j=1 |
| 1 | 1 | b    | b    | match, i=2, j=2 |
| 2 | 2 | a    | a    | match, i=3, j=3 |
| 3 | 3 | b    | b    | match, i=4, j=4 |
| 4 | 4 | a    | c    | mismatch, j = lps[3] = 2 |
| 4 | 2 | a    | a    | match, i=5, j=3 |
| 5 | 3 | b    | b    | match, i=6, j=4 |
| 6 | 4 | c    | c    | match, i=7, j=5 → found at 7-5=2 |

Time: O(n + m). Space: O(m).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find the Index of the First Occurrence in a String (LeetCode 28) | https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/ |
| Medium | Repeated Substring Pattern (LeetCode 459) | https://leetcode.com/problems/repeated-substring-pattern/ |
| Hard | Shortest Palindrome (LeetCode 214) | https://leetcode.com/problems/shortest-palindrome/ |
