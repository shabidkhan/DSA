# Same-direction two pointers

## What is this

A two-pointer technique where **both pointers move forward** (left-to-right) over an array, but advance under **different rules**. Unlike fast/slow (where one is always one step ahead per iteration), here the relative motion depends on what's at each pointer: one might wait while the other advances until some condition is satisfied. It's the underlying pattern for sliding windows, merging two sorted streams, and "partition into buckets" style problems.

## Why we use

- Solves "match / merge / partition" problems in O(n) or O(n + m) by exploiting an ordering or monotonicity in the data.
- Avoids nested loops: where a naïve approach would re-scan from the start, the second pointer remembers progress.
- Composes naturally with sliding-window thinking (sliding windows are themselves a special case).

## How to implement

```
i, j = 0, 0
while i < n and j < m:
    if condition(a[i], b[j]):
        record / action
        i += 1
    else:
        j += 1
# possibly continue draining the remaining pointer
```

Python — intersection of two sorted arrays (with duplicates):

```python
def intersection_sorted(a: list[int], b: list[int]) -> list[int]:
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return out
```

Python — is `s` a subsequence of `t`:

```python
def is_subsequence(s: str, t: str) -> bool:
    i = j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)
```

Invariant: each pointer **never moves backward**. Whatever portion of each array is "behind" the corresponding pointer has been fully processed and will not be revisited. Termination is guaranteed because at least one pointer advances per iteration.

## Which problems this approach solves in the real world

- **Merging two sorted lists** of records (e.g. two sorted log files into one sorted output).
- **Deduplicating / set operations on sorted streams** (intersection, union, difference) without loading both fully into a hash set.
- **Subsequence matching**: checking whether a user's typed prefix is consistent with a target command.
- **Multi-cursor synchronisation**: aligning two streams of timestamped events where one drives the other.
- **String matching with skips**: comparing a pattern against a target where some characters are wildcards.

## Pros and cons

**Pros**
- O(n + m) time when the inputs are sorted or otherwise monotonically aligned.
- O(1) extra space.
- Streaming-friendly: only forward access required.
- Easy to reason about — each step advances at least one pointer.

**Cons**
- Inputs typically need a pre-existing ordering (sorted, or alignable). Sorting first costs O(n log n).
- Easy to write a subtly wrong advancement rule (e.g. advancing both pointers when only one should advance) and silently get the wrong answer.
- Doesn't extend to "k pointers in different rates" without additional machinery (often a heap is better).

## Limitations

- For arrays without a useful ordering, this pattern doesn't help — use hash maps or sorting first.
- Can't seek backwards, so it doesn't fit problems requiring random access (e.g. finding a pair where one is much earlier than the other).
- For k > 2 streams to merge, a min-heap (k-way merge) is the canonical extension, not k same-direction pointers.

## One example

**Problem**: Given two strings `s` and `t`, return `true` if `s` is a **subsequence** of `t` (i.e. `s` can be obtained from `t` by deleting some characters without changing the order of the remaining characters). Constraints: `0 ≤ s.length ≤ 100`, `0 ≤ t.length ≤ 10^4`.

**Input**: `s = "abc"`, `t = "ahbgdc"`
**Output**: `true`

## Solution explanation

```python
def is_subsequence(s: str, t: str) -> bool:
    i = j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)
```

Walk-through on `s = "abc"`, `t = "ahbgdc"`:

| step | i | j | s[i] | t[j] | match? | action                  |
|------|---|---|------|------|--------|-------------------------|
| 0    | 0 | 0 | a    | a    | yes    | i=1, j=1                |
| 1    | 1 | 1 | b    | h    | no     | j=2                     |
| 2    | 1 | 2 | b    | b    | yes    | i=2, j=3                |
| 3    | 2 | 3 | c    | g    | no     | j=4                     |
| 4    | 2 | 4 | c    | d    | no     | j=5                     |
| 5    | 2 | 5 | c    | c    | yes    | i=3, j=6                |
| end  | 3 | 6 |      |      |        | i == len(s) → **true**  |

`j` advances every iteration (consuming `t`), while `i` only advances when `s[i]` is matched. The decision is locally greedy — take the **earliest** match in `t` for each character of `s`. Correctness: any subsequence proof can be transformed to also take the earliest match without losing validity, so the greedy choice is safe.

- **Time**: O(n + m).
- **Space**: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Is Subsequence** — check if `s` is a subsequence of `t`. | https://leetcode.com/problems/is-subsequence/ |
| Medium | **Intersection of Two Arrays II** — return the intersection with multiplicities (sort + two pointers). | https://leetcode.com/problems/intersection-of-two-arrays-ii/ |
| Hard   | **Smallest Range Covering Elements from K Lists** — generalises to k same-direction pointers + min-heap. | https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/ |
