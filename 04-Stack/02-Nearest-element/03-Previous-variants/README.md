# Previous greater / previous smaller (mirror variants)

## What is this

For every index `i`, find the **first index `j < i` such that `nums[j] > nums[i]`** (previous greater) or `nums[j] < nums[i]` (previous smaller). Two equivalent implementations exist:

1. **Right-to-left scan** with a stack — symmetric mirror of "next greater/smaller".
2. **Left-to-right scan** where the stack itself acts as a record of all candidates so far; after popping out everything that wouldn't satisfy the predicate, the *top of the stack* (if any) is the answer for the current index.

Both run in **O(n) amortised**. Choice depends on whether you can iterate backwards (sometimes the input is a stream).

## Why we use

- Solves "the nearest previous element with property P" in **O(n) total** — beating O(n²) linear scans per element.
- Frequently paired with "next greater/smaller" to bound the contribution range of each element (sum of subarray maxes/mins, largest rectangle in histogram).
- The left-to-right form is simpler to reason about in many cases: every time you push `i`, the new top-below-it is the previous-greater (or previous-smaller).

## How to implement

**Method A: left-to-right, query the stack as we go.**

```
stack = []                  # holds indices, values are strictly decreasing (for previous-greater)
prev_greater = [-1] * n
for i in 0..n-1:
    while stack and nums[stack[-1]] <= nums[i]:   # pop indices that can't be a "previous greater" anymore
        stack.pop()
    prev_greater[i] = stack[-1] if stack else -1
    stack.append(i)
return prev_greater
```

**Method B: right-to-left, mirror of next-greater.**

```
stack = []                  # values strictly decreasing
prev_greater = [-1] * n
for i in n-1..0:
    while stack and nums[stack[-1]] < nums[i]:    # those still hunting a "previous greater" find one at i
        prev_greater[stack.pop()] = i
    stack.append(i)
return prev_greater
```

Python — previous smaller (Method A):

```python
def previous_smaller(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n
    stack: list[int] = []   # values strictly increasing
    for i in range(n):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        res[i] = stack[-1] if stack else -1
        stack.append(i)
    return res
```

JavaScript — previous greater (Method B, right-to-left):

```javascript
function previousGreater(nums) {
  const n = nums.length;
  const res = Array(n).fill(-1);
  const stack = [];
  for (let i = n - 1; i >= 0; i--) {
    while (stack.length && nums[stack[stack.length - 1]] < nums[i]) {
      res[stack.pop()] = i;
    }
    stack.push(i);
  }
  return res;
}
```

Invariant (Method A for previous-greater): after popping, every index left in the stack has a value `> nums[i]`. The top is therefore the **nearest** such index — exactly the previous greater.

## Which problems this approach solves in the real world

- **Histogram / skyline**: each bar's left bound is the previous-smaller index → forms the rectangle width.
- **Stock charts**: bars since the last higher high or lower low.
- **System metrics**: latency in milliseconds since the last spike that exceeded current sample.
- **Sensor diagnostics**: distance back to the last reading lower than current.
- **Compiler dominance analysis**: for each instruction, last earlier instruction with greater scope depth.
- **Geometry**: convex-hull-like sweeps where we need the last point that dominated.

## Pros and cons

**Pros**
- O(n) amortised total time, O(n) space.
- Two formulations let you choose based on iteration direction needed.
- The left-to-right form integrates directly into other left-to-right passes — useful in DP-on-arrays.
- Symmetric to next-greater/smaller; flipping comparison + direction covers all four "nearest" variants with the same skeleton.

**Cons**
- Pick wrong strict/weak comparison and the answer is silently off by one in duplicates.
- Method A's "stack top after pops" pattern is non-obvious until you've seen it once.
- Easy to confuse Method A (we record an answer for the *current* `i` using the *stack top*) with Method B (we record an answer for the *popped index* using the *current* `i`).

## Limitations

- Returns only the *single* nearest previous element; "k-th previous greater" needs different structures.
- For windowed variants ("previous greater within window of size W"), pair with index-based eviction (monotonic deque).
- In strictly online streams where you only see values from the right, you can't do Method B without buffering.

## One example

**Problem**: Given a list of bar heights, for each bar return the **distance to the nearest previous bar that is taller than it**, or `-1` if no such bar exists.
Constraints: `1 ≤ n ≤ 10^5`, `0 ≤ heights[i] ≤ 10^9`.

**Input**: `heights = [2, 1, 5, 6, 2, 3]`
**Output**: `[-1, 0, -1, -1, 0, 1]` (distance: index − previous_greater_index; `-1` if none).

## Solution explanation

```python
def distance_to_previous_taller(heights: list[int]) -> list[int]:
    n = len(heights)
    res = [-1] * n
    stack: list[int] = []   # values strictly decreasing
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] <= h:
            stack.pop()
        if stack:
            res[i] = i - stack[-1] - 1   # bars between (exclusive)
        stack.append(i)
    return res
```

(Alternative formulation: distance = `i - stack[-1]` if you want "i minus index of previous taller", inclusive of step. The problem statement above uses *bars between*, so we subtract 1.)

Walk-through on `[2, 1, 5, 6, 2, 3]`:

| i | h | pops while heights[top]≤h | stack indices (top→bot) | res[i] computation                | res so far                    |
|---|---|----------------------------|--------------------------|-----------------------------------|--------------------------------|
| 0 | 2 | —                          | [0]                      | empty → -1                        | [-1,?,?,?,?,?]                 |
| 1 | 1 | —                          | [1, 0]                   | top=0 → 1 - 0 - 1 = 0             | [-1, 0, ?,?,?,?]               |
| 2 | 5 | pop 1 (1≤5), pop 0 (2≤5)   | [2]                      | empty → -1                        | [-1, 0, -1, ?,?,?]             |
| 3 | 6 | pop 2 (5≤6)                | [3]                      | empty → -1                        | [-1, 0, -1, -1, ?,?]           |
| 4 | 2 | —                          | [4, 3]                   | top=3 → 4 - 3 - 1 = 0             | [-1, 0, -1, -1, 0, ?]          |
| 5 | 3 | pop 4 (2≤3)                | [5, 3]                   | top=3 → 5 - 3 - 1 = 1             | [-1, 0, -1, -1, 0, 1]          |

Final answer: `[-1, 0, -1, -1, 0, 1]`.

Correctness: while popping, we remove every stacked index whose value is ≤ `h` — those can never be a *strictly greater* predecessor for `i` or any future index ≤ `h`. What's left is, by construction, an index with value `> h`, and it is the most-recently-pushed such index, i.e. the nearest previous greater.

- **Time**: O(n) — each index is pushed once and popped at most once.
- **Space**: O(n) for the stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Online Stock Span** — count consecutive previous days with price ≤ today; classic "previous greater" with span counting. | https://leetcode.com/problems/online-stock-span/ |
| Medium | **Sum of Subarray Minimums** — uses previous-smaller + next-smaller to compute each value's contribution as a window minimum. | https://leetcode.com/problems/sum-of-subarray-minimums/ |
| Hard | **Largest Rectangle in Histogram** — pair previous-smaller and next-smaller to find each bar's maximal-rectangle width in O(n). | https://leetcode.com/problems/largest-rectangle-in-histogram/ |
