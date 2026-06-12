# Top-K elements (heap)

## What is this

The Top-K pattern returns the `k` largest (or smallest) elements of a stream or array. The standard heap approach maintains a min-heap of size `k`: for every new element, push it; if the heap size exceeds `k`, pop the smallest. The heap then always contains the `k` largest seen so far.

For static arrays, Quickselect gives expected O(n) time to find the kth element, after which a single partition collects the top k. The heap approach is preferred when data is streaming or when `k` is small relative to `n`.

## Why we use

- O(n log k) deterministic time, ideal when k << n
- Constant memory beyond the heap (`O(k)`) — great for streams
- One-pass: process each element exactly once, never revisit
- Easy to generalise to "top k by score", "top k by frequency", "k closest points"

## How to implement

```
heap = []   # min-heap
for x in stream:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)
return heap   # k largest elements (unordered)
```

```python
import heapq

def top_k_largest(nums: list[int], k: int) -> list[int]:
    heap: list[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
```

Top K frequent elements with `Counter`:

```python
from collections import Counter
import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    return [x for x, _ in heapq.nlargest(k, counts.items(), key=lambda kv: kv[1])]
```

K closest points to the origin (max-heap by negating distance):

```python
import heapq

def k_closest(points: list[tuple[int, int]], k: int) -> list[tuple[int, int]]:
    heap: list[tuple[int, tuple[int, int]]] = []
    for x, y in points:
        d = x * x + y * y
        heapq.heappush(heap, (-d, (x, y)))
        if len(heap) > k:
            heapq.heappop(heap)
    return [p for _, p in heap]
```

Invariant for `top_k_largest`: after processing the i-th element, the heap holds the k largest elements seen in `nums[:i+1]`, with the smallest of them at `heap[0]` (the candidate to evict next).

## Which problems this approach solves in the real world

- "Top 10 trending hashtags" over a live event stream
- Search ranking: keep the k highest-scoring documents while iterating candidates
- Anomaly detection: track top-k largest outliers in a sliding window
- Leaderboards in games where only the top n need to be persisted
- Nearest-neighbour queries (k closest data points to a query in feature space)

## Pros and cons

**Pros**
- O(n log k) beats O(n log n) sort when k is small
- O(k) memory — streaming-friendly
- Easy to extend to weighted / scored variants

**Cons**
- Doesn't give a sorted output (need an extra sort if order matters)
- Slower than Quickselect on static arrays for very large `k`
- Heap operations have non-trivial constant factor — array sort can win on small `n`

## Limitations

- Can't easily produce "top k% of a distribution" without knowing n in advance
- Pure heap can't answer median or arbitrary quantiles in one pass (use two heaps)
- Ties broken by heap ordering rather than insertion order without auxiliary key

## One example

Problem: Given an integer array `nums` and an integer `k`, return the `k`-th largest element in the array.

```
Input:  nums = [3, 2, 1, 5, 6, 4], k = 2
Output: 5
Constraints: 1 <= k <= len(nums) <= 10^5, -10^4 <= nums[i] <= 10^4
```

## Solution explanation

```python
import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    heap: list[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

After the loop, the heap holds the `k` largest values; its root is the smallest of those, which is the kth largest overall.

Walkthrough for `nums = [3, 2, 1, 5, 6, 4]`, `k = 2`:

| x | push then | heap (sorted view) | pop if > k | heap after  |
|---|-----------|--------------------|------------|-------------|
| 3 | push 3    | [3]                | size 1 ok  | [3]         |
| 2 | push 2    | [2, 3]             | size 2 ok  | [2, 3]      |
| 1 | push 1    | [1, 2, 3]          | pop 1      | [2, 3]      |
| 5 | push 5    | [2, 3, 5]          | pop 2      | [3, 5]      |
| 6 | push 6    | [3, 5, 6]          | pop 3      | [5, 6]      |
| 4 | push 4    | [4, 5, 6]          | pop 4      | [5, 6]      |

`heap[0] = 5`, which is the 2nd largest. Time O(n log k), space O(k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Last Stone Weight (LeetCode 1046) | https://leetcode.com/problems/last-stone-weight/ |
| Medium | Kth Largest Element in an Array (LeetCode 215) | https://leetcode.com/problems/kth-largest-element-in-an-array/ |
| Hard | Find K Pairs with Smallest Sums (LeetCode 373) | https://leetcode.com/problems/find-k-pairs-with-smallest-sums/ |
