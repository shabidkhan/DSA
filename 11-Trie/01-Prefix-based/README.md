# Prefix-based Trie

## Folder structure

```
01-Prefix-based/
├── README.md
├── 01-Insert-search/README.md
└── 02-Prefix-match/README.md
```

## What is this

A trie (prefix tree) is a tree where each edge represents a character and each path from the root to a node spells a prefix of some inserted string. The prefix-based family answers two questions extremely fast: "is this exact word stored?" and "is there *any* stored word starting with this prefix?" Both take O(L) time, where L is the length of the query — independent of how many words are in the trie.

The pattern shines whenever many strings share prefixes. By collapsing common prefixes into a single path, the trie turns "look me up in 100k words" into "walk 5 edges." Variants extend it for wildcards, autocomplete suggestions, and longest-common-prefix queries.

## Why we use

- Lookup and insert are O(L) — independent of the size of the dictionary.
- Common prefixes are shared in memory; 100k similar words can be far smaller than a hash set.
- Prefix queries (autocomplete) are answered by walking to a node and emitting its subtree.
- Easy to extend for wildcards, edit-distance search, and longest-prefix routing.

## How to implement

```text
class TrieNode:
    children = {}     # char -> TrieNode
    isEnd    = False

function insert(root, word):
    cur = root
    for c in word:
        cur = cur.children.setdefault(c, TrieNode())
    cur.isEnd = True

function search(root, word):
    cur = root
    for c in word:
        if c not in cur.children: return False
        cur = cur.children[c]
    return cur.isEnd

function startsWith(root, prefix):
    cur = root
    for c in prefix:
        if c not in cur.children: return False
        cur = cur.children[c]
    return True
```

Subpatterns in this folder:

- `01-Insert-search/` — basic trie with `insert`, `search`, `startsWith`.
- `02-Prefix-match/` — autocomplete-style "all words with this prefix" via subtree walk.

## Which problems this approach solves in the real world

- Autocomplete suggestions in search bars and IDEs.
- Spell-checkers (find words within edit-distance k of a query).
- IP routing tables (longest-prefix match on binary tries).
- Streaming-keyword detection (Aho-Corasick is a multi-pattern trie extension).
- Tokenizer dictionaries for compressed text formats.
- Predictive text on mobile keyboards.

## Pros and cons

**Pros**
- O(L) operations regardless of dictionary size.
- Memory-efficient when keys share prefixes.
- Naturally supports prefix queries — impossible to do cheaply with hash sets.
- Composes with DFS to answer many richer queries (longest word, suggestions, wildcard search).

**Cons**
- Sparse alphabets waste memory if implemented with fixed-size arrays.
- HashMap-per-node has higher constant than array-per-node — slower in tight loops.
- Deletion is fiddly: must check whether a node is shared by other words before pruning.
- Serialization to disk is non-trivial; flat hash maps are easier to persist.

## Limitations

- Storing arbitrary binary keys requires bit-trie / radix variants.
- Worst-case memory is O(N · L) — bad if strings share no prefixes.
- Range queries on the original alphabet order are awkward — sorted arrays or BSTs may be better.
- Dynamic alphabets (Unicode) make array-per-node infeasible; hash maps are required.
