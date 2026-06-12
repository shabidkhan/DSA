# Next greater element

## What is this

For every index `i` of an array, find the **first index `j > i` such that `nums[j] > nums[i]`** (or return a sentinel like `-1` if none exists). The standard tool is a **monotonic decreasing stack** that walks left-to-right: when `nums[i]` is larger than the element at the stack's top, that top's "next greater" has just been found, so we pop and record. The unresolved indices stay stacked, waiting for a larger value to come along.

## Why we use

- Computes the next-greater answer for **every index in O(n) total** — beating the naive O(n²) double loop.
- Each index is pushed and popped at most once → amortised O(1) per index.
- Generalises to "next greater frequency", "next greater that satisfies condition P", and works on circular arrays with a small tweak (iterate `2n` indices modulo `n`).
- It's the foundational primitive behind histogram, span, and many DP-on-arrays problems.

## How to implement

```
stack = []                # holds indices waiting for their next-greater
res   = [-1] * n          # default: no greater
for i in 0..n-1:
    while stack and nums[stack[-1]] < nums[i]:
        j = stack.pop()
        res[j] = nums[i]    # or i, depending on what is asked
    stack.append(i)
return res
```

Python — return values of next-greater:

```python
def next_greater_element(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n
    stack: list[int] = []
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            res[stack.pop()] = nums[i]
        stack.append(i)
    return res
```

JavaScript — circular variant:

```javascript
function nextGreaterCircular(nums) {
  const n = nums.length;
  const res = Array(n).fill(-1);
  const stack = [];
  for (let i = 0; i < 2 * n; i++) {
    const x = nums[i % n];
    while (stack.length && nums[stack[stack.length - 1]] < x) {
      res[stack.pop()] = x;
    }
    if (i < n) stack.push(i);   // only push original indices
  }
  return res;
}
```

Invariant: indices in `stack` correspond to values that are **strictly decreasing** from bottom to top. Anything popped has been resolved.

## Which problems this approach solves in the real world

- **Trading / technical analysis**: bars until the next higher high — used in breakout strategies.
- **Operating systems**: time until the next CPU spike higher than the current sample.
- **Audio**: index of the next sample with higher amplitude — used in onset detection.
- **Game engines**: frame until the next frame-time spike — flag stutters.
- **DevOps SLO monitoring**: minutes until next request rate higher than current.
- **Compilers**: nearest later instruction with greater priority for scheduling.

## Pros and cons

**Pros**
- O(n) amortised total.
- O(n) extra space for the stack and result.
- Mirror-symmetric: scan right-to-left to get "previous greater".
- Works on streams with a slight rephrasing (online stock span is the streaming form).

**Cons**
- Strict vs. weak inequality must match the problem (`>` vs `>=`).
- Off-by-one in the sentinel choice (`-1` vs `n` vs `+inf`) is easy to get wrong if the downstream uses the result as a distance vs. value.
- Doesn't naturally extend to "k-th next greater"; for that, use a sorted multiset or a Fenwick tree.

## Limitations

- Only one greater is returned; "all greater" or "k-th greater" needs richer structures.
- For 2D matrices, you must apply row-wise / column-wise — there is no pure 2D version.
- In a circular array, the simple two-pass trick works only because `n` is finite; for infinite streams the question is ill-defined.
- Negative or non-numeric data is fine, but you must define a comparator carefully (e.g. lex order for strings).

## One example

**Problem**: You are given two distinct integer arrays `nums1` and `nums2` where `nums1` is a subset of `nums2`. For each `x` in `nums1`, find the **next greater element** of `x` in `nums2`. If it doesn't exist, output `-1` for that query.
Constraints: `1 ≤ nums1.length ≤ nums2.length ≤ 1000`, all elements unique.

**Input**: `nums1 = [4, 1, 2]`, `nums2 = [1, 3, 4, 2]`
**Output**: `[-1, 3, -1]`

## Solution explanation

Precompute the next greater for every value in `nums2` (linear time), then look up each query:

```python
def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    nge: dict[int, int] = {}
    stack: list[int] = []
    for x in nums2:
        while stack and stack[-1] < x:
            nge[stack.pop()] = x
        stack.append(x)
    # values still on the stack have no greater → default -1
    return [nge.get(q, -1) for q in nums1]
```

Walk-through on `nums2 = [1, 3, 4, 2]`:

| i | x | pops (resolved → x)         | stack (top→bot) | nge so far                |
|---|---|------------------------------|-----------------|----------------------------|
| 0 | 1 | —                            | [1]             | {}                         |
| 1 | 3 | pop 1 (1<3) → nge[1]=3       | [3]             | {1:3}                      |
| 2 | 4 | pop 3 (3<4) → nge[3]=4       | [4]             | {1:3, 3:4}                 |
| 3 | 2 | —                            | [4, 2]          | {1:3, 3:4}                 |

Leftovers `{4, 2}` have no next greater. Looking up `[4, 1, 2]` gives `[-1, 3, -1]`.

Correctness: when processing `x`, any stacked value `< x` has its next-greater answer fixed to `x` — because everything between it and `x` is even smaller (otherwise it would have been popped earlier). Anything `≥ x` stays on the stack, still hunting for something strictly larger.

- **Time**: O(|nums2|) for the precomputation, O(|nums1|) for the queries — overall O(n2 + n1).
- **Space**: O(|nums2|) for the map and the stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Next Greater Element I** — exactly the problem above; basic mapping + stack. | https://leetcode.com/problems/next-greater-element-i/ |
| Medium | **Next Greater Element II** — circular array; iterate `2n` times modulo `n`. | https://leetcode.com/problems/next-greater-element-ii/ |
| Hard | **Next Greater Node In Linked List** — convert list to array, then apply the same stack idea; or do it in one pass over the list. | https://leetcode.com/problems/next-greater-node-in-linked-list/ |
