# Rabin-Karp (rolling hash)

## What is this

Rabin-Karp searches for a pattern in a text by hashing fixed-size windows of the text and comparing hashes to the pattern's hash. The trick is a *rolling hash*: hash of `t[i+1..i+m]` is computed in O(1) from hash of `t[i..i+m-1]` by subtracting the leaving character's weight and adding the entering character's weight. Total time O(n + m) expected, O(n*m) worst case (when many false-positive hash hits force string equality re-checks).

A double hash (two different moduli) makes adversarial collisions effectively impossible — common in competitive programming for "compare two substrings in O(1)" queries.

## Why we use

- Expected O(n + m) for single-pattern search.
- Naturally handles **multi-pattern** search when patterns share length: hash all patterns into a set, slide one hash through text.
- Enables O(1) substring equality after O(n) prefix-hash precompute.
- Foundation for substring deduplication and chunking (e.g. content-defined chunking, rsync).

## How to implement

```
pre-pick base B (e.g. 31, 257) and modulus M (e.g. 10**9 + 7)
h_pat = hash(p)
h_win = hash(t[0..m-1])
power_m = B^m mod M
for i in 0..n-m:
    if h_win == h_pat and t[i..i+m-1] == p: yield i
    if i + m < n:
        h_win = (h_win * B - t[i] * power_m + t[i+m]) mod M
```

```python
def rabin_karp(text, pat, B=257, M=10**9 + 7):
    n, m = len(text), len(pat)
    if m == 0 or n < m: return []
    h_pat = 0
    h_win = 0
    power = 1
    for i in range(m):
        h_pat = (h_pat * B + ord(pat[i])) % M
        h_win = (h_win * B + ord(text[i])) % M
        if i < m - 1:
            power = (power * B) % M
    out = []
    for i in range(n - m + 1):
        if h_win == h_pat and text[i:i+m] == pat:
            out.append(i)
        if i + m < n:
            h_win = (h_win - ord(text[i]) * power) % M
            h_win = (h_win * B + ord(text[i + m])) % M
            h_win %= M
    return out
```

```python
class StringHash:
    def __init__(self, s, B=131, M=10**9 + 7):
        n = len(s)
        self.B = B; self.M = M
        self.h = [0] * (n + 1)
        self.pw = [1] * (n + 1)
        for i, c in enumerate(s):
            self.h[i+1] = (self.h[i] * B + ord(c)) % M
            self.pw[i+1] = (self.pw[i] * B) % M

    def query(self, l, r):           # hash of s[l..r]
        return (self.h[r+1] - self.h[l] * self.pw[r-l+1]) % self.M
```

Always verify hash hits by character comparison — collisions are rare but real.

## Which problems this approach solves in the real world

- Multi-pattern substring search at scale.
- File-deduplication systems chunking on content boundaries (rsync, restic).
- Detect plagiarism by comparing many document fingerprints.
- DNA / protein motif matching against reference genomes.
- Substring uniqueness / palindrome counting via O(1) hash queries.

## Pros and cons

**Pros**
- O(n + m) expected; rolling-hash idea is reusable for many problems.
- Trivial multi-pattern variant when patterns share length.
- O(1) substring equality after O(n) prefix-hash build.

**Cons**
- Worst case O(n*m) under hash collisions.
- Choice of base / modulus matters; bad choices invite attacks.
- Modular arithmetic obscures the code.

## Limitations

- Different-length multi-pattern needs Aho-Corasick.
- Floating-point hashing loses precision over long windows.
- Adversarial input can force collisions with single-hash; use two moduli.

## One example

**Problem**: Given two strings `haystack` and `needle`, return the index of the first occurrence of `needle` in `haystack`, or -1 if not found.

**Input**: `haystack = "sadbutsad"`, `needle = "sad"`
**Output**: `0`
**Constraints**: `1 <= haystack.length, needle.length <= 10^4`.

## Solution explanation

```python
def strStr(haystack, needle):
    matches = rabin_karp(haystack, needle)
    return matches[0] if matches else -1
```

Walkthrough on `haystack = "abca"`, `needle = "bc"` (B = 257, M = 10^9+7 for clarity):

| i | window  | h_win                  | h_pat == h_win? | char check | result |
|---|---------|------------------------|------------------|------------|--------|
| 0 | "ab"    | 97*257 + 98 = 25027    | no               | -          | -      |
| 1 | "bc"    | (25027 - 97*257)*1 + 99? recompute via roll | yes | "bc"=="bc" | match at 1 |
| 2 | "ca"    | rolled                 | no               | -          | -      |

Return 1 (or -1 if no match). Time: O(n + m) expected. Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Find the Index of the First Occurrence in a String (LeetCode 28) | https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/ |
| Medium | Repeated DNA Sequences (LeetCode 187) | https://leetcode.com/problems/repeated-dna-sequences/ |
| Hard | Longest Duplicate Substring (LeetCode 1044) | https://leetcode.com/problems/longest-duplicate-substring/ |
