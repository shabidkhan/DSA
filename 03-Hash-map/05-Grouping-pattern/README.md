# Grouping pattern

## What is this

Grouping uses a hash map of the form `key_function(x) -> list[x]` to bucket items that share a *derived* property. The key is computed from `x` rather than equal to `x`. Classic example: group anagrams by their sorted-letter signature, group points by slope from origin, group transactions by `(user, date)`.

It converts "find all pairs/groups where property P agrees" from O(n^2) comparisons into a single O(n) pass that emits the groups directly.

## Why we use

- Collapse equivalent items into groups in one pass.
- Reuse arbitrary derivation functions as the bucket key.
- Stream-friendly: groups grow as input arrives.
- Foundation for sharding, partitioning, and GROUP BY in databases.

## How to implement

```
groups = {}
for x in items:
    k = key(x)
    groups.setdefault(k, []).append(x)
return list(groups.values())
```

```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        sig = "".join(sorted(w))
        groups[sig].append(w)
    return list(groups.values())
```

```python
def group_by_first_letter(words):
    g = defaultdict(list)
    for w in words:
        g[w[0]].append(w)
    return dict(g)
```

Choose the key function carefully — it must be hashable and capture the equivalence relation you actually want.

## Which problems this approach solves in the real world

- GROUP BY in SQL engines: tuple of grouping columns becomes the hash key.
- Map-side combining in MapReduce / Spark shuffles.
- Aggregating log lines by `(host, error_class)` for triage.
- Bundling shipments by `(origin, destination, day)`.
- Clustering anagram-like signatures in fuzzy matching.

## Pros and cons

**Pros**
- O(n) grouping in a single pass.
- Key derivation can encode arbitrary equivalence relations.
- Defaultdict makes the code one line.

**Cons**
- Group sizes can skew (one giant bucket wrecks downstream cost models).
- Key computation may itself be expensive (e.g. `sorted(w)` is O(k log k)).
- Memory holds all groups simultaneously — not streaming-friendly past memory limits.

## Limitations

- Equivalence must be expressible as exact equality of a derived value; fuzzy / approximate equivalences need LSH or clustering instead.
- Order within a group depends on input order — explicit sorting may be required.
- Unbounded key cardinality drives memory blowup.

## One example

**Problem**: Given an array of strings `strs`, group the anagrams together. Return the groups in any order.

**Input**: `strs = ["eat", "tea", "tan", "ate", "nat", "bat"]`
**Output**: `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`
**Constraints**: `1 <= len(strs) <= 10^4`, `0 <= len(strs[i]) <= 100`.

## Solution explanation

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for w in strs:
        sig = "".join(sorted(w))
        groups[sig].append(w)
    return list(groups.values())
```

Walkthrough on `strs = ["eat", "tea", "tan"]`:

| w   | sig = sorted | groups state |
|-----|--------------|--------------|
| eat | aet          | {aet:[eat]}  |
| tea | aet          | {aet:[eat, tea]} |
| tan | ant          | {aet:[eat, tea], ant:[tan]} |

Time: O(n * k log k) where k is max word length. Space: O(n * k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Group Anagrams II / Same Number of Vowels (LeetCode 1684 — Count the Number of Consistent Strings) | https://leetcode.com/problems/count-the-number-of-consistent-strings/ |
| Medium | Group Anagrams (LeetCode 49) | https://leetcode.com/problems/group-anagrams/ |
| Hard | Max Points on a Line (LeetCode 149) | https://leetcode.com/problems/max-points-on-a-line/ |
