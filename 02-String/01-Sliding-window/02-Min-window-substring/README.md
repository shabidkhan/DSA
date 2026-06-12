# Minimum window substring (need / have counters)

## What is this

A variable-size sliding-window pattern that finds the **shortest substring of `s`** containing all characters of a pattern `t` (with multiplicities). Two counters drive it:

- `need`: a frequency map of required characters from `t`.
- `have`: a counter of how many *required* characters the current window already contains in sufficient quantity (not total characters — only those that have hit their required count).

The window grows on the right until `have == len(need)` (every required char is satisfied), then shrinks on the left as far as possible while staying valid, recording the best window seen.

## Why we use

- Solves the classic "smallest substring containing all of T" problem in **O(|s| + |t|) time** — much better than the naive O(|s|² · |t|) checker.
- Uses a constant-size counter when the alphabet is bounded (ASCII, DNA bases, byte values).
- Generalises to "find a window that satisfies a multiset constraint" — useful in many anagram, permutation, and inclusion problems.
- The `have/need` formulation neatly separates "is the window valid?" from "what characters are involved?", which keeps the code clean.

## How to implement

```
need = Counter(t)
have_counts = empty map
formed = 0       # how many required chars currently meet their target count
required = len(need)
left = 0
best_len, best_l = +inf, 0
for right in 0..n-1:
    c = s[right]
    have_counts[c] += 1
    if c in need and have_counts[c] == need[c]:
        formed += 1
    while formed == required:
        if right - left + 1 < best_len:
            best_len, best_l = right - left + 1, left
        d = s[left]
        have_counts[d] -= 1
        if d in need and have_counts[d] < need[d]:
            formed -= 1
        left += 1
return "" if best_len == +inf else s[best_l : best_l + best_len]
```

Python:

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need = Counter(t)
    have: dict[str, int] = {}
    formed = 0
    required = len(need)
    left = 0
    best = (float("inf"), 0, 0)  # (length, l, r)
    for right, c in enumerate(s):
        have[c] = have.get(c, 0) + 1
        if c in need and have[c] == need[c]:
            formed += 1
        while formed == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            d = s[left]
            have[d] -= 1
            if d in need and have[d] < need[d]:
                formed -= 1
            left += 1
    return "" if best[0] == float("inf") else s[best[1] : best[2] + 1]
```

Invariant: while shrinking, the window is **valid** (covers all of `t`); the moment removing one more character would make `formed < required`, we stop and let `right` advance again.

## Which problems this approach solves in the real world

- **Log searching**: smallest contiguous log range containing every error code from a watchlist.
- **DNA matching with multiplicity**: shortest region containing a required mix of nucleotides.
- **Compiler / lexer scope analysis**: smallest token window containing every required identifier.
- **E-commerce**: smallest contiguous purchase history covering every product in a wishlist.
- **Network packet inspection**: shortest byte range containing all signature bytes of a known payload.
- **Document summarisation**: shortest excerpt containing all keywords of a query.

## Pros and cons

**Pros**
- Linear time O(|s| + |t|) — each character of `s` enters and leaves the window at most once.
- O(|alphabet|) extra space — bounded by characters of `t`.
- The `formed` counter avoids re-checking the whole map every iteration; only changes are tracked.
- Cleanly extends to anagram/permutation-in-string problems with minor tweaks.

**Cons**
- The condition `have[c] == need[c]` (not `>=`) is subtle — using `>=` over-counts and yields wrong `formed`.
- Two layers of "is this character required?" checks make the code dense; off-by-one and missed branches are common.
- Returns the first minimum found; if you need *all* minima you must change the comparison and collect.

## Limitations

- Requires a definable "valid" condition you can incrementally maintain. For fuzzy matches, this isn't the right tool.
- The window has to be contiguous; can't skip characters.
- For huge alphabets (full Unicode), the hashmap overhead can dominate.
- Doesn't directly handle "*at least one* of each of K groups" — you'd need a more complex state.

## One example

**Problem**: Given two strings `s` and `t` of lengths m and n respectively, return the **minimum window substring** of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return `""`.
Constraints: `1 ≤ m, n ≤ 10^5`, `s` and `t` consist of English letters.

**Input**: `s = "ADOBECODEBANC"`, `t = "ABC"`
**Output**: `"BANC"` — it contains A, B, and C and has minimal length (4).

## Solution explanation

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    if not s or not t:
        return ""
    need = Counter(t)
    have: dict[str, int] = {}
    formed, required = 0, len(need)
    left = 0
    best = (float("inf"), 0, 0)
    for right, c in enumerate(s):
        have[c] = have.get(c, 0) + 1
        if c in need and have[c] == need[c]:
            formed += 1
        while formed == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            d = s[left]
            have[d] -= 1
            if d in need and have[d] < need[d]:
                formed -= 1
            left += 1
    return "" if best[0] == float("inf") else s[best[1] : best[2] + 1]
```

