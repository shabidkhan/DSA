# Trie insert / search

## What is this

A trie (prefix tree) is a rooted tree where each edge is labeled with one character of an alphabet. A path from root to a marked node spells a stored word. Insert and exact-search both run in O(L) where L is the length of the key, independent of how many keys are stored.

This is the foundational trie pattern — building the tree by walking children, marking end-of-word, and querying exact membership.

## Why we use

- O(L) insert and search regardless of dictionary size.
- Shared prefixes are stored once — compact for word lists with overlap.
- Enables O(L) autocomplete and prefix existence checks.
- Stepping stone to wildcard search, longest common prefix, suffix tries.

## How to implement

```
class Node: children = {}; end = False

insert(word):
    node = root
    for c in word:
        node = node.children.setdefault(c, Node())
    node.end = True

search(word):
    node = root
    for c in word:
        if c not in node.children: return False
        node = node.children[c]
    return node.end
```

```python
class Node:
    __slots__ = ("children", "end")
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.end = True

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.end

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def _walk(self, s):
        node = self.root
        for c in s:
            if c not in node.children: return None
            node = node.children[c]
        return node
```

For a fixed alphabet (e.g. lowercase a-z), replace the dict with a 26-cell array for better cache locality.

## Which problems this approach solves in the real world

- Autocomplete suggestion in search bars (`starts_with` + DFS).
- Spell checkers — dictionary membership in O(L).
- IP routing tables (binary trie over address bits).
- Genomic sequence indexing.
- Profanity / blocklist filters on streaming text.

## Pros and cons

**Pros**
- O(L) operations independent of dictionary size.
- Shared prefixes compress storage.
- Naturally supports prefix and autocomplete queries.

**Cons**
- High constant factor — every node stores child pointers.
- Hash maps are simpler when you only need exact membership.
- Memory hungry for large alphabets and sparse trees.

## Limitations

- Not great for very long, low-overlap strings (memory waste).
- Deletion requires care to prune dead branches.
- Wildcard / fuzzy search needs a different algorithm on top (DFS with budget).

## One example

**Problem**: Implement a Trie with the following methods: `insert(word)`, `search(word)`, `startsWith(prefix)`. `search` returns true only if the *exact* word is stored.

**Input**: `insert("apple"); search("apple"); search("app"); startsWith("app"); insert("app"); search("app");`
**Output**: `[null, true, false, true, null, true]`
**Constraints**: `1 <= word.length <= 2000`, lowercase letters.

## Solution explanation

The `Trie` class above satisfies the contract. Walkthrough on the example with a visual of the tree state:

| op                | trie state (paths)                                    | result |
|-------------------|-------------------------------------------------------|--------|
| insert("apple")   | a-p-p-l-e* (* = end)                                  | -      |
| search("apple")   | walk a-p-p-l-e, end? yes                              | True   |
| search("app")     | walk a-p-p, end? no                                   | False  |
| startsWith("app") | walk a-p-p succeeds                                   | True   |
| insert("app")     | a-p-p*-l-e*                                           | -      |
| search("app")     | walk a-p-p, end? yes                                  | True   |

Time per op: O(L). Space: O(total characters across inserted words).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Longest Common Prefix (LeetCode 14) | https://leetcode.com/problems/longest-common-prefix/ |
| Medium | Implement Trie (Prefix Tree) (LeetCode 208) | https://leetcode.com/problems/implement-trie-prefix-tree/ |
| Hard | Word Search II (LeetCode 212) | https://leetcode.com/problems/word-search-ii/ |
