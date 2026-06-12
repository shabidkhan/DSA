# Set-based hashing

## What is this

A hash set stores keys only — no values. It is used when you only care whether an element is present, not how many times or what it maps to. Operations are O(1) average for add, remove, contains, and set algebra (union / intersection / difference) is supported in linear time over the smaller operand.

Most "is this a duplicate?", "do these collections overlap?", and "have I visited this node?" patterns are set-based.

## Why we use

- O(1) membership tests.
- Natural deduplication of streams or batches.
- Efficient set algebra: intersection, union, difference.
- Compact "visited" marker for graph / grid traversals.

## How to implement

```
seen = set()
for x in stream:
    if x in seen: handle_dup(x)
    else: seen.add(x)
```

```python
def has_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

```python
def intersection(a, b):
    sa = set(a)
    return [x for x in set(b) if x in sa]
```

Use `frozenset` if you need a hashable, immutable set (e.g. as a dict key).

## Which problems this approach solves in the real world

- Mailing-list deduplication: keep the first occurrence of each email.
- Visited-URL tracking in a web crawler.
- A/B test bucket membership: is `user_id` in the experiment cohort?
- Spell-check / blocklist: is this word in the dictionary?
- Graph traversal: prevent revisiting nodes.

## Pros and cons

**Pros**
- O(1) average membership, add, delete.
- Cleaner than a map when you don't need an associated value.
- Built-in set algebra.

**Cons**
- Loses ordering and multiplicity.
- Memory grows with the number of distinct elements.
- Items must be hashable.

## Limitations

- Cannot store mutable items (lists, dicts) as elements.
- No range queries / predecessor / successor (use a sorted set / TreeSet for those).
- Iteration order is not insertion order (rely on `dict` keys if order matters).

## One example

**Problem**: Given two integer arrays `nums1` and `nums2`, return their intersection — each element in the result must be unique.

**Input**: `nums1 = [1, 2, 2, 1]`, `nums2 = [2, 2]`
**Output**: `[2]`
**Constraints**: `1 <= len <= 10^3`, `0 <= nums[i] <= 1000`.

## Solution explanation

```python
def intersection(nums1, nums2):
    a = set(nums1)
    return list(a & set(nums2))
```

Walkthrough on `nums1 = [4, 9, 5]`, `nums2 = [9, 4, 9, 8, 4]`:

| step | structure | content |
|------|-----------|---------|
| 0    | a = set(nums1) | {4, 9, 5}  |
| 1    | b = set(nums2) | {4, 9, 8}  |
| 2    | a & b          | {4, 9}     |
| 3    | list()         | [4, 9]     |

Time: O(n + m). Space: O(n + m).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Intersection of Two Arrays (LeetCode 349) | https://leetcode.com/problems/intersection-of-two-arrays/ |
| Medium | Longest Substring Without Repeating Characters (LeetCode 3) | https://leetcode.com/problems/longest-substring-without-repeating-characters/ |
| Hard | Number of Atoms (LeetCode 726) | https://leetcode.com/problems/number-of-atoms/ |
