# Anagram detection

## What is this

Anagram detection is the pattern of deciding whether two strings contain exactly the same multiset of characters. Two strings are anagrams if and only if their character frequencies match.

The standard approach uses a frequency hash map (or a fixed-size array for limited alphabets like lowercase English letters). Counting is `O(n)` and uses `O(k)` extra space, where `k` is the alphabet size.

## Why we use

- Avoids the `O(n log n)` cost of sorting both strings.
- Detects anagrams while streaming over the input only once.
- Works as a primitive inside group-anagrams, permutation-in-string, and find-all-anagrams problems.
- Fixed-size counter arrays use a tiny, constant amount of memory.

## How to implement

```text
function isAnagram(s, t):
    if length(s) != length(t): return False
    count = array of 26 zeros
    for ch in s: count[ch - 'a'] += 1
    for ch in t:
        count[ch - 'a'] -= 1
        if count[ch - 'a'] < 0: return False
    return True
```

```python
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    count = [0] * 26
    for ch in s:
        count[ord(ch) - ord('a')] += 1
    for ch in t:
        count[ord(ch) - ord('a')] -= 1
        if count[ord(ch) - ord('a')] < 0:
            return False
    return True
```

```python
from collections import Counter

def is_anagram_counter(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)
```

The invariant is simple: after fully processing `s`, the counter holds character multiplicities of `s`. Decrementing while scanning `t` should bring every entry to zero. Any negative value means `t` has a character that `s` does not, so the answer is `False`.

## Which problems this approach solves in the real world

- Spell-check and typo suggestions: group dictionary words by character signature so a misspelling can match an anagram of valid words.
- Deduplicating product titles in e-commerce where descriptive words are reordered ("red leather wallet" vs "leather red wallet").
- Detecting plagiarism at the sentence level by comparing word frequencies after tokenization.
- DNA/RNA short-read analysis where two reads of the same base composition need to be grouped.
- Building rainbow-table style indices for password lists that share the same character multiset.

## Pros and cons

**Pros**
- Linear time vs `O(n log n)` for sort-based comparison.
- Constant extra space for fixed alphabets.
- Streaming friendly: one pass per string.

**Cons**
- Hash map version is slower in practice than fixed-array version due to hashing overhead.
- Requires both strings in full; cannot answer on a prefix without re-counting.
- Equal-length check is mandatory; forgetting it produces wrong answers.

## Limitations

- Unicode strings need a map and careful normalization (NFC/NFD) because the same visual character may have multiple codepoints.
- Case sensitivity must be handled explicitly (lowercase the input or count separately).
- Multibyte encodings require decoding to codepoints first; byte-level counts are wrong for non-ASCII text.
- Approximate matching ("almost anagrams") is not supported and needs edit distance instead.

## One example

Problem: Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, else `False`. The strings contain only lowercase English letters.

```
Input:  s = "listen", t = "silent"
Output: True

Input:  s = "rat",    t = "car"
Output: False
```

Constraints: `1 <= len(s), len(t) <= 5 * 10^4`.

## Solution explanation

```python
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    count = [0] * 26
    for ch in s:
        count[ord(ch) - ord('a')] += 1
    for ch in t:
        idx = ord(ch) - ord('a')
        count[idx] -= 1
        if count[idx] < 0:
            return False
    return True
```

Walkthrough for `s = "listen"`, `t = "silent"`:

| Step | Action | Key counts (non-zero) |
|------|--------|-----------------------|
| 0 | start | all zero |
| 1 | +l, +i, +s, +t, +e, +n | l:1 i:1 s:1 t:1 e:1 n:1 |
| 2 | -s | l:1 i:1 s:0 t:1 e:1 n:1 |
| 3 | -i | l:1 i:0 s:0 t:1 e:1 n:1 |
| 4 | -l | l:0 i:0 s:0 t:1 e:1 n:1 |
| 5 | -e | l:0 i:0 s:0 t:1 e:0 n:1 |
| 6 | -n | l:0 i:0 s:0 t:1 e:0 n:0 |
| 7 | -t | all zero, no negatives |
| 8 | return True | |

Time: `O(n)` where `n` is the length of either string. Space: `O(1)` for the 26-slot array (or `O(k)` for alphabet size `k`).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Valid Anagram (LeetCode 242) | https://leetcode.com/problems/valid-anagram/ |
| Medium | Group Anagrams (LeetCode 49) | https://leetcode.com/problems/group-anagrams/ |
| Hard | Substring with Concatenation of All Words (LeetCode 30) | https://leetcode.com/problems/substring-with-concatenation-of-all-words/ |
