# String Patterns

## Folder structure

```
02-String/
├── README.md
├── 01-Sliding-window/
│   ├── README.md
│   ├── 01-Longest-substring-without-repeat/README.md
│   ├── 02-Min-window-substring/README.md
│   └── 03-Anagram/README.md
├── 02-Two-pointers/
│   ├── README.md
│   ├── 01-Palindrome/README.md
│   ├── 02-Reverse-words/README.md
│   └── 03-String-compression/README.md
└── 03-Pattern-matching/
    ├── README.md
    ├── 01-KMP/README.md
    ├── 02-Rabin-Karp/README.md
    └── 03-Z-algorithm/README.md
```

## What is this

Strings are arrays of characters, so most array techniques apply, but strings come with their own specialised toolkit because the alphabet is small (often just 26 letters or 128 ASCII codes), comparisons are character-by-character, and substring search has its own deeply studied algorithms (KMP, Rabin-Karp, Z-algorithm). The three pillars of string problems are sliding window (longest/shortest substring with a property), two pointers (palindromes, reversal, compression), and pattern matching (find/locate substrings efficiently).

Mastering strings means knowing when a frequency array or hash map beats an inner loop, when a window can expand/shrink cleverly, and when a specialised string-matching algorithm is needed instead of `str.find`.

## Why we use

- String problems show up everywhere: parsing, search, NLP preprocessing, log analysis.
- Bounded alphabets unlock O(1) tricks (fixed-size frequency arrays).
- Pattern matching has linear-time solutions far better than naive O(nm).
- The same skeletons (sliding window, two pointers) generalise from arrays.

## How to implement

Select the matching subpattern:

```
sliding window     — substring with constraint (k distinct, no repeats, anagram)
two pointers       — palindrome check, reverse words, in-place compression
pattern matching   — find pattern P in text T efficiently (KMP, RK, Z)
```

Subpatterns in this folder:

- **01-Sliding-window** — longest substring without repeat, minimum window substring, anagram detection.
- **02-Two-pointers** — palindrome checks, word/string reversal, in-place compression.
- **03-Pattern-matching** — KMP (deterministic linear), Rabin-Karp (rolling hash), Z-algorithm.

## Which problems this approach solves in the real world

- Full-text search inside editors and IDEs (find/replace, regex preprocessing).
- DNA/protein sequence search in bioinformatics.
- Log-line pattern detection in observability tools.
- Plagiarism and similarity detection.
- URL routing and template matching in web frameworks.
- Tokenisation passes in compilers and interpreters.

## Pros and cons

**Pros**
- Bounded alphabets enable O(1) per-character bookkeeping.
- Linear-time pattern matching is achievable with KMP / Z.
- Sliding window solutions are O(n) and easy to reason about.
- Rolling hash gives expected O(n + m) with very small constants.

**Cons**
- Unicode and multi-byte encodings complicate "per-character" assumptions.
- KMP failure-function construction is notoriously error-prone.
- In-place modification often conflicts with immutability in languages like Java/Python.
- Rabin-Karp needs careful hash design to avoid collisions.

## Limitations

- Naive substring search is O(nm) — fine for small inputs, prohibitive at scale.
- True regex matching is exponential in the worst case (catastrophic backtracking).
- Edit-distance and alignment are O(nm) DP problems, not pure string-pattern problems.
- Case-folding, normalization (NFC/NFD), and locale rules are easy to miss.
