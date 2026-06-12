# Trie prefix match

## What is this

Prefix match uses a trie to enumerate or test all strings sharing a given prefix. Walk down the trie following the prefix; if the walk succeeds, every word stored in the subtree rooted at the landing node has that prefix. DFS or BFS the subtree to enumerate them.

This is the basis of autocomplete, prefix-frequency queries, and "find all words starting with X" features.

## Why we use

- O(L) walk to the prefix node, then O(matches) to enumerate.
- Independent of dictionary size for the prefix step.
- Naturally supports ranking by storing aggregated counts at each node.
- Generalizes to "shortest unique prefix" and "longest common prefix".

## How to implement

```
node = root
for c in prefix:
    if c not in node.children: return []
    node = node.children[c]
# DFS from node collecting words with `end = True`
dfs(node, prefix, results)
```

```python
class Node:
    def __init__(self):
        self.children = {}
        self.end = False

def insert(root, word):
    n = root
    for c in word:
        n = n.children.setdefault(c, Node())
    n.end = True

def words_with_prefix(root, prefix):
    n = root
    for c in prefix:
        if c not in n.children:
            return []
        n = n.children[c]
    out = []
    def dfs(n, path):
        if n.end: out.append(path)
        for c, ch in n.children.items():
            dfs(ch, path + c)
    dfs(n, prefix)
    return out
```

Decorate each node with a count of words in its subtree if you need O(1) "how many words start with X".

## Which problems this approach solves in the real world

- Search-as-you-type suggestion lists.
- Command-line tab completion (shells, IDEs).
- DNS zone enumeration by suffix (reverse the keys).
- Forensic search: find all log lines beginning with a known fragment.
- Autosuggest with ranking (store frequency at each end-node).

## Pros and cons

**Pros**
- Prefix step is independent of total word count.
- Subtree enumeration is exactly proportional to matches.
- Easy to extend to ranked top-k via heaps.

**Cons**
- Heavy memory for large alphabets / long words.
- DFS enumeration cost dominates when prefixes are short.
- Branch caching at internal nodes adds bookkeeping.

## Limitations

- Wildcard mid-prefix (e.g. "a*c") requires branching DFS, breaking O(L).
- Frequency / ranking must be maintained eagerly.
- Doesn't help with arbitrary substring search — that needs suffix trees.

## One example

**Problem**: Given a list of products and a string `searchWord`, return after each prefix of `searchWord` (of length 1, 2, ...) the three lexicographically smallest products with that prefix.

**Input**: `products = ["mobile","mouse","moneypot","monitor","mousepad"]`, `searchWord = "mouse"`
**Output**:
```
[["mobile","moneypot","monitor"],
 ["mobile","moneypot","monitor"],
 ["mouse","mousepad"],
 ["mouse","mousepad"],
 ["mouse","mousepad"]]
```
**Constraints**: `1 <= n, len(searchWord) <= 1000`.

## Solution explanation

```python
def suggestedProducts(products, searchWord):
    root = Node()
    for w in sorted(products):
        insert(root, w)

    def first_three(n, path):
        out = []
        stack = [(n, path)]
        while stack and len(out) < 3:
            node, p = stack.pop(0)
            if node.end: out.append(p)
            for c in sorted(node.children):
                stack.append((node.children[c], p + c))
        return out

    out = []
    n = root
    prefix = ""
    cut = False
    for c in searchWord:
        prefix += c
        if cut or c not in n.children:
            cut = True
            out.append([])
            continue
        n = n.children[c]
        out.append(first_three(n, prefix))
    return out
```

Walkthrough for `searchWord = "mouse"` on `products` sorted = `["mobile","moneypot","monitor","mouse","mousepad"]`:

| prefix | landing path | first three lexicographic |
|--------|--------------|---------------------------|
| m      | m            | mobile, moneypot, monitor |
| mo     | m-o          | mobile, moneypot, monitor |
| mou    | m-o-u        | mouse, mousepad           |
| mous   | m-o-u-s      | mouse, mousepad           |
| mouse  | m-o-u-s-e    | mouse, mousepad           |

Time: O(sum of |product|) build + O(L * 3) per prefix query. Space: O(sum of |product|).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Longest Word in Dictionary (LeetCode 720) | https://leetcode.com/problems/longest-word-in-dictionary/ |
| Medium | Search Suggestions System (LeetCode 1268) | https://leetcode.com/problems/search-suggestions-system/ |
| Hard | Stream of Characters (LeetCode 1032) | https://leetcode.com/problems/stream-of-characters/ |
