# Monotonic window (deque-based)

## What is this

A sliding-window technique where a **deque** (double-ended queue) holds candidate indices in monotonic order — increasing or decreasing in their array values. As the window moves right, indices whose values can never again be the window's maximum (or minimum) are popped from the back; indices that have slid out of the window are popped from the front. The front of the deque always holds the optimal element for the current window.

## How is this different from "expand-shrink"? Expand-shrink maintains a *single aggregate* (sum, count) of the whole window. A monotonic window maintains an *ordered candidate list*, so you can query "what is the max/min in the window?" in O(1) without re-scanning.

## Why we use

- Computes the **max or min of every sliding window in O(n) total** — beating the naive O(n·k) and O(n log k) heap approaches.
- O(k) extra space because the deque never holds more than `k` indices at once.
- Each index enters and leaves the deque exactly once → amortised O(1) per step.
- Generalises beyond max/min: it answers any query that is monotone-friendly (e.g. "shortest subarray with sum ≥ K" using prefix sums + monotonic deque).

## How to implement

```
deque = empty  # stores INDICES, values are non-increasing (for max) or non-decreasing (for min)
for right in 0..n-1:
    # 1. evict elements that are out of window
    while deque is non-empty and deque.front <= right - k:
        deque.popleft()
    # 2. maintain monotonicity: pop indices whose value <= current (for max-window)
    while deque is non-empty and arr[deque.back] <= arr[right]:
        deque.pop()
    deque.push(right)
    # 3. once window has formed, record answer
    if right >= k - 1:
        result.append(arr[deque.front])
```

Python — sliding window maximum:

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq = deque()  # holds indices, nums[dq] is strictly decreasing
    out = []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

JavaScript — sliding window minimum (mirror of max):

```javascript
function minSlidingWindow(nums, k) {
  const dq = [];  // stores indices, nums[dq] is strictly increasing
  const out = [];
  for (let i = 0; i < nums.length; i++) {
    while (dq.length && dq[0] <= i - k) dq.shift();
    while (dq.length && nums[dq[dq.length - 1]] >= nums[i]) dq.pop();
    dq.push(i);
    if (i >= k - 1) out.push(nums[dq[0]]);
  }
  return out;
}
```

Invariant: at any moment, `nums[dq[0]] ≥ nums[dq[1]] ≥ ... ≥ nums[dq[-1]]` (for max-window), and every index in `dq` lies in `[i-k+1, i]`.

## Which problems this approach solves in the real world

- **Trading**: rolling max/min price over a fixed lookback to feed a Donchian-channel or breakout signal.
- **Networking**: rolling-window peak bandwidth measurement for SLA monitoring.
- **Real-time analytics**: max requests-per-second over the last N seconds for autoscaling decisions.
- **Sensor fusion / control systems**: rolling minimum sensor reading to filter spikes.
- **Game telemetry**: highest frame-time over the last N frames to detect stutters.
- **Compiler register allocation**: shortest subarray problems used in liveness analysis.

## Pros and cons

**Pros**
- O(n) total time across all windows — strictly faster than heap (O(n log k)) or naive (O(nk)).
- O(k) space — small and bounded.
- Each element enters and exits the deque exactly once — easy to argue amortised cost.
- Pattern extends to "shortest subarray with sum ≥ K" via prefix sums.

**Cons**
- Trickier to write correctly than a basic two-pointer; the eviction-then-pop-then-push order matters.
- Stores **indices, not values**, so you can do the "out of window" check.
- Doesn't generalise to k-th element (use multiset / heap for that).

## Limitations

- Only works when the answer per window is monotone-friendly (max, min, or a similar order statistic).
- Doesn't directly compute sums, products, or means — those use a simple sum-and-subtract window.
- Eviction is by position (window boundary), not by value, so out-of-order data streams don't fit.
- For 2D sliding-window max, you need to run this trick row-wise then column-wise — implementation gets fiddly.

## One example

**Problem**: Given an integer array `nums` and an integer `k`, return the **maximum element in every sliding window of size k**.
Constraints: `1 ≤ k ≤ nums.length ≤ 10^5`, `-10^4 ≤ nums[i] ≤ 10^4`.

**Input**: `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`
**Output**: `[3, 3, 5, 5, 6, 7]`

## Solution explanation

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

Walk-through on `[1, 3, -1, -3, 5, 3, 6, 7]`, k = 3 (deque shows indices, brackets show values):

| i | x  | evict-front | pop-back while ≤ x | push | deque (vals)  | record? |
|---|----|-------------|--------------------|------|---------------|---------|
| 0 | 1  | —           | —                   | 0    | [0]→[1]       | no (i<2)|
| 1 | 3  | —           | pop 0 (1≤3)         | 1    | [1]→[3]       | no      |
| 2 | -1 | —           | —                   | 2    | [1,2]→[3,-1]  | **3**   |
| 3 | -3 | —           | —                   | 3    | [1,2,3]→[3,-1,-3] | **3** |
| 4 | 5  | pop 1 (out) | pop 2,3 (≤5)        | 4    | [4]→[5]       | **5**   |
| 5 | 3  | —           | —                   | 5    | [4,5]→[5,3]   | **5**   |
| 6 | 6  | —           | pop 5,4 (≤6)        | 6    | [6]→[6]       | **6**   |
| 7 | 7  | —           | pop 6 (≤7)          | 7    | [7]→[7]       | **7**   |

Final output: `[3, 3, 5, 5, 6, 7]`.

Correctness: when we push `right`, any earlier index `j` with `nums[j] ≤ nums[right]` is dominated — `right` is both later and bigger, so it will outlive `j` in every future window. Popping such `j`s preserves the invariant "deque is strictly decreasing in value" without losing any future answer. The front is the largest value still in the window, by construction.

- **Time**: O(n) — every index is pushed once and popped at most once.
- **Space**: O(k) — deque holds at most `k` indices.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold** — basic fixed-window scan; useful warm-up before deque. | https://leetcode.com/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/ |
| Medium | **Sliding Window Maximum** — the canonical monotonic-deque problem; max of every window of size k. | https://leetcode.com/problems/sliding-window-maximum/ |
| Hard | **Shortest Subarray with Sum at Least K** — prefix sums + monotonic increasing deque to find shortest window with sum ≥ K (handles negatives). | https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/ |