Walk-through on `s = "ADOBECODEBANC"`, `t = "ABC"` (need = {A:1, B:1, C:1}, required = 3):

| right | c | have changes      | formed | shrink? best window |
|-------|---|-------------------|--------|---------------------|
| 0     | A | A:1 → met         | 1      | no |
| 1     | D | D:1               | 1      | no |
| 2     | O | O:1               | 1      | no |
| 3     | B | B:1 → met         | 2      | no |
| 4     | E | E:1               | 2      | no |
| 5     | C | C:1 → met         | 3      | shrink: "ADOBEC" (6) → "DOBEC" (formed=2, stop) |
| 6     | O | O:2               | 2      | no |
| 7     | D | D:2               | 2      | no |
| 8     | E | E:2               | 2      | no |
| 9     | B | B:2               | 2      | no |
| 10    | A | A:2 → wait, A was already met; have[A]=2 ≠ need[A]=1, formed stays | 2 | no |

Hmm — actually at step 10, since A's first occurrence (index 0) was popped during the shrink, `have[A]` went to 0; the second A here lifts it back to 1 = need, so `formed → 3`. Let me re-trace from index 6 with that in mind:

| right | c | running have   | formed | shrink → best |
|-------|---|---------------|--------|---------------|
| 5     | C | A:1,D:1,O:1,B:1,E:1,C:1 | 3 | left=0: best=(6, "ADOBEC"); pop A → A:0 (formed=2); left=1 |
| 6     | O | O:2           | 2      | no |
| 7     | D | D:2           | 2      | no |
| 8     | E | E:2           | 2      | no |
| 9     | B | B:2           | 2      | no |
| 10    | A | A:1 → met     | 3      | pop D,O,B,E... shrink to "BANC" eventually? continue with right first |
| 11    | N | N:1           | 3      | best now (4, "BANC") after pops |
| 12    | C | C:2           | 3      | further shrink narrows to "BANC" (length 4) |

Final answer: **"BANC"** (length 4).

Correctness: the `formed` counter increments **only** when a required character reaches its needed count exactly, and decrements **only** when it drops below. So `formed == required` is true iff every requirement is met. While true, the window is a valid candidate, and shrinking finds the smallest valid window ending at the current `right`.

- **Time**: O(|s| + |t|) — each `right` step is O(1), and `left` advances at most |s| times total.
- **Space**: O(|alphabet|) — the two counters.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Find All Anagrams in a String** — fixed-size window variant where we look for permutations of `p` in `s`. | https://leetcode.com/problems/find-all-anagrams-in-a-string/ |
| Medium | **Permutation in String** — check if any permutation of `s1` is a substring of `s2`; same need/have framework, fixed size. | https://leetcode.com/problems/permutation-in-string/ |
| Hard | **Minimum Window Substring** — the canonical problem this pattern solves. | https://leetcode.com/problems/minimum-window-substring/ |
