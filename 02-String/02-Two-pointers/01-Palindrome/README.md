# Palindrome patterns

## What is this

A palindrome is a string that reads the same forward and backward. Palindrome patterns are the family of techniques used to check, count, or find the longest palindromic substring/subsequence inside a string.

The three common variants are:
- **Two-pointer check**: verify whether a given string is a palindrome.
- **Expand-around-center**: find palindromic substrings by expanding outward from each index (and each pair of indices).
- **DP / Manacher**: count or find longest palindromes in `O(n^2)` (DP) or `O(n)` (Manacher).

## Why we use

- Palindrome checks are a primitive in many string problems (e.g., partitioning, longest palindrome subsequence).
- Expand-around-center is simple, in-place, and `O(n^2)` time with `O(1)` space.
- Recognizing palindromic structure lets you avoid expensive sorting or hashing.
- Manacher solves longest-palindrome problems at typing speed of input (linear time).

## How to implement

```text
function isPalindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]: return False
        l += 1; r -= 1
    return True

function longestPalindrome(s):
    best = ""
    for i in 0..len(s)-1:
        a = expand(s, i, i)       # odd length
        b = expand(s, i, i+1)     # even length
        best = longer(best, a, b)
    return best
```

```python
def is_palindrome(s: str) -> bool:
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True
```

```python
def longest_palindrome(s: str) -> str:
    def expand(l: int, r: int) -> str:
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l + 1 : r]

    best = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        for cand in (odd, even):
            if len(cand) > len(best):
                best = cand
    return best
```

The expand-around-center invariant: for each center (a single index or a gap between two indices), we keep moving the two boundaries outward as long as the characters match. Each center finds the maximum palindrome anchored at it; the global maximum is the answer.

## Which problems this approach solves in the real world

- Detecting palindromic DNA sequences (reverse-complement palindromes) used in restriction enzyme recognition sites.
- Building text-editor features such as "highlight palindromic words" or palindrome puzzles.
- Compression heuristics: encoding repeated symmetric patterns more compactly.
- Reading mirrored license plates / IDs in OCR pipelines that need quick symmetry validation.
- Validating user-generated palindrome content (e.g., word games like SpellTower, palindrome challenges).

## Pros and cons

**Pros**
- Two-pointer check is `O(n)` time and `O(1)` space.
- Expand-around-center is short and works for both odd and even palindromes.
- Manacher's algorithm reaches `O(n)` time for the longest palindrome problem.

**Cons**
- Expand-around-center is `O(n^2)` worst-case (e.g., all same characters).
- Manacher's algorithm is tricky to implement correctly under time pressure.
- DP for palindrome partitioning uses `O(n^2)` memory.

## Limitations

- Naive substring slicing inside loops can blow up memory; track indices instead.
- For very long inputs (`n >= 10^6`), only Manacher or suffix-automaton approaches are feasible.
- Case, whitespace, and punctuation handling must be defined explicitly (e.g., "A man a plan a canal Panama").
- Unicode requires codepoint-aware indexing; byte-level reverse breaks multibyte characters.

## One example

Problem: Given a string `s`, return the longest palindromic substring of `s`.

```
Input:  s = "babad"
Output: "bab"   (or "aba", both are valid)

Input:  s = "cbbd"
Output: "bb"
```

Constraints: `1 <= len(s) <= 1000`, `s` consists of digits and English letters.

## Solution explanation

```python
def longest_palindrome(s: str) -> str:
    def expand(l: int, r: int) -> tuple[int, int]:
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - 1  # inclusive bounds of palindrome

    start, end = 0, 0
    for i in range(len(s)):
        l1, r1 = expand(i, i)        # odd
        l2, r2 = expand(i, i + 1)    # even
        if r1 - l1 > end - start:
            start, end = l1, r1
        if r2 - l2 > end - start:
            start, end = l2, r2
    return s[start : end + 1]
```

Walkthrough for `s = "babad"`:

| i | Odd expand (i,i) → bounds, len | Even expand (i,i+1) → bounds, len | Best so far |
|---|----|----|----|
| 0 | (0,0) "b", len 1 | (1,0) "", len 0 | "b" |
| 1 | (0,2) "bab", len 3 | (2,1) "", len 0 | "bab" |
| 2 | (1,3) "aba", len 3 | (3,2) "", len 0 | "bab" |
| 3 | (3,3) "a", len 1 | (4,3) "", len 0 | "bab" |
| 4 | (4,4) "d", len 1 | n/a | "bab" |

Time: `O(n^2)`. Space: `O(1)` extra (output excluded).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Valid Palindrome (LeetCode 125) | https://leetcode.com/problems/valid-palindrome/ |
| Medium | Longest Palindromic Substring (LeetCode 5) | https://leetcode.com/problems/longest-palindromic-substring/ |
| Hard | Palindrome Pairs (LeetCode 336) | https://leetcode.com/problems/palindrome-pairs/ |
