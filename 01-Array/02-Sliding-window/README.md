# Sliding Window Patterns

## Folder structure

```
02-Sliding-window/
├── README.md
├── 01-Fixed-size/README.md
└── 02-Variable-size/
    ├── README.md
    ├── 01-Expand-shrink/README.md
    └── 02-Monotonic-window/README.md
```

## What is this

A sliding window maintains a contiguous subarray (or substring) defined by two boundaries that move forward through the data. The window slides by advancing the right boundary to include new elements and the left boundary to exclude stale ones, all while incrementally updating a running aggregate (sum, count, max, frequency table). This turns "look at every possible subarray" — naturally O(n²) — into a single O(n) pass.

Sliding windows come in two flavours: **fixed-size** (window length is given — average of every k consecutive elements, max sum of k consecutive) and **variable-size** (window grows and shrinks to satisfy a constraint — longest substring without repeats, minimum window substring, longest subarray with sum ≤ K). Variable-size windows further split into **expand-shrink** (grow right, shrink left to maintain validity) and **monotonic-window** (use a deque to track running max/min in O(1)).

## Why we use

- O(n) replacement for naive O(nk) or O(n²) inner loops.
- O(1) extra space for fixed-size; O(k) for frequency-tracking variants.
- The mental model — "what enters the window, what leaves" — is intuitive.
- Generalises to strings, streams, and 2D grids.

## How to implement

```
fixed-size:
    sum = sum(arr[0..k-1])
    for i in k..n-1:
        sum += arr[i] - arr[i - k]
        record(sum)

variable-size (expand-shrink):
    l = 0
    for r in 0..n-1:
        include arr[r] in window
        while window invalid:
            exclude arr[l]; l += 1
        record(r - l + 1)

monotonic deque:
    dq holds indices in decreasing arr-value order; front = max
    push: while dq and arr[dq.back] <= arr[r]: dq.pop_back; dq.push_back(r)
    pop:  if dq.front <= l - 1: dq.pop_front
```

Subpatterns in this folder:

- **01-Fixed-size** — window of known length k.
- **02-Variable-size** — expand-shrink for constraint-based windows; monotonic-window for max/min.

## Which problems this approach solves in the real world

- Rolling averages and moving maxima in time-series.
- Bandwidth and rate-limit windows in networking.
- Longest stretches of valid activity in user-session logs.
- Anomaly detection over rolling baselines.
- Stock-price sliding maxima.
- Streaming aggregations in Kafka / Flink.

## Pros and cons

**Pros**
- O(n) amortised — each element enters and leaves the window once.
- O(1) or O(k) extra space.
- Pattern recognition is fast once practised.
- Pairs with hash maps for constraint-based variants.

**Cons**
- Determining what makes the window "invalid" can be subtle.
- Variable-size with multiple constraints gets messy quickly.
- 2D sliding windows are more complex (need running structures per row or column).
- Off-by-one errors on window bounds are common.

## Limitations

- The constraint must be monotone in window length (otherwise can't shrink left predictably).
- Doesn't help for non-contiguous subarrays — that's subset / DP territory.
- Negative-number windows need extra care (running sum can go non-monotone).
- Streaming with random insertion/deletion needs different structures.
