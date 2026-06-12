# String Pattern Matching

## Folder structure

```
03-Pattern-matching/
├── README.md
├── 01-KMP/README.md
├── 02-Rabin-Karp/README.md
└── 03-Z-algorithm/README.md
```

## What is this

String pattern matching answers "where does the pattern P (length m) occur inside the text T (length n)?". The naive double-loop is O(nm); three specialised algorithms achieve O(n + m) average or worst case by exploiting structure in P. The three classical algorithms here are **KMP** (Knuth-Morris-Pratt: deterministic O(n + m) via a failure / LPS array), **Rabin-Karp** (rolling hash for expected O(n + m), excellent for multi-pattern search), and **Z-algorithm** (Z-array gives a different O(n + m) angle that's simpler than KMP for many uses).

Knowing which algorithm to reach for depends on the workload: KMP and Z are deterministic; Rabin-Karp wins when you need many patterns at once (precompute hashes, query in O(m) each). All three rely on a precomputed structure that summarises "useful prefix knowledge" of the pattern so the text pointer never has to back up.

## Why we use

- O(n + m) replaces naive O(nm); for long texts this is a huge win.
- Rolling hash (RK) supports multiple patterns and approximate matches.
- KMP / Z give worst-case linear time with no probabilistic assumptions.
- Deterministic linear scan over the text — friendly to streaming and very long inputs.

## How to implement

```
KMP:
    1. Build LPS (longest proper prefix that is also a suffix) array for P.
    2. Scan T with pointer i; on mismatch, fall back to LPS[j-1] (j = pattern pointer).
    3. Every match found in O(n + m) total.

Rabin-Karp (rolling hash):
    1. Compute hash of P and of T[0..m-1].
    2. Slide the window in T, updating hash in O(1) using add-new-drop-old.
    3. On hash match, verify character-by-character to avoid false positives.

Z-algorithm:
    1. Build Z-array: Z[i] = longest substring starting at i that matches a prefix of S.
    2. Run on (P + "$" + T); positions in T with Z[i] == m are matches.
```

Subpatterns in this folder:

- **01-KMP** — failure-function-based deterministic linear matcher.
- **02-Rabin-Karp** — rolling hash for expected linear matching and multi-pattern search.
- **03-Z-algorithm** — Z-array linear matcher; simple, fast, and elegant.

## Which problems this approach solves in the real world

- Substring search in editors and IDEs (find / find-and-replace).
- DNA / protein motif search in bioinformatics.
- Log-line pattern matching in observability and SIEM systems.
- Web-crawler URL pattern matching.
- Plagiarism detection (with rolling hashes for variable-length matches).
- Stream-mode `grep` for very large logs.

## Pros and cons

**Pros**
- O(n + m) — optimal for single-pattern search.
- Rolling hash supports many patterns at once.
- Stream-friendly — no need to backtrack the text pointer.
- Z-algorithm doubles as a tool for many string problems (longest palindrome, etc.).

**Cons**
- KMP's failure function construction is famously error-prone.
- Rabin-Karp needs careful hash design to avoid collisions; mod choice matters.
- Z-array is conceptually clean but rarely the default in libraries.
- Implementations are denser and harder to debug than naive search.

## Limitations

- All assume a finite ordered alphabet; very large alphabets can hurt RK constants.
- Approximate / fuzzy matching needs different algorithms (Bitap, dynamic programming).
- Regex matching is a richer problem and uses NFA / DFA construction.
- For small texts, the naive O(nm) is often faster due to lower constants.
