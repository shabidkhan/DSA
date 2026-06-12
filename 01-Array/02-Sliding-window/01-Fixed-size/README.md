# Fixed-size sliding window

## What is this

A scan where you maintain a window of **fixed length `k`** over an array. Initialise the window on the first `k` elements (computing whatever aggregate you need: sum, max, count of distinct), then slide it one step at a time, **adding the entering element and removing the leaving element** from the aggregate. The result is one O(1)-or-O(log k) update per slide instead of recomputing the whole window each time.

## Why we use

- Converts the naive "for each window, scan k elements" O(n·k) approach into **O(n)** (or O(n log k) for max/min queries with a deque/heap).
- Models the common "rolling statistic" use case directly: moving average, rolling max, rolling distinct count.
- Composes cleanly with hash maps, deques, or heaps to support more complex aggregates than a plain sum.

## How to implement

```
window_aggregate = aggregate(arr[0..k-1])
result.append(window_aggregate)

for i in k..n-1:
    add arr[i] to window_aggregate
    remove arr[i - k] from window_aggregate
    result.append(window_aggregate)
```

Python — rolling average of window size `k`:

```python
def rolling_average(nums: list[int], k: int) -> list[float]:
    if len(nums) < k:
        return []
    window_sum = sum(nums[:k])
    out = [window_sum / k]
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        out.append(window_sum / k)
    return out
```

Python — rolling maximum in O(n) using a monotonic deque:

```python
from collections import deque

def rolling_max(nums: list[int], k: int) -> list[int]:
    dq = deque()        # stores indices, values decreasing
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

Invariant: after processing index `i ≥ k - 1`, the window covers exactly `arr[i - k + 1 .. i]`, and the aggregate reflects only those elements. The "add new, remove old" symmetry is what makes each step O(1).

## Which problems this approach solves in the real world

- **Time-series moving averages**: 30-day rolling mean of daily active users, computed in one pass over a stream.
- **Network throughput monitoring**: rolling sum of bytes/sec in the last 60 seconds to trigger alerts.
- **Audio signal processing**: rolling RMS / peak amplitude on a buffer of samples.
- **A/B test windowed metrics**: conversion rate over the last `k` sessions, slid forward as new sessions arrive.
- **Fraud detection windows**: count of transactions in the last `k` events per user, refreshed in O(1) per event.

## Pros and cons

**Pros**
- O(n) total time for sum/count aggregates; O(n) for max/min with a deque.
- O(k) extra space (often even O(1) for sum-only).
- One pass, streaming-friendly — works when you can't randomly seek into the data.
- Easy to combine with hash maps (window-distinct-count, anagram windows).

**Cons**
- Aggregate must be incrementally updatable in O(1) or O(log k). Median over a sliding window needs two heaps or a balanced BST — more involved.
- For very small `k`, the constant-factor overhead of the deque/hash map can be worse than just rescanning.
- Floating-point aggregates can drift over a long stream; periodic recomputation may be needed.

## Limitations

- Requires fixed `k`. If the window size depends on a condition, use **variable-size** sliding window instead.
- Doesn't apply to non-decomposable aggregates (e.g. mode of arbitrary multiset is awkward without extra structures).
- Streaming with k larger than available memory needs reservoir sampling or approximate sketches instead.

## One example

**Problem**: Given an integer array `nums` and an integer `k`, return the **maximum average value** of any contiguous subarray of length `k`. Constraints: `1 ≤ k ≤ nums.length ≤ 10^5`, `-10^4 ≤ nums[i] ≤ 10^4`.

**Input**: `nums = [1, 12, -5, -6, 50, 3]`, `k = 4`
**Output**: `12.75` (subarray `[12, -5, -6, 50]`, sum 51, average 12.75)

## Solution explanation

```python
def find_max_average(nums: list[int], k: int) -> float:
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        if window > best:
            best = window
    return best / k
```

Walk-through on `nums = [1, 12, -5, -6, 50, 3]`, k = 4:

| i | leaving (nums[i-k]) | entering (nums[i]) | window | best |
|---|---------------------|--------------------|--------|------|
| — | —                   | initial sum(nums[0..3]) | 2      | 2    |
| 4 | nums[0] = 1         | nums[4] = 50       | 2 - 1 + 50 = **51** | 51 |
| 5 | nums[1] = 12        | nums[5] = 3        | 51 - 12 + 3 = 42    | 51 |

We track the **sum** of the window (not the average) until the end, because comparing sums is cheaper and avoids floating-point drift; we divide only once at the very end. Each slide is O(1).

- **Time**: O(n) — one initial scan + one per slide.
- **Space**: O(1) — two scalars.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Maximum Average Subarray I** — max average of any size-k window. | https://leetcode.com/problems/maximum-average-subarray-i/ |
| Medium | **Find All Anagrams in a String** — find start indices of windows of size `len(p)` that are anagrams of `p`. | https://leetcode.com/problems/find-all-anagrams-in-a-string/ |
| Hard   | **Sliding Window Maximum** — return the maximum in every size-k window using a monotonic deque. | https://leetcode.com/problems/sliding-window-maximum/ |
