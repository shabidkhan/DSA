# Index mapping

## What is this

Index mapping stores `value -> index` (or `value -> last_index`) so you can recover *where* something appeared without re-scanning. It is the structural cousin of the lookup pattern, but the value stored is specifically a positional integer (or list of positions), and the typical query is "how far apart are two occurrences?" or "did this exist before index i?".

Examples: nearest duplicate within window k, longest substring with at most one repeat, replace-words-with-indices, build inverse permutations.

## Why we use

- Recover the position of a previously seen value in O(1).
- Reason about distance between two occurrences of the same value.
- Build inverse mappings (permutation, dictionary encoding).
- Drive sliding-window algorithms that close on the last duplicate seen.

## How to implement

```
last = {}
for i, x in enumerate(arr):
    if x in last and i - last[x] <= k:
        # nearby duplicate
    last[x] = i
```

```python
def contains_nearby_duplicate(nums, k):
    last = {}
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False
```

```python
def inverse_permutation(p):
    inv = [0] * len(p)
    for i, v in enumerate(p):
        inv[v] = i
    return inv
```

When multiple positions matter, store a list: `positions[x].append(i)` so you can binary-search inside it later.

## Which problems this approach solves in the real world

- Near-duplicate detection in event streams (same user clicked twice within 5 seconds).
- Inverse indexes in compilers: variable name -> declaration site.
- Reconstructing original order after sorting (`argsort` + inverse).
- Caching last-seen offset in log parsers.
- Mapping enum values to display strings via inverse lookup.

## Pros and cons

**Pros**
- Combines presence test and position recall in one structure.
- O(1) update and query.
- Naturally extends to "all positions" by storing lists.

**Cons**
- Storing positions per value doubles memory in the worst case.
- Stale entries linger unless you actively prune them.
- Position semantics (0-based vs 1-based, before/after update) cause subtle bugs.

## Limitations

- Not useful when you need range-position queries (use a sorted list of positions plus binary search).
- A single `value -> index` map cannot tell you "second-most-recent" without keeping a list.
- Concurrent writers must synchronize; the map is not idempotent w.r.t. ordering.

## One example

**Problem**: Given an integer array `nums` and an integer `k`, return `true` if there are two distinct indices `i` and `j` such that `nums[i] == nums[j]` and `abs(i - j) <= k`.

**Input**: `nums = [1, 2, 3, 1]`, `k = 3`
**Output**: `True`
**Constraints**: `1 <= n <= 10^5`, `0 <= k <= 10^5`.

## Solution explanation

```python
def contains_nearby_duplicate(nums, k):
    last = {}
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False
```

Walkthrough on `nums = [1, 0, 1, 1]`, `k = 1`:

| i | x | last before | match? | last after |
|---|---|-------------|--------|------------|
| 0 | 1 | {}          | no     | {1:0}      |
| 1 | 0 | {1:0}       | no     | {1:0, 0:1} |
| 2 | 1 | {1:0, 0:1}  | 2-0=2 > 1, no | {1:2, 0:1} |
| 3 | 1 | {1:2, 0:1}  | 3-2=1 <= 1, return True |

Time: O(n). Space: O(min(n, k+1)) if you prune old entries.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Contains Duplicate II (LeetCode 219) | https://leetcode.com/problems/contains-duplicate-ii/ |
| Medium | Find and Replace in String (LeetCode 833) | https://leetcode.com/problems/find-and-replace-in-string/ |
| Hard | Contains Duplicate III (LeetCode 220) | https://leetcode.com/problems/contains-duplicate-iii/ |
