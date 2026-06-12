# Frequency-based hash map

## What is this

A frequency-based hash map counts how many times each element (key) appears in a stream or collection. The map stores `key -> count` and is updated incrementally as you scan input. It turns "how many of X are there?" from an O(n) per-query scan into an O(1) lookup after a single O(n) pass.

This pattern underpins anagram checks, "majority element" problems, sliding-window character counts, and any situation where decisions depend on multiplicity rather than position.

## Why we use

- Constant-time lookup of any element's count.
- Single linear pass to build, then arbitrary queries.
- Naturally supports incremental updates (add/remove one occurrence at a time).
- Cleanly separates *what* values appear from *where* they appear.
- Foundation for higher-level patterns: sliding-window frequency, k-most-common, etc.

## How to implement

```
freq = {}
for x in stream:
    freq[x] = freq.get(x, 0) + 1
# Query:
freq.get(key, 0)
```

```python
from collections import Counter

def char_freq(s: str) -> dict:
    return dict(Counter(s))

print(char_freq("mississippi"))
# {'m': 1, 'i': 4, 's': 4, 'p': 2}
```

```python
def most_frequent(nums):
    freq = {}
    for n in nums:
        freq[n] = freq.get(n, 0) + 1
    return max(freq, key=freq.get)
```

Use `collections.Counter` when you need ranking (`most_common(k)`), arithmetic on counts, or set-like operations between two counters.

## Which problems this approach solves in the real world

- Word-frequency analysis in search engines and document indexing.
- Bot detection by counting requests per IP in a time window.
- Inventory management — track quantity on hand for each SKU.
- Vote tallying in elections or polls.
- Telemetry: counting error codes emitted by a service over a window.

## Pros and cons

**Pros**
- O(1) average insert / lookup.
- Trivial to implement with built-in dict / Counter.
- Composes well with sliding windows and two-pointer scans.

**Cons**
- O(n) extra space.
- Hash collisions and resizing cause occasional spikes.
- Loses ordering information — only counts survive.

## Limitations

- Floating-point keys are risky (hash equality on floats is fragile).
- Unordered: you cannot answer "what was the order they appeared in" without a parallel structure.
- Not suitable when the universe of keys is huge and most appear once (use sketches like Count-Min instead).

## One example

**Problem**: Given an array of integers `nums`, return the element that appears more than `n/2` times. You may assume the majority element always exists.

**Input**: `nums = [3, 2, 3]`
**Output**: `3`
**Constraints**: `1 <= n <= 5*10^4`, `-10^9 <= nums[i] <= 10^9`.

## Solution explanation

```python
def majority_element(nums):
    freq = {}
    n = len(nums)
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
        if freq[x] > n // 2:
            return x
```

Walkthrough on `nums = [2, 2, 1, 1, 1, 2, 2]` (n=7, threshold=3):

| step | x | freq after update | returns? |
|------|---|-------------------|----------|
| 0    | 2 | {2:1}             | no       |
| 1    | 2 | {2:2}             | no       |
| 2    | 1 | {2:2, 1:1}        | no       |
| 3    | 1 | {2:2, 1:2}        | no       |
| 4    | 1 | {2:2, 1:3}        | no       |
| 5    | 2 | {2:3, 1:3}        | no       |
| 6    | 2 | {2:4, 1:3}        | yes -> 2 |

Time: O(n). Space: O(k) where k is the number of distinct elements.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Majority Element (LeetCode 169) | https://leetcode.com/problems/majority-element/ |
| Medium | Top K Frequent Elements (LeetCode 347) | https://leetcode.com/problems/top-k-frequent-elements/ |
| Hard | Substring with Concatenation of All Words (LeetCode 30) | https://leetcode.com/problems/substring-with-concatenation-of-all-words/ |
