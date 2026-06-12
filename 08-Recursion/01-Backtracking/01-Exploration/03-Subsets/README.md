# Subsets via backtracking

## What is this

A backtracking algorithm that enumerates the **power set** — all 2ⁿ subsets — of an n-element collection. At each index, you have two choices: **include** the current element in the running subset, or **exclude** it. The recursion tree has depth `n` and binary branching, with each of the 2ⁿ leaves corresponding to exactly one subset. An alternative formulation iterates over starting indices and recursively appends; both produce the same set of outputs but in different orders.

## Why we use

- Enumerates every subset in O(n · 2ⁿ) total work using O(n) recursion stack and O(n) "current subset" buffer.
- The include/exclude recursion teaches the simplest binary backtracking pattern, generalising to "choose-or-not" problems (knapsack-style enumeration).
- The "for-loop-over-starting-index" variant is the foundation for `combinations(n, k)` and subset-sum-with-target enumeration.

## How to implement

```
build(index, current):
    if index == n:
        record(current)
        return
    # exclude
    build(index + 1, current)
    # include
    current.append(arr[index])
    build(index + 1, current)
    current.pop()
```

Python — all subsets, include/exclude form:

```python
def subsets(nums: list[int]) -> list[list[int]]:
    out, current = [], []

    def build(i: int) -> None:
        if i == len(nums):
            out.append(current.copy())
            return
        build(i + 1)                  # exclude nums[i]
        current.append(nums[i])       # include nums[i]
        build(i + 1)
        current.pop()

    build(0)
    return out
```

Python — start-index form (often more convenient for "subsets of size k" or "subsets with sum k"):

```python
def subsets_startindex(nums: list[int]) -> list[list[int]]:
    out, current = [], []

    def build(start: int) -> None:
        out.append(current.copy())    # record at every node
        for i in range(start, len(nums)):
            current.append(nums[i])
            build(i + 1)
            current.pop()

    build(0)
    return out
```

Invariant: at the call `build(i)` in the include/exclude form, `current` contains the chosen elements from `nums[0..i-1]`. The recursion will produce exactly 2^(n - i) subsets — one for every possible decision on the remaining elements.

## Which problems this approach solves in the real world

- **Feature flag combinations**: enumerate every on/off combination of small flag sets for exhaustive testing.
- **Product configurators**: small bundles where every subset of add-ons must be enumerated.
- **Subset-sum / partition problems**: enumerate feasible subsets when DP isn't worth it (small n).
- **A/B test bucket sampling**: small-scale combinatorial coverage.
- **Permission-set audits**: enumerate every subset of granted permissions to check policy invariants.

## Pros and cons

**Pros**
- Conceptually trivial: each element is a binary choice.
- O(n) recursion stack, O(n) auxiliary buffer.
- Easy to convert to "subsets satisfying P" by adding a `prune` check at the include step.
- Iterative bitmask version (`for mask in range(1 << n)`) is equivalent and avoids recursion entirely.

**Cons**
- Output size 2ⁿ grows quickly: n = 25 gives 33 million subsets — already painful to enumerate.
- Without dedup logic, duplicate inputs produce duplicate subsets — sort first and skip duplicates at the same depth.
- The "record at every node" variant produces subsets in a particular tree order, not lexicographic.

## Limitations

- Not viable for n > ~25 unless you only need to **search** for a satisfying subset (use DP or branch-and-bound instead of enumerating).
- For "count subsets with property P" alone, DP over the value axis is typically far faster.
- For random sampling of subsets, use per-element coin flips — don't enumerate.

## One example

**Problem**: Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets; return the solution in any order. Constraints: `1 ≤ nums.length ≤ 10`, `-10 ≤ nums[i] ≤ 10`.

**Input**: `nums = [1, 2, 3]`
**Output**: `[[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]` (any order)

## Solution explanation

```python
def subsets(nums: list[int]) -> list[list[int]]:
    out, current = [], []

    def build(i: int) -> None:
        if i == len(nums):
            out.append(current.copy())
            return
        build(i + 1)
        current.append(nums[i])
        build(i + 1)
        current.pop()

    build(0)
    return out
```

Walk-through on `nums = [1, 2, 3]` — the include/exclude tree (excl. on left, incl. on right):

| recursion path        | current at leaf | subset recorded |
|-----------------------|-----------------|-----------------|
| excl 1, excl 2, excl 3 | []              | []              |
| excl 1, excl 2, incl 3 | [3]             | [3]             |
| excl 1, incl 2, excl 3 | [2]             | [2]             |
| excl 1, incl 2, incl 3 | [2, 3]          | [2, 3]          |
| incl 1, excl 2, excl 3 | [1]             | [1]             |
| incl 1, excl 2, incl 3 | [1, 3]          | [1, 3]          |
| incl 1, incl 2, excl 3 | [1, 2]          | [1, 2]          |
| incl 1, incl 2, incl 3 | [1, 2, 3]       | [1, 2, 3]       |

Each leaf of the binary tree corresponds to one bitmask of length 3, and there are exactly 2³ = 8 of them. The recursion visits each internal node twice (one per branch) and does O(1) work per node, with O(n) at each leaf to copy the subset.

- **Time**: O(n · 2ⁿ) — 2ⁿ leaves, each copies an O(n) subset.
- **Space**: O(n) recursion + O(n) `current` + O(n · 2ⁿ) output.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Combinations** — all subsets of `1..n` of size exactly `k`. | https://leetcode.com/problems/combinations/ |
| Medium | **Subsets II** — input may contain duplicates; sort, then skip duplicates at the same recursion depth. | https://leetcode.com/problems/subsets-ii/ |
| Hard   | **Partition to K Equal Sum Subsets** — backtracking with subset-sum pruning. | https://leetcode.com/problems/partition-to-k-equal-sum-subsets/ |
