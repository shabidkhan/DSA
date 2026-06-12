# Monotonic increasing stack

## What is this

A stack whose elements (or indices into an array) are kept in **strictly (or weakly) increasing order from bottom to top**. Before pushing a new value `x`, we pop every top element that is greater than (or equal to) `x`. The invariant guarantees that for any index inside the stack, every index after it that has been processed is **larger or equal** — which is exactly the information needed to answer "next smaller element", "rectangle bounded by smaller heights", and similar queries.

## Why we use

- Lets us answer "the nearest element to the right (or left) that is smaller than the current" in **O(n) total** rather than O(n²).
- Each element is pushed and popped at most once → amortised O(1) per element.
- The stack itself acts as a compact data structure encoding "candidates whose answer hasn't been finalised yet".
- It generalises to a huge family of problems: largest rectangle in histogram, daily temperatures (mirror), sum of subarray minimums, etc.

## How to implement

```
stack = []   # stores indices, values nums[stack] are strictly increasing
for i in 0..n-1:
    while stack and nums[stack[-1]] > nums[i]:
        top = stack.pop()
        # at this moment, i is the "next smaller" of top
        # nums[stack[-1]] (if any) is the "previous smaller" of top
    stack.append(i)
# remaining indices have no next-smaller — their "next smaller" is n (sentinel)
```

Python — "next smaller element" for every index:

```python
def next_smaller(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [n] * n            # default: no smaller to the right → n
    stack: list[int] = []    # values are strictly increasing in stack order
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            res[stack.pop()] = i
        stack.append(i)
    return res
```

JavaScript — same algorithm:

```javascript
function nextSmaller(nums) {
  const n = nums.length;
  const res = Array(n).fill(n);
  const stack = [];
  for (let i = 0; i < n; i++) {
    while (stack.length && nums[stack[stack.length - 1]] > nums[i]) {
      res[stack.pop()] = i;
    }
    stack.push(i);
  }
  return res;
}
```

Invariant: at any point, the values at the indices in `stack` are strictly increasing from bottom to top. The top of the stack always represents the **smallest right-most unresolved value** seen so far.

## Which problems this approach solves in the real world

- **Stock spans / financial analytics**: number of consecutive prior days where price was lower.
- **Histogram skyline analysis**: largest contiguous rectangle that fits under a sequence of bars.
- **Temperature / weather APIs**: days until a colder day appears (cold-streak detection).
- **Memory profiling**: longest range where allocation size stayed under a threshold.
- **Compiler scheduling**: nearest preceding instruction with smaller latency.
- **Audio processing**: nearest preceding sample lower than the current — used in envelope detection.

## Pros and cons

**Pros**
- O(n) amortised — every element enters and leaves at most once.
- O(n) space worst-case; often much smaller in practice.
- Simple control flow once the invariant is internalised.
- Mirror-symmetric: reverse iteration gives "previous smaller" with the same code.

**Cons**
- Easy to confuse strict vs. weak comparisons (`>` vs `>=`); the choice depends on whether duplicates should be treated as "smaller".
- Off-by-one bugs at the sentinel end (n vs n-1, or -1).
- Stores **indices, not values** in most variants, which can trip up first-time implementers.

## Limitations

- Only applies when the answer depends on the "next/previous smaller/greater" relation — which is monotone.
- Doesn't generalise to "k-th smaller to the right" — that's a different problem (Fenwick / wavelet tree).
- For 2D problems you'd run this row-wise then column-wise; pure 2D extensions don't exist out of the box.
- Real-time streams must accept that an element's answer may resolve much later (when something smaller arrives).

## One example

**Problem**: Given a list of daily stock prices `prices`, for each day return the number of consecutive days *immediately before* the current day where the price was **less than or equal to** the current price (this is the **Online Stock Span**).
Constraints: `1 ≤ n ≤ 10^4`, `1 ≤ prices[i] ≤ 10^5`.

**Input**: `prices = [100, 80, 60, 70, 60, 75, 85]`
**Output**: `[1, 1, 1, 2, 1, 4, 6]`

## Solution explanation

We keep a monotonic decreasing stack of `(price, span)` pairs (i.e. **values strictly decreasing top→bottom from the front, but we treat it as "increasing pops" for clarity**). For each new price, pop while the top's price ≤ current, summing their spans:

```python
def stock_spans(prices: list[int]) -> list[int]:
    stack: list[tuple[int, int]] = []  # (price, span)
    out = []
    for p in prices:
        span = 1
        while stack and stack[-1][0] <= p:
            span += stack.pop()[1]
        stack.append((p, span))
        out.append(span)
    return out
```

Walk-through on `[100, 80, 60, 70, 60, 75, 85]`:

| i | price | pops                         | new span | stack (price, span)                                |
|---|-------|------------------------------|----------|----------------------------------------------------|
| 0 | 100   | —                            | 1        | [(100,1)]                                          |
| 1 | 80    | —                            | 1        | [(100,1), (80,1)]                                  |
| 2 | 60    | —                            | 1        | [(100,1), (80,1), (60,1)]                          |
| 3 | 70    | pop (60,1)                   | 1+1 = 2  | [(100,1), (80,1), (70,2)]                          |
| 4 | 60    | —                            | 1        | [(100,1), (80,1), (70,2), (60,1)]                  |
| 5 | 75    | pop (60,1), (70,2)           | 1+1+2=4  | [(100,1), (80,1), (75,4)]                          |
| 6 | 85    | pop (75,4), (80,1)           | 1+4+1=6  | [(100,1), (85,6)]                                  |

Final answer: `[1, 1, 1, 2, 1, 4, 6]`.

Correctness: an earlier day's span is "absorbed" by a later day if and only if the later price is ≥ the earlier price — the earlier day can never *itself* extend a future span beyond that point, so we can compress it into the later entry. The stack carries the maximal compressed history.

- **Time**: amortised O(n) — total pops ≤ total pushes = n.
- **Space**: O(n) worst-case (strictly decreasing sequence), O(1) best-case.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Final Prices With a Special Discount in a Shop** — for each item, find the next item with price ≤ current and subtract. Plain monotonic-stack drill. | https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/ |
| Medium | **Online Stock Span** — the canonical span problem, implemented as a streaming class. | https://leetcode.com/problems/online-stock-span/ |
| Hard | **Largest Rectangle in Histogram** — combines "previous smaller" + "next smaller" via one increasing stack to compute the max rectangle area. | https://leetcode.com/problems/largest-rectangle-in-histogram/ |
