# Sliding window on strings

## Folder structure

```
01-Sliding-window/
├── README.md
├── 01-Longest-substring-without-repeat/README.md
├── 02-Min-window-substring/README.md
└── 03-Anagram/README.md
```

## What is this

Sliding window on strings is a pattern where two pointers `l` and `r` define a contiguous window over the string, and a hash map (or fixed-size counter) tracks the characters currently inside the window. The window grows by moving `r` forward and shrinks by moving `l` forward when a constraint is violated.

It is the string-specialized form of the variable-size sliding window pattern, and is used to answer questions like "longest substring with property X" or "smallest substring containing all characters of T".

## Why we use

- Reduces brute-force `O(n^2)` substring scans to a single linear `O(n)` pass.
- Naturally fits "longest/shortest substring with constraint" problems.
- The window state (a counter) updates incrementally in `O(1)` per character.
- Works seamlessly with character-frequency constraints (distinct chars, ratios, exact matches).

## How to implement

```text
function longestWithAtMostKDistinct(s, k):
    count = {}
    l = 0
    best = 0
    for r in 0..len(s)-1:
        count[s[r]] += 1
        while len(count) > k:
            count[s[l]] -= 1
            if count[s[l]] == 0: del count[s[l]]
            l += 1
        best = max(best, r - l + 1)
    return best
```

```python
from collections import defaultdict

def longest_at_most_k_distinct(s: str, k: int) -> int:
    if k == 0:
        return 0
    count = defaultdict(int)
    l = 0
    best = 0
    for r, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[l]] -= 1
            if count[s[l]] == 0:
                del count[s[l]]
            l += 1
        best = max(best, r - l + 1)
    return best
```

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    have = {}
    required = len(need)
    formed = 0
    l = 0
    best = (float("inf"), 0, 0)
    for r, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if ch in need and have[ch] == need[ch]:
            formed += 1
        while formed == required:
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, r)
            have[s[l]] -= 1
            if s[l] in need and have[s[l]] < need[s[l]]:
                formed -= 1
            l += 1
    return "" if best[0] == float("inf") else s[best[1] : best[2] + 1]
```

The invariant: between `l` and `r`, the window always represents a valid (or just-broken) candidate. When the constraint breaks, shrink from the left until it holds again. Every index enters and leaves the window at most once, so the total work is `O(n)`.

## Which problems this approach solves in the real world

- Detecting brute-force login attempts: smallest window of log entries that contains all suspicious IPs.
- Streaming text analytics: longest stretch of tweets/messages containing at most `k` distinct hashtags.
- Bioinformatics: smallest DNA segment containing all required nucleotide markers.
- Real-time chat moderation: shortest substring containing all banned-phrase keywords.
- Network packet inspection: longest contiguous packet payload matching a character-frequency profile.

## Pros and cons

**Pros**
- Single `O(n)` pass with `O(k)` extra memory (k = alphabet/distinct count).
- Simple to extend with character-frequency constraints.
- Each character touched at most twice (in/out), so constants are small.

**Cons**
- Requires the constraint to be "monotonic": shrinking a valid window must keep it valid (or restore feasibility).
- Counter bookkeeping is bug-prone; off-by-one errors are common.
- Cannot answer non-contiguous subsequence questions.

## Limitations

- Constraints that depend on global string properties (e.g., median character) break the pattern.
- For multibyte/Unicode strings, treat the string as a list of codepoints before iterating.
- Very large alphabets (e.g., 1M distinct emojis) make the counter heavy; consider hashing or rolling hash instead.
- Problems requiring "exactly k" rather than "at most k" need two runs (`atMost(k) - atMost(k-1)`).

## One example

Problem: Given a string `s` and an integer `k`, return the length of the longest substring of `s` that contains at most `k` distinct characters.

```
Input:  s = "eceba", k = 2
Output: 3        # "ece"

Input:  s = "aa",    k = 1
Output: 2        # "aa"
```

Constraints: `1 <= len(s) <= 5 * 10^4`, `0 <= k <= 50`.

## Solution explanation

```python
from collections import defaultdict

def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    if k == 0:
        return 0
    count = defaultdict(int)
    l = 0
    best = 0
    for r, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[l]] -= 1
            if count[s[l]] == 0:
                del count[s[l]]
            l += 1
        best = max(best, r - l + 1)
    return best
```

Walkthrough for `s = "eceba"`, `k = 2`:

| r | s[r] | count after add | shrink? | l | window | best |
|---|------|-----------------|---------|---|--------|------|
| 0 | e | {e:1} | no | 0 | "e" | 1 |
| 1 | c | {e:1,c:1} | no | 0 | "ec" | 2 |
| 2 | e | {e:2,c:1} | no | 0 | "ece" | 3 |
| 3 | b | {e:2,c:1,b:1} | yes, drop e then c | 3 | "b" | 3 |
| 4 | a | {b:1,a:1} | no | 3 | "ba" | 3 |

Return `3`.

Time: `O(n)`. Space: `O(k)` for the counter.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Longest Substring Without Repeating Characters (LeetCode 3) | https://leetcode.com/problems/longest-substring-without-repeating-characters/ |
| Medium | Longest Substring with At Most K Distinct Characters (LeetCode 340) | https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/ |
| Hard | Minimum Window Substring (LeetCode 76) | https://leetcode.com/problems/minimum-window-substring/ |
