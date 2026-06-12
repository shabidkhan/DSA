# Permutations via backtracking

## What is this

A backtracking algorithm that enumerates all `n!` orderings of a collection. At each recursion level you **choose** an unused element, append it to the current partial permutation, recurse on the remaining elements, then **undo** the choice. The recursion tree has depth `n` and branching factor equal to the number of remaining unused elements, so every leaf of the tree corresponds to exactly one full permutation.

## Why we use

- Produces all permutations in O(n · n!) time using O(n) recursion stack and O(n) "current permutation" buffer — no auxiliary set of permutations stored in memory until the leaf.
- The choose/recurse/undo skeleton is identical to the one used for combinations, subsets, and N-queens — a single mental model for many enumeration tasks.
- Easy to add **pruning** for permutations-with-constraint problems (e.g. permutations summing to k, permutations matching a regex).

## How to implement

```
permute(current, available):
    if available is empty:
        record(current)
        return
    for each element x in available:
        current.append(x)
        remove x from available
        permute(current, available)
        add x back to available
        current.pop()
```

Python — all permutations using a `used` boolean array:

```python
def permutations(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    out: list[list[int]] = []
    current: list[int] = []
    used = [False] * n

    def backtrack() -> None:
        if len(current) == n:
            out.append(current.copy())
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            current.append(nums[i])
            backtrack()
            current.pop()
            used[i] = False

    backtrack()
    return out
```

Python — unique permutations when input has duplicates:

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    nums.sort()
    n = len(nums)
    out, current = [], []
    used = [False] * n

    def backtrack() -> None:
        if len(current) == n:
            out.append(current.copy())
            return
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue        # skip duplicate at same level
            used[i] = True
            current.append(nums[i])
            backtrack()
            current.pop()
            used[i] = False

    backtrack()
    return out
```

Invariant: at any call to `backtrack()`, `current` holds a valid partial permutation, and `used[i]` is `True` iff `nums[i]` already appears in `current`. The undo restores the same state that existed before the choice, so sibling branches see a clean slate.

## Which problems this approach solves in the real world

- **Test fixture generation**: enumerate all argument orderings to probe order-sensitive APIs.
- **Travel itinerary planning**: enumerate visit orders when the search space is small.
- **Cryptographic puzzle / cryptarithm solving**: try every digit assignment for letters.
- **Production scheduling**: enumerate small task orderings to find one satisfying a constraint.
- **Game AI for small boards**: brute-force every move ordering when depth is shallow.

## Pros and cons

**Pros**
- Conceptually simple — one recursive function, one `used` array.
- O(n) recursion depth, O(n) auxiliary state per path — memory-efficient.
- Easy to plug in early pruning ("if partial sum already > target, return").
- Generalises to "next permutation" (lexicographic walking) and "k-th permutation" (factorial number system) with small tweaks.

**Cons**
- Exponential output size: `n!` grows astronomically (10! ≈ 3.6 million, 15! ≈ 1.3 trillion).
- Without dedup logic, duplicate inputs produce duplicate permutations.
- Recursive solution may blow the Python stack for `n > ~1000` (though factorial blowup makes that academic).

## Limitations

- Doesn't scale to large `n` — combinatorial explosion is fundamental, not algorithmic.
- Only practical when permutations themselves are the answer (or you're scanning for one that meets a property with aggressive pruning).
- "Random permutation" or "k-th permutation" is much faster via Fisher-Yates / factorial number system — don't enumerate.

## One example

**Problem**: Given an array `nums` of distinct integers, return all the possible permutations. Constraints: `1 ≤ nums.length ≤ 6`, `-10 ≤ nums[i] ≤ 10`, all integers are unique.

**Input**: `nums = [1, 2, 3]`
**Output**: `[[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]`

## Solution explanation

```python
def permutations(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    out, current = [], []
    used = [False] * n

    def backtrack() -> None:
        if len(current) == n:
            out.append(current.copy())
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            current.append(nums[i])
            backtrack()
            current.pop()
            used[i] = False

    backtrack()
    return out
```

Walk-through on `nums = [1, 2, 3]` (showing the recursion tree as a table; depth = length of `current`):

| depth | current   | next picks tried | comment                  |
|-------|-----------|------------------|--------------------------|
| 0     | []        | 1, 2, 3          | root                     |
| 1     | [1]       | 2, 3             | (skip 1 — used)          |
| 2     | [1, 2]    | 3                | (skip 1, 2 — used)       |
| 3     | [1, 2, 3] | —                | leaf → record            |
| 2     | [1, 3]    | 2                | undo to [1], then pick 3 |
| 3     | [1, 3, 2] | —                | leaf → record            |
| 1     | [2]       | 1, 3             | back to root, pick 2     |
| ...   | (continues mirror-symmetrically for [2,1,3], [2,3,1], [3,1,2], [3,2,1]) |

Each recursive call iterates over `n` candidates and does O(1) work outside the recursion; the total number of node visits is the size of the permutation tree, `Σ n!/k!` ≈ `e · n!`.

- **Time**: O(n · n!) — `n!` leaves, each copying an n-length list.
- **Space**: O(n) recursion depth + O(n) used array + O(n · n!) for the output.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Letter Case Permutation** — for each alphabetic character, choose lower or upper. | https://leetcode.com/problems/letter-case-permutation/ |
| Medium | **Permutations II** — input may contain duplicates; emit unique permutations only. | https://leetcode.com/problems/permutations-ii/ |
| Hard   | **Permutation Sequence** — return the k-th permutation of `1..n` directly via factorial number system. | https://leetcode.com/problems/permutation-sequence/ |
