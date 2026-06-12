# Hash map Patterns

## Folder structure

```
03-Hash-map/
├── README.md
├── 01-Frequency-based/README.md
├── 02-Lookup-based/README.md
├── 03-Set-based/README.md
├── 04-Index-mapping/README.md
└── 05-Grouping-pattern/README.md
```

## What is this

Hash maps (also called dictionaries or hash tables) give average-O(1) lookup, insert, and delete, making them the universal "memory" of algorithms. Whenever you find yourself thinking "have I seen this element before?", "how many times has this happened?", "what's mapped to what?", or "group items by some key" — you're in hash-map territory. The family decomposes into five distinct patterns: frequency counting, fast lookup, set membership, index mapping, and grouping.

The reason hash maps appear in so many algorithms is that they replace expensive scans with constant-time queries, and they let you trade a small amount of memory for huge runtime gains. Two-sum, anagrams, subarray-sum-equals-K, and most "count something" problems all reduce to choosing the right hash-map subpattern.

## Why we use

- O(1) average lookup turns O(n²) brute force into O(n) one-pass solutions.
- They're the universal "state" structure — almost every linear algorithm uses one.
- The five subpatterns (frequency, lookup, set, index, grouping) cover most needs.
- They compose well with arrays, sliding windows, prefix sums, and graphs.

## How to implement

Pick the subpattern by the question shape:

```
frequency      — "how many times does X appear?" → map: key → count
lookup         — "is X here? what's at X?" → map: key → value (often complement-search)
set            — "have I seen X?" → set: just membership
index mapping  — "what index does X live at?" → map: value → index
grouping       — "bucket by property" → map: key → list of items
```

Subpatterns in this folder:

- **01-Frequency** — count occurrences of items.
- **02-Lookup** — fast "have I seen this?" or "what is the complement?" checks.
- **03-Set** — membership-only tracking when counts don't matter.
- **04-Index-mapping** — value → index for fast positional queries.
- **05-Grouping** — bucket items by computed key (anagrams, by-prefix, etc.).

## Which problems this approach solves in the real world

- Caches and memoization tables (LRU, Redis, browser cache).
- Database indexes (hash indexes on equality lookups).
- Symbol tables in compilers and interpreters.
- Duplicate detection in data pipelines.
- Routing tables and DNS lookups.
- Counting unique users, events, or sessions in analytics.

## Pros and cons

**Pros**
- O(1) average for lookup / insert / delete.
- Massive constant-factor speedup over array search.
- Five subpatterns cover most algorithmic counting/lookup needs.
- Easy to combine with other patterns (sliding window + hash map is iconic).

**Cons**
- Worst-case O(n) on hash collisions (rare with good hash functions).
- Higher memory overhead than fixed arrays — typically 2-4x slot bloat.
- Iteration order is undefined in many languages (use ordered maps if order matters).
- Hashing custom objects requires correct `hash` / `equals` contract.

## Limitations

- Not suitable for range queries — use sorted maps or segment trees.
- No prefix or partial-key search — that's what tries are for.
- Adversarial inputs can blow up collisions in some hash schemes.
- Memory usage can grow unboundedly if not capped (caches need eviction).
