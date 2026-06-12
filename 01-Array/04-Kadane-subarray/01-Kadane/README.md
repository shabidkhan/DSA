# Kadane's algorithm

## What is this

A linear-scan algorithm that computes the **maximum-sum contiguous subarray** of an integer array in one pass. The key insight: at each index `i`, the best subarray ending at `i` is either (a) `arr[i]` alone or (b) `arr[i]` extending the best subarray ending at `i-1`. So you track a rolling `current_sum` and reset it to `arr[i]` whenever the accumulated sum drops below zero. The global maximum of `current_sum` over the scan is the answer.

## Why we use

- Solves "max subarray sum" in O(n) time, O(1) space — a brute-force O(n²) or O(n³) scan is unnecessary.
- The recurrence `best_ending_here = max(arr[i], best_ending_here + arr[i])` is a textbook 1D dynamic programming pattern in disguise.
- It generalises: max product subarray, max circular subarray, max submatrix (2D), and "buy/sell stock once" all reduce to Kadane.

## How to implement

```
best_sum         = arr[0]
best_ending_here = arr[0]
for i in 1..n-1:
    best_ending_here = max(arr[i], best_ending_here + arr[i])
    best_sum         = max(best_sum, best_ending_here)
return best_sum
```

Python — classic Kadane:

```python
def max_subarray(nums: list[int]) -> int:
    best_sum = best_here = nums[0]
    for x in nums[1:]:
        best_here = max(x, best_here + x)
        best_sum = max(best_sum, best_here)
    return best_sum
```

Python — Kadane with start/end indices reconstructed:

```python
def max_subarray_with_indices(nums: list[int]) -> tuple[int, int, int]:
    best_sum = best_here = nums[0]
    best_l = best_r = cur_l = 0
    for i in range(1, len(nums)):
        if nums[i] > best_here + nums[i]:
            best_here = nums[i]
            cur_l = i
        else:
            best_here += nums[i]
        if best_here > best_sum:
            best_sum = best_here
            best_l, best_r = cur_l, i
    return best_sum, best_l, best_r
```

Invariant: after processing index `i`, `best_here` is the maximum sum of any subarray ending exactly at `i`, and `best_sum` is the maximum sum of any subarray ending at or before `i`. The reset rule guarantees that a stretch with negative running sum is discarded — keeping it could only hurt the next candidate.

## Which problems this approach solves in the real world

- **Trading signals**: maximum profit window from a stream of price changes (changes = daily deltas).
- **Sensor anomaly detection**: longest contiguous burst of positive deviation in a time series.
- **Log/QoS analysis**: maximum cumulative "good - bad" event score over any contiguous window.
- **Game balance tuning**: longest streak where a player's score delta stays net positive.
- **Energy management**: peak net-charging interval in a battery telemetry log.

## Pros and cons

**Pros**
- O(n) time, O(1) space — optimal for the problem.
- One pass, branch-light loop — fits in a single CPU register set.
- Trivial to extend with start/end index tracking, or to compute max product (track both min and max).
- Generalises to 2D in O(rows² · cols) for max submatrix.

**Cons**
- All-negative arrays need a careful base case (must return the largest single element, not 0).
- Doesn't natively handle "at least one positive element" or "exactly k elements" constraints — those need different DP.
- For max product, the standard formulation breaks; you must track both min and max because two negatives can multiply to a large positive.

## Limitations

- Works only for **contiguous** subarrays. For arbitrary subsets, use other DP techniques.
- Doesn't apply if the operation isn't associative/monotonic in a useful way (e.g. max XOR subarray needs a trie, not Kadane).
- For streaming data with a sliding window of size `k`, use a deque or sliding-window structure instead — Kadane is for unrestricted windows.

## One example

**Problem**: Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum. Constraints: `1 ≤ nums.length ≤ 10^5`, `-10^4 ≤ nums[i] ≤ 10^4`.

**Input**: `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`
**Output**: `6` (subarray `[4, -1, 2, 1]`)

## Solution explanation

```python
def max_subarray(nums: list[int]) -> int:
    best_sum = best_here = nums[0]
    for x in nums[1:]:
        best_here = max(x, best_here + x)
        best_sum = max(best_sum, best_here)
    return best_sum
```

Walk-through on `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`:

| i | nums[i] | best_here | best_sum |
|---|---------|-----------|----------|
| 0 | -2      | -2        | -2       |
| 1 |  1      | max(1, -2+1) = 1 | 1 |
| 2 | -3      | max(-3, 1-3) = -2 | 1 |
| 3 |  4      | max(4, -2+4) = 4 | 4 |
| 4 | -1      | max(-1, 4-1) = 3 | 4 |
| 5 |  2      | max(2, 3+2) = 5  | 5 |
| 6 |  1      | max(1, 5+1) = 6  | **6** |
| 7 | -5      | max(-5, 6-5) = 1 | 6 |
| 8 |  4      | max(4, 1+4) = 5  | 6 |

At step 2, `best_here` becomes -2 — worse than just starting fresh at the next positive. So at step 3 we discard the running sum and start at `4`. From there we accumulate `4, 3, 5, 6` before another negative spike forces a reset.

- **Time**: O(n) — one pass.
- **Space**: O(1) — two scalars.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Maximum Subarray** — return the largest contiguous sum. | https://leetcode.com/problems/maximum-subarray/ |
| Medium | **Maximum Product Subarray** — like Kadane but for product; track min and max simultaneously. | https://leetcode.com/problems/maximum-product-subarray/ |
| Hard   | **Maximum Sum Circular Subarray** — array wraps around; combine Kadane on `nums` and on the inverted array. | https://leetcode.com/problems/maximum-sum-circular-subarray/ |
