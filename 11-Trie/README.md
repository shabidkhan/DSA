# Trie Patterns

## Folder structure

```
11-Trie/
├── README.md
├── 01-Prefix-based/
│   ├── 01-Insert-search/README.md
│   └── 02-Prefix-match/README.md
└── 02-Bitwise-trie/README.md
```

## What is this

A trie (prefix tree) is a tree-shaped container of strings where each edge represents a character and each root-to-node path spells a prefix. Tries trade extra memory for blazing-fast prefix queries — insert, search, and `startsWith` are all O(L) where L is the key length, independent of the number of keys stored. Two flavours dominate: classic character tries for word/prefix work, and bitwise tries (binary tries) for XOR-maximisation and integer-prefix problems.

Tries are the right answer whenever you have a dictionary of strings and need to ask prefix, autocomplete, longest-common-prefix, or word-search questions. They're also the structure behind IP routing tables, autocomplete in search bars, and the famous Maximum XOR of Two Numbers in an Array problem.

## Why we use

- O(L) prefix queries — independent of dictionary size.
- Natural fit for autocomplete and spellchecking.
- Bitwise tries solve XOR-max problems that no other structure handles cleanly.
- They merge naturally with DP for word-break, word-search-on-grid, and similar.

## How to implement

Pick by the alphabet:

```
character trie  — each node has up to |alphabet| children, plus an is_word flag
bitwise trie    — each node has 0 / 1 children; depth = number of bits (32 or 64)

insert: walk from root, create nodes for missing chars/bits; mark terminal
search: walk; return is_word at the end
startsWith: walk; success if walk completes
```

Subpatterns in this folder:

- **01-Prefix-based** — insert / search / startsWith for word dictionaries.
- **02-Bitwise-trie** — binary trie for XOR maximisation and integer prefix queries.

## Which problems this approach solves in the real world

- Autocomplete in search bars and IDEs.
- Spellcheckers and "did you mean?" suggestions.
- IP routing tables (longest-prefix match via bitwise trie).
- Phone-number prefix matching for international dialling.
- Plagiarism / DNA sequence prefix lookups.
- T9 keypad input prediction.

## Pros and cons

**Pros**
- O(L) operations independent of dictionary size.
- Prefix queries (autocomplete) are free side-effects of the structure.
- Shared prefixes save memory at scale.
- Bitwise tries give a deterministic O(32) maximum-XOR algorithm.

**Cons**
- High pointer overhead: one node per character is wasteful for sparse data.
- Removing words is fiddly (must clean up empty branches).
- Cache-unfriendly: nodes scatter across memory.
- Implementation complexity is higher than hash maps.

## Limitations

- Hash maps win for pure equality lookup (no prefix needs).
- Memory cost grows with the alphabet size per node.
- Concurrent inserts require fine-grained locking or persistent structures.
- For very long keys or huge dictionaries, radix trees or DAWGs are more compact.
