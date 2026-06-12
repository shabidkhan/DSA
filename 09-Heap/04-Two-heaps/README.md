# Two heaps

## What is this

The Two-Heap pattern maintains a partition of a multiset into "lower half" (a max-heap) and "upper half" (a min-heap), with size invariants such that the median is always accessible at one of the two roots. It supports insertion in O(log n), median lookup in O(1), and is the canonical way to compute running medians.

The same idea applies whenever you need fast access to two extremes of a dynamically updated set — e.g. the smallest in the upper half and the largest in the lower half — such as in IPO problems and "median-style" thresholds.

## Why we use

- O(log n) insert and O(1) median query on a dynamic stream
- Generalises to any "split-the-set" problem with two-sided extremum queries
- Saves a full sort per insertion
- Easy to extend with lazy deletion for sliding-window medians

## How to implement

```
lower = max-heap   (we store -x to use min-heap as max-heap)
upper = min-heap

insert(x):
    if lower empty or x <= -lower.peek():
        push -x to lower
    else:
        push x to upper
    # rebalance so |size(lower) - size(upper)| <= 1, lower never smaller
    if len(lower) > len(upper) + 1:
        push -heappop(lower) to upper
    elif len(upper) > len(lower):
        push -heappop(upper) to lower

median():
    if len(lower) > len(upper): return -lower[0]
    return (-lower[0] + upper[0]) / 2
```

```python
import heapq

class MedianFinder:
    def __init__(self) -> None:
        self.lower: list[int] = []   # max-heap via negation
        self.upper: list[int] = []   # min-heap

    def add(self, x: int) -> None:
        if not self.lower or x <= -self.lower[0]:
            heapq.heappush(self.lower, -x)
        else:
            heapq.heappush(self.upper, x)
        if len(self.lower) > len(self.upper) + 1:
            heapq.heappush(self.upper, -heapq.heappop(self.lower))
        elif len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def median(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0
```

Invariant: every element in `lower` is `<=` every element in `upper`, and `|len(lower) - len(upper)| <= 1` with `lower` allowed to be one larger. Therefore the median is either `-lower[0]` (odd total) or the average of the two roots (even total).

## Which problems this approach solves in the real world

- Real-time median of incoming sensor data (temperature, latency)
- Rolling median in financial time series (detect drift without a full sort)
- Threshold tracking in adaptive trading: median of recent prices
- Anomaly detection where "above-median" and "below-median" buckets must each be queried
- Online statistics dashboards that update p50 as new events arrive

## Pros and cons

**Pros**
- O(log n) per insert, O(1) median
- Streaming-friendly, no full re-sort
- Simple core; extends to other quantiles with multiple heaps

**Cons**
- Doesn't support arbitrary deletion without a lazy-deletion add-on
- Median is only one quantile — p90/p99 needs a different structure
- Two heaps mean two memory allocations and two `heappop` constants per insertion

## Limitations

- Cannot answer arbitrary rank queries (use order statistics tree / SortedList)
- Sliding-window median requires lazy deletion; raw two-heaps cannot remove old values
- For huge data sets, approximate sketches (t-digest) are more memory-efficient

## One example

Problem: Design a data structure that supports adding numbers and returning the median of all numbers added so far.

```
Input:
    add(1)
    add(2)
    median() -> 1.5
    add(3)
    median() -> 2
Constraints: up to 5 * 10^4 operations, |value| <= 10^5
```

## Solution explanation

```python
import heapq

class MedianFinder:
    def __init__(self) -> None:
        self.lower: list[int] = []
        self.upper: list[int] = []

    def add(self, x: int) -> None:
        if not self.lower or x <= -self.lower[0]:
            heapq.heappush(self.lower, -x)
        else:
            heapq.heappush(self.upper, x)
        if len(self.lower) > len(self.upper) + 1:
            heapq.heappush(self.upper, -heapq.heappop(self.lower))
        elif len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def median(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0
```

Push into the appropriate heap based on value relative to current low-side max; rebalance if either heap grows too large; report median from the heap roots.

Walkthrough for the operation sequence above:

| Operation | lower (max view) | upper (min view) | Returned    |
|-----------|------------------|-------------------|-------------|
| add(1)    | [1]              | []                |             |
| add(2)    | [1]              | [2]               |             |
| median()  | [1]              | [2]               | (1 + 2) / 2 = 1.5 |
| add(3)    | [2, 1]           | [3]               |             |
| median()  | [2, 1]           | [3]               | -lower[0] = 2 |

Time O(log n) per `add`, O(1) per `median`. Space O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Kth Largest Element in a Stream (LeetCode 703) | https://leetcode.com/problems/kth-largest-element-in-a-stream/ |
| Medium | Find Median from Data Stream (LeetCode 295) | https://leetcode.com/problems/find-median-from-data-stream/ |
| Hard | Sliding Window Median (LeetCode 480) | https://leetcode.com/problems/sliding-window-median/ |
