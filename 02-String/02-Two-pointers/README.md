# String Two-pointer Patterns

## Folder structure

```
02-Two-pointers/
├── README.md
├── 01-Palindrome/README.md
├── 02-Reverse-words/README.md
└── 03-String-compression/README.md
```

## What is this

Two-pointer techniques on strings use two coordinated indices that walk through the characters either from opposite ends (palindrome checks, reverse-in-place) or in lock-step from the same end (in-place compression, word-by-word reversal). The mental model is identical to two-pointer on arrays, but the character domain unlocks language-specific tricks — alphabet-size bookkeeping, case folding, whitespace handling, and in-place mutation when the language permits.

The three canonical subproblems are: palindrome verification (l/r converge, compare characters, skip non-alphanumerics if needed), reverse words in a string (reverse the whole string then reverse each word, or split-reverse-join), and string compression (read pointer scans, write pointer emits a compact representation).

## Why we use

- O(n) replacement for naive O(n²) "compare all pairs" approaches.
- O(1) extra space when in-place modification is allowed.
- Mental simplicity: l/r or read/write pointers are easy to reason about.
- Same skeleton ports straight from arrays — low cognitive load.

## How to implement

```
palindrome (with skip rules):
    l, r = 0, n - 1
    while l < r:
        if not is_alnum(s[l]): l += 1
        elif not is_alnum(s[r]): r -= 1
        elif s[l].lower() != s[r].lower(): return False
        else: l += 1; r -= 1
    return True

reverse words:
    reverse the whole string
    then for each word boundary, reverse that word in place

in-place compression:
    write = 0
    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]: j += 1
        s[write] = s[i]; write += 1
        if j - i > 1:
            for d in str(j - i): s[write] = d; write += 1
        i = j
    return write     # new length
```

Subpatterns in this folder:

- **01-Palindrome** — l/r converging with optional skip rules for non-alphanumerics.
- **02-Reverse-words** — reverse-then-reverse trick for in-place word reversal.
- **03-String-compression** — read/write pointer for run-length-style compaction.

## Which problems this approach solves in the real world

- Palindrome / mirror validation in DNA and text processing.
- In-place reversal of editor lines or terminal buffers.
- Compact representation of repeating-character data.
- Whitespace normalisation in text pipelines.
- Two-string comparison under skip rules (versioning, normalisation).
- Cleanup passes in tokenisers and lexers.

## Pros and cons

**Pros**
- O(n) time, O(1) extra space when in-place is allowed.
- Template is identical to array two-pointer — small mental tax.
- In-place modification suits memory-constrained environments.
- Generalises to streams when reading is monotonic.

**Cons**
- Unicode and combining characters break naive character-by-character comparisons.
- Case-insensitive comparison needs explicit locale-aware folding.
- In-place modification is impossible on immutable strings (Java, Python).
- Skip-rule logic balloons quickly when multiple categories must be ignored.

## Limitations

- Cannot solve patterns that need lookahead beyond the two pointers.
- Multi-byte encodings (UTF-8) require byte-vs-character awareness.
- "Words" definition is locale-specific (spaces, tabs, punctuation).
- Pattern matching needs different algorithms (KMP / Z / Rabin-Karp).
