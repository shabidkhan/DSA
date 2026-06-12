# Variable-size sliding window

## Folder structure

```
02-Variable-size/
├── README.md
├── 01-Expand-shrink/README.md
└── 02-Monotonic-window/README.md
```

## What is this

A two-pointer scan where the window `[left, right]` **grows by advancing `right`** and **shrinks by advancing `left`** based on a condition. Unlike the fixed-size variant, the window length is determined dynamically: you expand while a property holds (or doesn't), then contract until it does (or doesn't). Each element is visited at most twice — once when `right` reaches it, once when `left` passes it — giving overall **O(n)** time.

## Why we use

- Answers "longest / shortest contiguous subarray with property P" in O(n) instead of O(n²).
- Models a huge family of problems: longest substring without repeating characters, minimum window substring, smallest subarray with sum ≥ target, etc.
- Pairs naturally with a hash map / counter to track properties of the current window (distinct count, character frequencies, etc.).

## How to implement

```
left = 0
maintain window_state
for right in 0..n-1:
    add arr[right] to window_state
    while window_state violates the condition:
        remove arr[left] from window_state
        left += 1
    record result based on window [left, right]
```

Python — longest substring without repeating characters:

```python
def length_of_longest_substring(s: str) -> int:
    seen = {}                # char → last index seen
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

Python — minimum size subarray with sum ≥ target:

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    left = 0
    window_sum = 0
    best = float('inf')
    for right, x in enumerate(nums):
        window_sum += x
        while window_sum >= target:
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1
    return 0 if best == float('inf') else best
```

Invariant: the window `[left, right]` always satisfies the loop's chosen condition at the moment the result is recorded. The two pointers each move at most `n` times, so the total work is O(n) even though the inner `while` looks nested.

## Which problems this approach solves in the real world

- **Stream sessionisation**: longest gap-free user session — expand on every event, shrink when an inactivity threshold is exceeded.
- **Rate-limit windowing**: smallest window containing N requests to detect bursts.
- **Substring search with wildcards / multi-character anagrams**: minimum window containing all required characters of a query.
- **Resource usage analytics**: longest period under a memory threshold, growing while OK and shrinking when overshot.
- **Genomics**: shortest substring containing all required nucleotides for a primer.

## Pros and cons

**Pros**
- O(n) time — each pointer advances monotonically.
- O(window-state) space — usually a hash map of size at most `n` distinct elements.
- Streaming-friendly: needs only a forward scan over the input.
- Generalises to many condition types (sum, distinct count, character frequency match).

**Cons**
- The shrink condition must be **monotonic** in the window: once shrinking is required, no future expansion of `right` will fix it without shrinking. If the condition isn't monotone, you need a different technique.
- Off-by-one bugs are common — especially around whether to record the result inside or outside the shrink loop.
- For "exactly K distinct" type problems, the trick is to compute `atMost(K) - atMost(K-1)`; a single window doesn't directly give "exactly K".

## Limitations

- Only works for **contiguous** subarrays/substrings. Subset problems need DP or bitmask techniques.
- Doesn't apply when the condition is non-monotonic (e.g. window must contain at least 3 distinct AND at most 5 distinct — needs two interlocked windows or different DP).
- Negative numbers can break the monotonicity of sum-based conditions ("smallest subarray with sum ≥ target" fails if negatives exist — use prefix sums + deque instead).

## One example

**Problem**: Given a string `s`, find the **length of the longest substring** without repeating characters. Constraints: `0 ≤ s.length ≤ 5·10^4`, `s` consists of ASCII characters.

**Input**: `s = "abcabcbb"`
**Output**: `3` (substring `"abc"`)

## Solution explanation

```python
def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

Walk-through on `s = "abcabcbb"`:

| right | ch | last_seen[ch] (before) | left | last_seen (after) | window length | best |
|-------|----|------------------------|------|-------------------|---------------|------|
| 0     | a  | —                      | 0    | {a:0}             | 1             | 1    |
| 1     | b  | —                      | 0    | {a:0, b:1}        | 2             | 2    |
| 2     | c  | —                      | 0    | {a:0, b:1, c:2}   | 3             | **3** |
| 3     | a  | 0 (≥ left)             | 1    | {a:3, b:1, c:2}   | 3             | 3    |
| 4     | b  | 1 (≥ left)             | 2    | {a:3, b:4, c:2}   | 3             | 3    |
| 5     | c  | 2 (≥ left)             | 3    | {a:3, b:4, c:5}   | 3             | 3    |
| 6     | b  | 4 (≥ left)             | 5    | {a:3, b:6, c:5}   | 2             | 3    |
| 7     | b  | 6 (≥ left)             | 7    | {a:3, b:7, c:5}   | 1             | 3    |

The instant we'd repeat a character, we jump `left` to one past the prior occurrence — never revisiting any index from the left. Both pointers advance monotonically, so even though there's a conditional jump, total work is O(n).

- **Time**: O(n) — each character processed once.
- **Space**: O(min(n, σ)) where σ is the alphabet size.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Minimum Size Subarray Sum** — smallest contiguous subarray with sum ≥ target (positive ints). | https://leetcode.com/problems/minimum-size-subarray-sum/ |
| Medium | **Longest Substring Without Repeating Characters** — the canonical variable-window problem. | https://leetcode.com/problems/longest-substring-without-repeating-characters/ |
| Hard   | **Minimum Window Substring** — smallest window in `s` containing all characters of `t`. | https://leetcode.com/problems/minimum-window-substring/ |
