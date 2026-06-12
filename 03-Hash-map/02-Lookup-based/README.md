# Lookup-based hash map

## What is this

A lookup-based hash map answers "have I seen this value, and if so where / what is associated with it?" in O(1) average. Unlike frequency maps that count, lookup maps store a *single* associated value per key — typically an index, a node reference, or a derived complement.

The archetype is Two Sum: scan the array once, and for each `x` ask whether `target - x` was already stored. This converts an O(n^2) double loop into an O(n) single pass.

## Why we use

- Replace nested loops with a single pass plus O(1) lookups.
- Recall positional information (index) for previously seen values.
- Detect duplicates or pair complements while streaming.
- Cache results of expensive computations keyed by input.

## How to implement

```
seen = {}                 # key -> useful info (index, node, computed value)
for i, x in enumerate(nums):
    if needed(x) in seen:
        return (seen[needed(x)], i)
    seen[x] = i
```

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
```

```python
def first_unique_char(s: str) -> int:
    last = {}
    for i, c in enumerate(s):
        if c not in last:
            last[c] = i
        else:
            last[c] = -1  # mark seen more than once
    return min((v for v in last.values() if v != -1), default=-1)
```

The discipline is: check before insert, so you cannot accidentally match an element against itself.

## Which problems this approach solves in the real world

- Detecting duplicate transactions in a financial stream.
- Currency / unit conversion: lookup `from -> to` rate in a rate table.
- DNS / ARP caches mapping name -> address.
- Memoizing expensive function results.
- Session-token validation: `token -> user`.

## Pros and cons

**Pros**
- O(1) average lookup, insert, delete.
- Trivially supports many associated payloads beyond just a count.
- Replaces nested scans with linear scans for many pair / triple problems.

**Cons**
- Worst-case O(n) per operation under pathological hashing.
- Order is not preserved (use `OrderedDict` / list of insertions if needed).
- Memory proportional to distinct keys, not always free.

## Limitations

- Mutable, unhashable keys (list, dict) cannot be stored directly.
- High-cardinality streams may blow memory.
- Not appropriate when you also need range / predecessor queries (use a sorted structure or balanced BST).

## One example

**Problem**: Given an array `nums` and a target `t`, return the indices of the two numbers that add up to `t`. Each input has exactly one solution; you may not use the same element twice.

**Input**: `nums = [2, 7, 11, 15]`, `t = 9`
**Output**: `[0, 1]`
**Constraints**: `2 <= n <= 10^4`, `-10^9 <= nums[i] <= 10^9`.

## Solution explanation

```python
def two_sum(nums, target):
    seen = {}                       # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
```

Walkthrough on `nums = [3, 2, 4]`, `target = 6`:

| i | x | target - x | seen before | hit? | seen after |
|---|---|------------|-------------|------|------------|
| 0 | 3 | 3          | {}          | no   | {3:0}      |
| 1 | 2 | 4          | {3:0}       | no   | {3:0, 2:1} |
| 2 | 4 | 2          | {3:0, 2:1}  | yes  | return [1, 2] |

Time: O(n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Two Sum (LeetCode 1) | https://leetcode.com/problems/two-sum/ |
| Medium | 4Sum II (LeetCode 454) | https://leetcode.com/problems/4sum-ii/ |
| Hard | Longest Consecutive Sequence (LeetCode 128) | https://leetcode.com/problems/longest-consecutive-sequence/ |
