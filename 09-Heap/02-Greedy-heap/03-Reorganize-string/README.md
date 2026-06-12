# Reorganize string (heap)

## What is this

Reorganize-string asks to rearrange the characters of a string so that no two adjacent characters are the same. The greedy approach uses a max-heap keyed by remaining count: always emit the most-frequent character whose previous emission was *not* the immediate prior output. After emitting a character, "park" it until one step later, then return it to the heap.

This is a sibling pattern of Task Scheduler — same heap + parking-slot pattern, different cooldown (always 1).

## Why we use

- O(n log k) — small alphabet so very fast in practice.
- Greedy "most frequent first" provably minimal-conflict.
- Easy correctness argument: if any char's count exceeds ceil(n/2), no valid arrangement exists.
- Same machinery extends to Reorganize-string-with-cooldown-k.

## How to implement

```
counts = Counter(s)
if max count > (n + 1) // 2: return ""
heap = max-heap of (-count, char)
prev = (0, '#')        # placeholder
out = []
while heap:
    c, ch = heappop(heap)         # c is negative
    out.append(ch)
    if prev[0] < 0: heappush(heap, prev)
    prev = (c + 1, ch)            # one less remaining
return "".join(out)
```

```python
import heapq
from collections import Counter

def reorganize_string(s):
    n = len(s)
    counts = Counter(s)
    if max(counts.values()) > (n + 1) // 2:
        return ""
    heap = [(-cnt, ch) for ch, cnt in counts.items()]
    heapq.heapify(heap)
    out = []
    prev = (0, '#')
    while heap:
        cnt, ch = heapq.heappop(heap)
        out.append(ch)
        if prev[0] < 0:
            heapq.heappush(heap, prev)
        prev = (cnt + 1, ch)
    return "".join(out)
```

```python
def is_valid(s):
    return all(s[i] != s[i + 1] for i in range(len(s) - 1))
```

The "previous" parking slot blocks immediate re-emission of the same character.

## Which problems this approach solves in the real world

- Card-shuffling so no two same-color cards land adjacent.
- Spacing-out scheduled notifications by category.
- Round-robin tournament seeding so no opponent repeats.
- Audio playlist generation that avoids same-artist back-to-back tracks.
- Distributing tasks across workers so no worker handles two of one type in a row.

## Pros and cons

**Pros**
- O(n log k) — fast on typical alphabets.
- Simple correctness argument via the ceil(n/2) bound.
- Generalizes to cooldown k > 1.

**Cons**
- Heap + previous-slot pattern is verbose for a small concept.
- Edge case when ceil(n/2) bound exceeded must be handled explicitly.
- Output order is not unique.

## Limitations

- Cooldown k > 1 requires the full Task Scheduler queue pattern.
- Streaming variants need online heap updates.
- Tie-breaking is arbitrary; specific deterministic order requires extra keys.

## One example

**Problem**: Given a string `s`, rearrange the characters so that any two adjacent characters are not the same. Return any such valid arrangement; if none exists, return `""`.

**Input**: `s = "aab"`
**Output**: `"aba"`
**Constraints**: `1 <= s.length <= 500`, `s` consists of lowercase letters.

## Solution explanation

```python
import heapq
from collections import Counter

def reorganizeString(s):
    counts = Counter(s)
    n = len(s)
    if max(counts.values()) > (n + 1) // 2:
        return ""
    heap = [(-c, ch) for ch, c in counts.items()]
    heapq.heapify(heap)
    out = []
    prev = (0, '#')
    while heap:
        c, ch = heapq.heappop(heap)
        out.append(ch)
        if prev[0] < 0:
            heapq.heappush(heap, prev)
        prev = (c + 1, ch)
    return "".join(out)
```

Walkthrough on `s = "aab"`:

| step | heap before     | prev     | pop      | out  | new prev   |
|------|------------------|----------|----------|------|------------|
| 1    | [(-2,'a'), (-1,'b')] | (0,'#') | (-2,'a') | "a"  | (-1,'a')   |
| 2    | [(-1,'b')]        | (-1,'a') | (-1,'b') | "ab" | push prev → heap=[(-1,'a')]; prev=(0,'b') |
| 3    | [(-1,'a')]        | (0,'b')  | (-1,'a') | "aba"| (0,'a')    |

Return "aba". Time: O(n log k). Space: O(k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Sort Characters By Frequency (LeetCode 451) | https://leetcode.com/problems/sort-characters-by-frequency/ |
| Medium | Reorganize String (LeetCode 767) | https://leetcode.com/problems/reorganize-string/ |
| Hard | Rearrange String k Distance Apart (LeetCode 358) | https://leetcode.com/problems/rearrange-string-k-distance-apart/ |
