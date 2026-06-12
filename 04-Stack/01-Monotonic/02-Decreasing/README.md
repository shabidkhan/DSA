# Monotonic decreasing stack

## What is this

A stack whose elements (or indices into an array) are kept in **strictly (or weakly) decreasing order from bottom to top**. Before pushing a new value `x`, we pop every top element that is less than (or equal to) `x`. The invariant guarantees that for any index inside the stack, every index after it that has been processed is **smaller** — which is exactly the information needed to answer "next greater element", "daily temperatures" (days until warmer), and similar queries.

## Why we use

- Computes "the nearest element to the right (or left) that is **larger** than the current" in **O(n) total** across all queries.
- Each element is pushed and popped at most once → amortised O(1) per element.
- Mirrors the increasing-stack pattern, so once you know one, the other is "flip the comparison".
- Used as a building block in problems involving maxima: next-greater, daily temperatures, sum of subarray maximums.

## How to implement

```
stack = []   # stores indices, values nums[stack] are strictly decreasing
for i in 0..n-1:
    while stack and nums[stack[-1]] < nums[i]:
        top = stack.pop()
        # at this moment, i is the "next greater" of top
    stack.append(i)
# remaining indices have no next-greater (or use a sentinel, e.g. -1)
```

Python — "next greater element" for every index:

```python
def next_greater(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n             # default: no greater to the right
    stack: list[int] = []      # values strictly decreasing
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            res[stack.pop()] = nums[i]
        stack.append(i)
    return res
```

JavaScript:

```javascript
function nextGreater(nums) {
  const n = nums.length;
  const res = Array(n).fill(-1);
  const stack = [];
  for (let i = 0; i < n; i++) {
    while (stack.length && nums[stack[stack.length - 1]] < nums[i]) {
      res[stack.pop()] = nums[i];
    }
    stack.push(i);
  }
  return res;
}
```

Invariant: at any point, values at indices in `stack` are strictly decreasing from bottom to top. The top represents the **largest right-most unresolved value** so far.

## Which problems this approach solves in the real world

- **Daily temperatures**: days until a warmer day for each day in a series.
- **Traffic analytics**: time until the next request burst higher than the current.
- **Hardware monitoring**: time until a CPU temperature exceeds the current sample.
- **Audio peak detection**: distance to the next sample with higher amplitude.
- **Compiler / scheduler**: nearest later instruction with a higher priority.
- **Trading**: bars until the next higher high — used in technical-analysis indicators.

## Pros and cons

**Pros**
- O(n) amortised — every element enters and leaves at most once.
- O(n) space worst-case (already-decreasing input).
- Mirror of the increasing-stack pattern; flipping the comparison switches between min and max.
- Combines well with circular-array tricks (process the array twice modulo n) to handle "next greater in circular array".

**Cons**
- Strict vs. weak comparison choice has the same trap as the increasing variant — pick deliberately based on duplicate semantics.
- Some problems want the *value* of the next greater, others want the *index*, others the *distance*; pick correctly when writing the output line.
- Edge case: when no greater exists, you must record a sentinel (-1, n, or +inf) so downstream code doesn't crash.

## Limitations

- Only applies when "next/previous greater" is the natural query.
- "k-th greater to the right" is **not** solvable with a single monotonic stack.
- For 2D problems, you typically run the 1D version row-wise or column-wise — there is no pure 2D monotonic-stack.
- In a streaming setting, individual answers may resolve much later (only when a larger value finally arrives).

## One example

**Problem**: Given an array `temperatures` of daily temperatures, return an array `answer` such that `answer[i]` is the **number of days until a warmer temperature**. If there is no future warmer day, set `answer[i] = 0`.
Constraints: `1 ≤ n ≤ 10^5`, `30 ≤ temperatures[i] ≤ 100`.

**Input**: `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`
**Output**: `[1, 1, 4, 2, 1, 1, 0, 0]`

## Solution explanation

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    answer = [0] * n
    stack: list[int] = []   # indices; temperatures[stack] strictly decreasing
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer
```

Walk-through on `[73, 74, 75, 71, 69, 72, 76, 73]`:

| i | t  | pops (idx → resolved) | stack indices (top → bot) | answer so far                         |
|---|----|-----------------------|----------------------------|----------------------------------------|
| 0 | 73 | —                     | [0]                        | [0,0,0,0,0,0,0,0]                      |
| 1 | 74 | pop 0 → answer[0]=1   | [1]                        | [1,0,0,0,0,0,0,0]                      |
| 2 | 75 | pop 1 → answer[1]=1   | [2]                        | [1,1,0,0,0,0,0,0]                      |
| 3 | 71 | —                     | [2,3]                      | [1,1,0,0,0,0,0,0]                      |
| 4 | 69 | —                     | [2,3,4]                    | [1,1,0,0,0,0,0,0]                      |
| 5 | 72 | pop 4 (69<72) → ans[4]=1; pop 3 (71<72) → ans[3]=2 | [2,5] | [1,1,0,2,1,0,0,0]                 |
| 6 | 76 | pop 5 → ans[5]=1; pop 2 → ans[2]=4 | [6]              | [1,1,4,2,1,1,0,0]                      |
| 7 | 73 | —                     | [6,7]                      | [1,1,4,2,1,1,0,0]                      |

Indices 6 and 7 remain on the stack with `answer = 0` (no future warmer day).

Correctness: when we encounter `t = temperatures[i]`, any earlier index `j` with `temperatures[j] < t` has its "next warmer" resolved as `i` — we record `i - j` and pop. Any earlier index with `temperatures[j] ≥ t` is still waiting for something strictly larger, so we leave it on the stack. The stack stays strictly decreasing because we only stop popping once the top is `≥ t`.

- **Time**: O(n) — each index is pushed once and popped at most once.
- **Space**: O(n) worst-case.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Next Greater Element I** — for each element of `nums1`, find the next greater in `nums2`. Direct application of decreasing stack on `nums2`. | https://leetcode.com/problems/next-greater-element-i/ |
| Medium | **Daily Temperatures** — the canonical problem this pattern solves. | https://leetcode.com/problems/daily-temperatures/ |
| Hard | **Next Greater Element II** — same problem on a *circular* array; process the array twice modulo n. | https://leetcode.com/problems/next-greater-element-ii/ |
