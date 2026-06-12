# Expand-and-shrink (variable-size sliding window)

## What is this

A variable-size sliding window where the right pointer always **expands** the window by one step each iteration, and the left pointer **shrinks** the window whenever a constraint is violated. The window size is not fixed — it grows and contracts to maintain an invariant (e.g. "sum ≤ target", "at most K distinct characters", "no duplicate elements"). At every iteration the window `[left, right]` is the largest (or smallest) valid window ending at `right`, and the answer is updated from it.

## Why we use

- It converts a search over all O(n²) subarrays/substrings into a single **O(n) two-pointer sweep**, because each element is added once and removed at most once.
- It naturally handles "longest/shortest subarray that satisfies condition X" — a huge family of problems.
- It uses O(1) or O(k) auxiliary state (a running sum, a frequency map keyed by the alphabet), so it scales to large inputs and streams.
- The mental model is simple: "expand until invalid, then shrink until valid again", which makes correctness easy to argue.

## How to implement

```
left = 0
state = empty   # running aggregate (sum, counter, set, etc.)
best = 0        # or +inf for shortest variants
for right in 0..n-1:
    add arr[right] to state
    while constraint is violated:
        remove arr[left] from state
        left += 1
    update best with window [left, right]
return best
```

Python — longest subarray with sum ≤ K (positive numbers):

```python
def longest_sub_at_most_k(nums: list[int], k: int) -> int:
    left = 0
    window_sum = 0
    best = 0
    for right, x in enumerate(nums):
        window_sum += x
        while window_sum > k:
            window_sum -= nums[left]
            left += 1
        best = max(best, right - left + 1)
    return best
```

JavaScript — longest substring with at most K distinct characters:

```javascript
function longestKDistinct(s, k) {
  const freq = new Map();
  let left = 0, best = 0;
  for (let right = 0; right < s.length; right++) {
    freq.set(s[right], (freq.get(s[right]) || 0) + 1);
    while (freq.size > k) {
      const c = s[left++];
      freq.set(c, freq.get(c) - 1);
      if (freq.get(c) === 0) freq.delete(c);
    }
    best = Math.max(best, right - left + 1);
  }
  return best;
}
```

Invariant: after processing index `right`, the window `[left, right]` is the **largest valid window ending at `right`**. Any window with a smaller `left` is invalid and stays invalid forever for this `right`.

## Which problems this approach solves in the real world

- **Rate limiting / quota tracking**: longest interval where request count stayed under quota.
- **Sensor data smoothing**: longest run where a measurement stayed within a tolerance band.
- **Networking**: longest TCP burst where packet rate stayed below congestion threshold.
- **Bioinformatics**: longest DNA stretch with at most K mismatches against a reference.
- **Text editors / autocomplete**: longest prefix containing at most K distinct letter classes (vowels, digits, etc.).
- **Game analytics**: longest streak of plays where a player's score stayed positive.

## Pros and cons

**Pros**
- O(n) time — each element is touched at most twice (one add, one remove).
- O(1) or O(alphabet) space — only the running aggregate.
- Works in a single pass — friendly to streaming data.
- Generalises to many constraints just by swapping the "invalid" check.

**Cons**
- Requires the constraint to be **monotone**: once a window becomes invalid, growing it further can't make it valid again. Negative numbers break this for sum problems.
- Two-pointer code has subtle off-by-ones (when to update `best`, when to shrink, what to do at the end of the array).
- Doesn't directly find "exactly K" — you usually compute "at most K" minus "at most K-1".

## Limitations

- Fails when the constraint isn't monotone. E.g. "subarray with sum exactly K" with negative numbers — use prefix sums + hashmap instead.
- Doesn't apply when you need information from *outside* the window during shrinking (e.g. global rank).
- For "shortest" variants, the loop structure inverts: you shrink while the window is **valid**, not while it's invalid. Mixing them up is the most common bug.
- The window must be contiguous. For non-contiguous selections, this isn't the right tool.

## One example

**Problem**: Given an array of positive integers `nums` and an integer `target`, return the **minimal length** of a contiguous subarray whose sum is ≥ `target`. If no such subarray exists, return 0.
Constraints: `1 ≤ nums.length ≤ 10^5`, `1 ≤ nums[i] ≤ 10^4`, `1 ≤ target ≤ 10^9`.

**Input**: `nums = [2, 3, 1, 2, 4, 3]`, `target = 7`
**Output**: `2` — the subarray `[4, 3]` has sum 7 with length 2.

## Solution explanation

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    left = 0
    window_sum = 0
    best = len(nums) + 1
    for right, x in enumerate(nums):
        window_sum += x
        while window_sum >= target:
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1
    return 0 if best == len(nums) + 1 else best
```

Walk-through on `[2, 3, 1, 2, 4, 3]`, target = 7:

| step | right | x | window | sum | action |
|------|-------|---|--------|-----|--------|
| 0 | 0 (2) | 2 | [2]            | 2  | sum<7 |
| 1 | 1 (3) | 3 | [2,3]          | 5  | sum<7 |
| 2 | 2 (1) | 1 | [2,3,1]        | 6  | sum<7 |
| 3 | 3 (2) | 2 | [2,3,1,2]      | 8  | sum≥7 → best=4; shrink → [3,1,2] sum=6 |
| 4 | 4 (4) | 4 | [3,1,2,4]      | 10 | sum≥7 → best=4; shrink → [1,2,4] sum=7 → best=3; shrink → [2,4] sum=6 |
| 5 | 5 (3) | 3 | [2,4,3]        | 9  | sum≥7 → best=3; shrink → [4,3] sum=7 → best=2; shrink → [3] sum=3 |

Final answer: **2**.

Correctness: when `window_sum ≥ target`, the window `[left, right]` is a valid candidate. Shrinking from the left gives the smallest *valid* window that still ends at `right`. Since `nums[i] > 0`, removing an element strictly decreases the sum — so once the window becomes invalid we must move `right` to recover, never re-using a `left` we already advanced past.

- **Time**: O(n) — `right` advances n times, `left` advances at most n times total across the run.
- **Space**: O(1) — just `left`, `right`, `window_sum`, `best`.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Maximum Average Subarray I** — find the contiguous subarray of length k with the largest average. (Fixed-size variant, good warm-up.) | https://leetcode.com/problems/maximum-average-subarray-i/ |
| Medium | **Longest Substring with At Most K Distinct Characters** — expand and shrink while keeping the distinct-character count ≤ K. | https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/ |
| Hard | **Subarrays with K Different Integers** — count subarrays with exactly K distinct integers, using "at most K" − "at most K−1". | https://leetcode.com/problems/subarrays-with-k-different-integers/ |
