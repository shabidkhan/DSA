# Kadane / Subarray Patterns

## Folder structure

```
04-Kadane-subarray/
├── README.md
├── 01-Kadane/README.md
├── 02-Max-product-subarray/README.md
└── 03-Subarray-with-XOR/README.md
```

## What is this

Kadane's algorithm is the canonical solution to the maximum-subarray problem: find the contiguous subarray with the largest sum, in O(n) time and O(1) space. The core idea is breathtakingly simple — at every index, decide whether to extend the current best subarray or start a new one ending here. The family generalises to maximum product subarray (track both max and min because negatives flip), and to "count subarrays with sum = K" or "with XOR = K" (which pair prefix sums/XORs with a hash map).

The unifying skeleton is "track a running aggregate ending at index i; reset or extend based on a local rule; update global answer". Once you internalise this, problems like Maximum Subarray, Maximum Product Subarray, Maximum Circular Subarray, and Subarray Sum Equals K all feel like variants of the same idea.

## Why we use

- O(n) — best possible for this problem class.
- O(1) extra space for the classic case.
- Single-pass — works on streams as well as static arrays.
- The "extend or restart" decision generalises to many running-aggregate problems.

## How to implement

```
max subarray sum (Kadane):
    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)

max subarray product:
    cur_max = cur_min = best = a[0]
    for x in a[1:]:
        candidates = (x, cur_max * x, cur_min * x)
        cur_max, cur_min = max(candidates), min(candidates)
        best = max(best, cur_max)

count subarrays with sum K (with prefix-sum + hashmap):
    freq = {0: 1}; prefix = 0; count = 0
    for x in a:
        prefix += x
        count += freq.get(prefix - k, 0)
        freq[prefix] = freq.get(prefix, 0) + 1
```

Subpatterns in this folder:

- **01-Kadane** — classic max contiguous sum.
- **02-Max-product-subarray** — track running max AND min because of sign flips.
- **03-Subarray-with-XOR** — prefix-XOR + hashmap to count subarrays with XOR == K.

## Which problems this approach solves in the real world

- Best window of profitable trading in a price series.
- Largest contiguous block of healthy server pings.
- Maximum-energy span in a sensor reading.
- Best span of positive customer-satisfaction scores.
- Image processing: brightest contiguous region in a 1D scan.
- Audio signal processing: loudest run of samples.

## Pros and cons

**Pros**
- O(n) and O(1) — optimal in both dimensions.
- Easy to extend to track start and end indices.
- Generalises to circular arrays with a small twist.
- Combines cleanly with prefix sums for counting variants.

**Cons**
- The product variant must track min and max simultaneously — easy to forget.
- All-negative arrays need a careful base case (initialise from a[0], not 0).
- Doesn't extend to non-contiguous subsets.
- Circular variant needs handling of all-negative arrays specially.

## Limitations

- Cannot solve max-sum across non-contiguous indices (that's a different problem class).
- 2D max-subrectangle is more involved (Kadane per row pair).
- For weighted / constrained variants you may need DP.
- Streaming variants with sliding window need additional structures.
