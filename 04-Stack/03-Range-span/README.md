# Range / span (stack-based)

## What is this

A family of stack-based techniques where each value's contribution to the answer is a **range or span** — typically "how many earlier (or later) elements does it dominate?" or "what is the contiguous range where it is the maximum/minimum?". A monotonic stack compresses these ranges in O(n) total instead of recomputing them naively.

Two canonical examples:
- **Stock Span**: for each day, count the consecutive previous days with price ≤ today.
- **Sum of Subarray Ranges / Sum of Subarray Minimums**: for each element, multiply by the number of subarrays in which it is the minimum (or maximum).

The trick: when you pop an element, the popped element's span (length of its left side) is fully known.

## Why we use

- Computes O(n) ranges in **linear total time**, replacing O(n²) double scans.
- Allows "contribution of each element to a global sum" to be computed in one sweep: each element contributes `count_of_subarrays_where_it_is_extreme × its_value`.
- The stack acts as a *streaming* data structure — span problems can be answered online as data arrives.
- Reduces complex DP-on-arrays formulations to a simple stack pass.

## How to implement

**Stock Span (left-side span):**
```
stack = []   # holds (price, span)
for each new price p:
    span = 1
    while stack and stack.top.price <= p:
        span += stack.pop().span
    stack.push((p, span))
    output span
```

**Sum of Subarray Minimums (left + right span per element):**
```
for each index i:
    L[i] = i - prev_less_or_equal[i]          # distance to previous index with value < nums[i] (strict)
    R[i] = next_less[i] - i                   # distance to next index with value <= nums[i] (weak, to avoid double counting equal values)
total = sum(nums[i] * L[i] * R[i] for i in 0..n-1)
```

Python — Online Stock Span:

```python
class StockSpanner:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []   # (price, span)

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
```

JavaScript — Sum of Subarray Minimums:

```javascript
function sumSubarrayMins(arr) {
  const MOD = 1_000_000_007n;
  const n = arr.length;
  const prev = Array(n).fill(-1);
  const next = Array(n).fill(n);
  const stack = [];
  for (let i = 0; i < n; i++) {
    while (stack.length && arr[stack[stack.length - 1]] >= arr[i]) stack.pop();
    prev[i] = stack.length ? stack[stack.length - 1] : -1;
    stack.push(i);
  }
  stack.length = 0;
  for (let i = n - 1; i >= 0; i--) {
    while (stack.length && arr[stack[stack.length - 1]] > arr[i]) stack.pop();
    next[i] = stack.length ? stack[stack.length - 1] : n;
    stack.push(i);
  }
  let total = 0n;
  for (let i = 0; i < n; i++) {
    const L = BigInt(i - prev[i]);
    const R = BigInt(next[i] - i);
    total = (total + BigInt(arr[i]) * L * R) % MOD;
  }
  return Number(total);
}
```

Invariant: every popped element has its full span determined; nothing on the stack will ever "rewrite" it.

## Which problems this approach solves in the real world

- **Stock analysis**: number of consecutive prior days where price stayed under today's — a momentum measure.
- **Server load profiling**: longest preceding run of lower-load samples — used in scaling decisions.
- **Sensor calibration**: span of preceding readings under the new sample, useful for outlier weighting.
- **Game speedrunning leaderboards**: streak length of slower previous runs that the current run dominates.
- **Compiler optimisation**: span of preceding instructions with smaller register pressure.
- **Skyline / silhouette computation**: contributing range of each rectangle.

## Pros and cons

**Pros**
- O(n) amortised — both for offline and online (streaming) forms.
- O(n) extra memory for the stack — usually much smaller in practice.
- The "contribution per element" framing is conceptually clean and generalises to many sum-over-subarrays problems.
- Online stock span solves a streaming problem with O(1) amortised per `next()` call.

**Cons**
- Correctly handling **ties** is the trickiest part: for "sum of subarray minimums", you must use strict `<` on one side and `≤` on the other to count each subarray's minimum exactly once.
- Stack contents (compressed history) become harder to inspect/debug.
- For multi-dimensional spans (2D rectangles), you typically combine 1D span passes — possible but fiddly.

## Limitations

- Only works for spans defined by a monotone predicate.
- Can't answer "exact rank of element in span" — for that, you need a Fenwick or wavelet tree.
- Compressed spans lose individual identities — fine for sums and counts, not for listing.
- The streaming form requires O(n) worst-case memory; you cannot bound it to a small constant for arbitrary inputs.

## One example

**Problem**: Implement a class `StockSpanner` that has one method `next(price)`. For each call, it returns the **stock price span**, defined as the maximum number of consecutive days (ending today, going backwards) for which the price was less than or equal to today's price.
Constraints: `1 ≤ price ≤ 10^5`, up to `10^4` calls.

**Input**:
```
prices = [100, 80, 60, 70, 60, 75, 85]
```
**Output**:
```
[1, 1, 1, 2, 1, 4, 6]
```

## Solution explanation

```python
class StockSpanner:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []  # (price, span)

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
```

Walk-through (same as Stock Span analysis):

| day | price | pops               | new span | stack (price, span)                                |
|-----|-------|--------------------|----------|----------------------------------------------------|
| 0   | 100   | —                  | 1        | [(100,1)]                                          |
| 1   | 80    | —                  | 1        | [(100,1), (80,1)]                                  |
| 2   | 60    | —                  | 1        | [(100,1), (80,1), (60,1)]                          |
| 3   | 70    | pop (60,1)         | 1+1 = 2  | [(100,1), (80,1), (70,2)]                          |
| 4   | 60    | —                  | 1        | [(100,1), (80,1), (70,2), (60,1)]                  |
| 5   | 75    | pop (60,1), (70,2) | 1+1+2=4  | [(100,1), (80,1), (75,4)]                          |
| 6   | 85    | pop (75,4), (80,1) | 1+4+1=6  | [(100,1), (85,6)]                                  |

Output: `[1, 1, 1, 2, 1, 4, 6]`.

Correctness: by induction, when a stacked pair `(p', s')` is popped because `p' <= price`, the *entire span of s' days ending on that earlier day* has prices ≤ p' ≤ price, so they all qualify as part of today's span. We sum them into today's span and continue popping. We stop the moment the top's price exceeds today's, because that day breaks the run.

- **Time**: amortised O(1) per `next()` call (O(n) total over n calls).
- **Space**: O(n) worst-case (strictly decreasing input sequence keeps everything on the stack).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Number of Students Unable to Eat Lunch** — simple stack/queue interaction warm-up. | https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/ |
| Medium | **Online Stock Span** — the canonical span problem above. | https://leetcode.com/problems/online-stock-span/ |
| Hard | **Sum of Subarray Ranges** — for every subarray, compute (max − min); sum all. Use next-/previous-greater AND next-/previous-smaller to compute contributions. | https://leetcode.com/problems/sum-of-subarray-ranges/ |
