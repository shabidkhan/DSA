# Reverse words / characters

## What is this

Two related two-pointer string-manipulation tasks: **reverse a whole string** in place, and **reverse the order of words** in a sentence. Both reduce to a sequence of two-pointer swaps. For reversing words, the canonical trick is "reverse the whole string, then reverse each word individually" — yielding the desired order with O(1) extra memory (in mutable arrays).

## Why we use

- O(n) time, O(1) extra space for mutable arrays.
- Two-pointer swaps are cache-friendly and trivial to verify.
- The "reverse twice" trick generalizes to rotations (`rotate(a, k)`).
- Pure string analogue of array reversal — same primitive.

## How to implement

```
reverse(a, lo, hi):
    while lo < hi:
        swap a[lo], a[hi]; lo += 1; hi -= 1

reverse_words(s):
    # 1) reverse whole string in place
    reverse(s, 0, n - 1)
    # 2) reverse each word
    i = 0
    while i < n:
        j = i
        while j < n and s[j] != ' ': j += 1
        reverse(s, i, j - 1)
        i = j + 1
```

```python
def reverse_string(s):
    a = list(s)
    lo, hi = 0, len(a) - 1
    while lo < hi:
        a[lo], a[hi] = a[hi], a[lo]
        lo += 1; hi -= 1
    return "".join(a)
```

```python
def reverse_words_inplace(s):
    a = list(s)
    n = len(a)
    def rev(lo, hi):
        while lo < hi:
            a[lo], a[hi] = a[hi], a[lo]
            lo += 1; hi -= 1
    rev(0, n - 1)
    i = 0
    while i < n:
        j = i
        while j < n and a[j] != ' ':
            j += 1
        rev(i, j - 1)
        i = j + 1
    return "".join(a)
```

For the more practical "trim + collapse whitespace" variant: split on whitespace, reverse the list, rejoin with single spaces.

## Which problems this approach solves in the real world

- Reverse the word order in user-input sentences for display.
- Build right-to-left text rendering pipelines (RTL languages).
- Inverse-tokenize log lines for ordering reports.
- Rotate a string by k positions ("reverse-reverse-reverse" trick).
- Implement undo for typed input.

## Pros and cons

**Pros**
- O(n) time, O(1) extra space (on mutable buffers).
- Two-pointer swap is the simplest possible building block.
- Composes for in-place rotation.

**Cons**
- Python strings are immutable — must convert to list first.
- Whitespace handling (multiple spaces, leading/trailing) needs care.
- Multi-byte / Unicode grapheme clusters break naive char-level reversal.

## Limitations

- Naive char-reverse breaks emoji clusters, combining marks.
- Streaming / partial-input variants require buffering the full token.
- Locale-sensitive ordering (e.g. Hebrew) needs Unicode bidi algorithm.

## One example

**Problem**: Given an input string `s`, reverse the order of the words. A word is a maximal substring of non-space characters. Returned string should have no leading / trailing spaces and exactly one space between words.

**Input**: `s = "the sky is blue"`
**Output**: `"blue is sky the"`
**Constraints**: `1 <= s.length <= 10^4`, `s` contains ASCII characters.

## Solution explanation

```python
def reverseWords(s):
    words = s.split()         # split on runs of whitespace, drops empties
    return " ".join(reversed(words))
```

Walkthrough on `s = "  hello world  "`:

| step           | value                  |
|----------------|------------------------|
| s.split()      | ["hello", "world"]     |
| reversed(...)  | ["world", "hello"]     |
| " ".join(...)  | "world hello"          |

Time: O(n). Space: O(n) for the token list.

For the in-place O(1) variant (LeetCode 151 follow-up), use `reverse_words_inplace` after a pre-processing pass to collapse spaces.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Reverse String (LeetCode 344) | https://leetcode.com/problems/reverse-string/ |
| Medium | Reverse Words in a String (LeetCode 151) | https://leetcode.com/problems/reverse-words-in-a-string/ |
| Hard | Reverse Words in a String II (LeetCode 186) | https://leetcode.com/problems/reverse-words-in-a-string-ii/ |
