# Huffman / merge cost (greedy)

## What is this

The "merge cost" greedy pattern: given a collection of weights, repeatedly merge the two smallest into a single combined weight equal to their sum, and pay that sum as the merge cost. The minimum total cost is achieved by always picking the two smallest currently in the pool — implemented with a min-heap.

This is the same greedy structure as Huffman coding, applied here for sequence-merge cost (minimum cost to connect sticks, minimum cost to merge files, etc.).

## Why we use

- O(n log n) — heap-driven greedy.
- Provably optimal via Huffman's exchange argument.
- Single template covers minimum-cost merging, optimal prefix codes, optimal connect-sticks.
- Easy to implement with `heapq.heapify` + repeated `heappop`/`heappush`.

## How to implement

```
heap = list(weights)
heapify(heap)
total = 0
while len(heap) > 1:
    a = heappop(heap)
    b = heappop(heap)
    total += a + b
    heappush(heap, a + b)
return total
```

```python
import heapq

def min_merge_cost(weights):
    heap = list(weights)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)
    return total
```

```python
def connect_sticks(sticks):
    return min_merge_cost(sticks)
```

The optimality argument: any other strategy pays each weight in some sum at least as many times as the always-smallest-first strategy.

## Which problems this approach solves in the real world

- File / log concatenation: minimize total bytes read.
- Merging k sorted streams when each merge costs combined-size.
- Huffman coding for prefix-free codes (same greedy step).
- Optimal binary tree of weighted leaves (e.g. optimal BST given frequencies).
- Network-message bundling cost minimization.

## Pros and cons

**Pros**
- O(n log n) optimal.
- Simple, well-understood greedy.
- Same template as Huffman coding.

**Cons**
- Heap overhead vs counting / bucket alternatives for small alphabets.
- Doesn't extend to constrained merges (e.g. "always merge adjacent in order" needs interval DP).
- Cannot handle "merge k at a time" cleanly without modification.

## Limitations

- Adjacent-only merges (matrix chain multiplication) need interval DP, not heap.
- Streaming variants need online priority queues.
- Tie-breaking is arbitrary; deterministic ordering needs extra keys.

## One example

**Problem**: You have sticks of various lengths. The cost of joining two sticks is the sum of their lengths. Return the minimum total cost to join all sticks into one.

**Input**: `sticks = [2, 4, 3]`
**Output**: `14`
**Constraints**: `1 <= n <= 10^4`, `1 <= sticks[i] <= 10^4`.

## Solution explanation

```python
import heapq

def connectSticks(sticks):
    heapq.heapify(sticks)
    total = 0
    while len(sticks) > 1:
        a = heapq.heappop(sticks)
        b = heapq.heappop(sticks)
        total += a + b
        heapq.heappush(sticks, a + b)
    return total
```

Walkthrough on `sticks = [2, 4, 3]`:

| step | heap before | pop a | pop b | merge | total |
|------|-------------|-------|-------|-------|-------|
| 1    | [2, 4, 3]   | 2     | 3     | 5     | 5     |
| 2    | [4, 5]      | 4     | 5     | 9     | 14    |

Return 14. Time: O(n log n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Last Stone Weight (LeetCode 1046) | https://leetcode.com/problems/last-stone-weight/ |
| Medium | Minimum Cost to Connect Sticks (LeetCode 1167) | https://leetcode.com/problems/minimum-cost-to-connect-sticks/ |
| Hard | Reorganize String (LeetCode 767) | https://leetcode.com/problems/reorganize-string/ |
