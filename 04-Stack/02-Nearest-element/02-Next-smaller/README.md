# Next smaller element

## What is this

For every index `i`, find the **first index `j > i` such that `nums[j] < nums[i]`** (or a sentinel like `n` or `-1` if none exists). The natural tool is a **monotonic increasing stack** walked left-to-right: when `nums[i]` is smaller than the stack's top, that top's "next smaller" has just been found, so we pop and record.

The mirror of "next greater". Same algorithm, comparison flipped.

## Why we use

- Resolves all next-smaller queries in **O(n) total** — better than the naive O(n²) loop.
- Each index is pushed once and popped at most once → amortised O(1).
- Essential primitive for "largest rectangle in histogram" (with previous-smaller, you bound each bar's max rectangle in O(n)), "sum of subarray minimums", and similar.
- Mirror symmetric: scanning right-to-left gives "previous smaller".

## How to implement

```
stack = []                # holds indices waiting for their next-smaller
res   = [n] * n           # default: no smaller → sentinel n (or -1)
for i in 0..n-1:
    while stack and nums[stack[-1]] > nums[i]:
        j = stack.pop()
        res[j] = i        # or nums[i], depending on what we want
    stack.append(i)
return res
```

Python — return the **index** of the next smaller (sentinel `n`):

```python
def next_smaller_index(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [n] * n
    stack: list[int] = []   # values are strictly increasing
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            res[stack.pop()] = i
        stack.append(i)
    return res
```

JavaScript — return the **value** of the next smaller (sentinel `-1`):

```javascript
function nextSmallerValue(nums) {
  const n = nums.length;
  const res = Array(n).fill(-1);
  const stack = [];
  for (let i = 0; i < n; i++) {
    while (stack.length && nums[stack[stack.length - 1]] > nums[i]) {
      res[stack.pop()] = nums[i];
    }
    stack.push(i);
  }
  return res;
}
```

Invariant: values at indices in `stack` are **strictly increasing** from bottom to top.

## Which problems this approach solves in the real world

- **Histogram analysis / Skyline**: bounds for each bar's maximal-fit rectangle.
- **Stock market**: bars until the next lower low — used in trend-reversal logic.
- **Climate data**: time until next colder reading after a warm spell.
- **Pressure / queue load monitoring**: time until backlog drops below current.
- **Compiler / register allocator**: nearest later instruction with lower live count.
- **Genomics**: nearest later position with lower coverage depth.

## Pros and cons

**Pros**
- O(n) amortised total — fast enough for 10⁶+ inputs.
- O(n) space, often less in practice.
- Mirror of "next greater"; trivially reversible to "previous smaller".
- Combines beautifully with "previous smaller" to compute "sum/max over all subarrays" problems in O(n).

**Cons**
- Strict vs. weak inequality must match the problem semantics. `> vs >=` decides whether equal values count.
- Sentinel choice (`n` vs `-1`) must match how downstream code uses the result.
- The mental model "values increase in the stack" is the opposite of "next greater" — flipping in your head is the easiest place to bug out.

## Limitations

- Returns only the *first* smaller; for "k-th smaller to the right" use other structures (segment tree, wavelet).
- Can't answer "smaller within a window of size W" directly; use a monotonic deque with eviction by index.
- In streaming/online mode, an index's answer can remain unresolved indefinitely.
- For 2D, you'd run row-wise / column-wise; no native 2D form.

## One example

**Problem**: Given an integer array `nums`, return for each index `i` the **length of the longest contiguous subarray starting at `i`** such that every element is ≥ `nums[i]`. Equivalently, this equals `(j - i)` where `j` is the next index whose value is strictly less than `nums[i]` (or `n` if no such index).
Constraints: `1 ≤ n ≤ 10^5`, `-10^9 ≤ nums[i] ≤ 10^9`.

**Input**: `nums = [3, 1, 4, 1, 5, 9, 2, 6]`
**Output**: `[1, 2, 1, 4, 3, 2, 1, 1]`

## Solution explanation

We compute next-smaller indices; the answer is `next_smaller_index[i] - i`:

```python
def longest_ge_run(nums: list[int]) -> list[int]:
    n = len(nums)
    nsi = [n] * n
    stack: list[int] = []
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            nsi[stack.pop()] = i
        stack.append(i)
    return [nsi[i] - i for i in range(n)]
```

Walk-through on `[3, 1, 4, 1, 5, 9, 2, 6]` (n=8):

| i | x | pops (resolved → i)              | stack (top → bot) | nsi so far                  |
|---|---|-----------------------------------|--------------------|------------------------------|
| 0 | 3 | —                                 | [0]               | [8,8,8,8,8,8,8,8]            |
| 1 | 1 | pop 0 (3>1) → nsi[0]=1            | [1]               | [1,8,8,8,8,8,8,8]            |
| 2 | 4 | —                                 | [1,2]             | [1,8,8,8,8,8,8,8]            |
| 3 | 1 | pop 2 (4>1) → nsi[2]=3            | [1,3]             | [1,8,3,8,8,8,8,8]            |
| 4 | 5 | —                                 | [1,3,4]           | [1,8,3,8,8,8,8,8]            |
| 5 | 9 | —                                 | [1,3,4,5]         | [1,8,3,8,8,8,8,8]            |
| 6 | 2 | pop 5 (9>2) → nsi[5]=6; pop 4 (5>2) → nsi[4]=6 | [1,3,6]    | [1,8,3,8,6,6,8,8]            |
| 7 | 6 | —                                 | [1,3,6,7]         | [1,8,3,8,6,6,8,8]            |

Leftovers `{1, 3, 6, 7}` have no next-smaller → keep sentinel `8`.

Final `nsi = [1, 8, 3, 8, 6, 6, 8, 8]`.
Answer: `[1-0, 8-1, 3-2, 8-3, 6-4, 6-5, 8-6, 8-7] = [1, 7, 1, 5, 2, 1, 2, 1]`.

(Hmm, double-check the desired output against the example: the example output above assumes a slightly different problem formulation. Re-examining: indeed for `nums = [3,1,4,1,5,9,2,6]`, the longest run at index 1 starting with value 1 with all values ≥ 1 goes through positions 1–7 — length 7. So the correct output is `[1, 7, 1, 5, 2, 1, 2, 1]`. The earlier example output was misstated; the algorithm yields the verified table above.)

Correctness: every time we see `x = nums[i]`, indices on the stack with strictly larger values have their next-smaller finally found at `i`. We pop them, record `nsi[j] = i`, and stop when the top is ≤ `x` (so `x` is not smaller than it). The stack stays strictly increasing.

- **Time**: O(n) — pushes + pops bounded by 2n.
- **Space**: O(n) for stack + result.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Final Prices With a Special Discount in a Shop** — for each item, subtract the next item's price if smaller. Direct application. | https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/ |
| Medium | **Sum of Subarray Minimums** — combine next-smaller + previous-smaller to compute each element's contribution as a window minimum. | https://leetcode.com/problems/sum-of-subarray-minimums/ |
| Hard | **Largest Rectangle in Histogram** — pair previous-smaller and next-smaller to bound the maximal rectangle for each bar. | https://leetcode.com/problems/largest-rectangle-in-histogram/ |
