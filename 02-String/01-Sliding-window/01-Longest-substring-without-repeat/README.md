# Longest substring without repeating characters

## What is this

A variable-size sliding-window pattern for strings. The right pointer expands the window character by character; the left pointer jumps forward whenever a duplicate enters the window, restoring the invariant "all characters in `[left, right]` are unique". A hashmap (or array indexed by ASCII code) stores the **last seen index** of every character so that the left jump is O(1).

## Why we use

- Converts the naive O(n²) "for every left, scan right" into a single **O(n) two-pointer sweep**.
- Uses O(σ) memory where σ is the alphabet size (52 for letters, 128 for ASCII, ~10⁵ for full Unicode codepoints in practice) — independent of input length.
- The last-seen-index trick lets `left` skip multiple positions at once instead of advancing one by one — important when duplicates appear far apart.
- The pattern generalises to many "longest substring with property P" problems by swapping the duplicate check for any other invariant.

## How to implement

```
left = 0
last_seen = empty map  # char -> most recent index
best = 0
for right in 0..n-1:
    c = s[right]
    if c in last_seen and last_seen[c] >= left:
        left = last_seen[c] + 1
    last_seen[c] = right
    best = max(best, right - left + 1)
return best
```

Python:

```python
def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in last_seen and last_seen[c] >= left:
            left = last_seen[c] + 1
        last_seen[c] = right
        best = max(best, right - left + 1)
    return best
```

JavaScript:

```javascript
function lengthOfLongestSubstring(s) {
  const lastSeen = new Map();
  let left = 0, best = 0;
  for (let right = 0; right < s.length; right++) {
    const c = s[right];
    if (lastSeen.has(c) && lastSeen.get(c) >= left) {
      left = lastSeen.get(c) + 1;
    }
    lastSeen.set(c, right);
    best = Math.max(best, right - left + 1);
  }
  return best;
}
```

Invariant: at the end of each iteration, the substring `s[left..right]` has **all distinct characters**, and any longer substring ending at `right` would contain a duplicate.

## Which problems this approach solves in the real world

- **Token / session deduplication**: longest stretch of unique session IDs in a clickstream.
- **DNA / genome analysis**: longest unique-base run, useful for identifying low-complexity regions.
- **Log analysis**: longest interval where every error code was unique (signals random vs. clustered failures).
- **URL routing**: validating that a path segment doesn't repeat a category.
- **Password strength heuristics**: penalising long repeating runs.
- **Game design**: longest streak of unique pickups in a roguelike level for scoring bonuses.

## Pros and cons

**Pros**
- O(n) time — every character is visited at most twice (push to right, jump over by left).
- O(σ) space — small constant for ASCII; bounded by alphabet for Unicode.
- Single pass, streaming-friendly.
- The `last_seen[c] >= left` check elegantly handles characters that were duplicates *before* the window started but are now stale.

**Cons**
- The `>= left` guard is easy to forget — without it, `left` can jump backwards and give wrong answers.
- For very large alphabets (full Unicode, BPE token vocab) the hashmap can be memory-heavy.
- Doesn't directly extend to "all unique within a constraint" — see "at most K distinct" variant for that.

## Limitations

- Only works for the "no repeats" constraint as-is. Variants like "exactly K distinct" or "at most K distinct" need a frequency-counter window instead of last-seen index.
- Not suitable when characters carry weight or score and the window is bounded by total weight — that's a different DP/window mix.
- Doesn't return the substring itself by default — track `best_left` alongside `best` if you need to reconstruct it.

## One example

**Problem**: Given a string `s`, find the length of the **longest substring** without repeating characters.
Constraints: `0 ≤ s.length ≤ 5 × 10^4`, `s` consists of English letters, digits, symbols and spaces.

**Input**: `s = "abcabcbb"`
**Output**: `3` — the answer is `"abc"`, length 3.

## Solution explanation

```python
def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in last_seen and last_seen[c] >= left:
            left = last_seen[c] + 1
        last_seen[c] = right
        best = max(best, right - left + 1)
    return best
```

Walk-through on `"abcabcbb"`:

| right | c | last_seen[c] | left  | window         | length | best |
|-------|---|--------------|-------|----------------|--------|------|
| 0     | a | —            | 0     | "a"            | 1      | 1    |
| 1     | b | —            | 0     | "ab"           | 2      | 2    |
| 2     | c | —            | 0     | "abc"          | 3      | 3    |
| 3     | a | 0 (≥ 0)      | 1     | "bca"          | 3      | 3    |
| 4     | b | 1 (≥ 1)      | 2     | "cab"          | 3      | 3    |
| 5     | c | 2 (≥ 2)      | 3     | "abc"          | 3      | 3    |
| 6     | b | 4 (≥ 3)      | 5     | "cb"           | 2      | 3    |
| 7     | b | 6 (≥ 5)      | 7     | "b"            | 1      | 3    |

Final answer: **3**.

Correctness: the guard `last_seen[c] >= left` is crucial — if the previously-seen copy of `c` is *outside* the current window (already skipped), it can be safely ignored. When it's *inside*, we jump `left` to `last_seen[c] + 1`, the smallest position that excludes the duplicate. Every other position from the old `left` to `last_seen[c]` would still contain the duplicate, so we can't keep any of them.

- **Time**: O(n) — `right` advances n times; `left` only ever moves forward.
- **Space**: O(min(n, σ)) where σ is the alphabet size.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Reverse Vowels of a String** — basic two-pointer string walk; warm-up for string indexing. | https://leetcode.com/problems/reverse-vowels-of-a-string/ |
| Medium | **Longest Substring Without Repeating Characters** — the canonical problem this pattern solves. | https://leetcode.com/problems/longest-substring-without-repeating-characters/ |
| Hard | **Longest Substring with At Most K Distinct Characters** — frequency-counter window variant; the natural generalisation. | https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/ |
