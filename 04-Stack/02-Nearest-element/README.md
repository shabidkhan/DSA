# Nearest-element Patterns

## Folder structure

```
02-Nearest-element/
├── README.md
├── 01-Next-greater/README.md
├── 02-Next-smaller/README.md
└── 03-Previous-variants/README.md
```

## What is this

Nearest-element problems ask, for each index in an array, "what is the nearest element to my left/right that is greater/smaller/equal under some predicate?". The naive answer is O(n²) (scan back/forward from each index). A monotonic stack solves the entire family in O(n) total: maintain a stack that's increasing or decreasing depending on the variant, push and pop as the scan progresses, and record the answer at pop time (or at the new push, depending on direction).

The four canonical variants — Next Greater, Next Smaller, Previous Greater, Previous Smaller — all share the same five-line skeleton. Once you've internalised the "pop while monotone-broken; record at pop" pattern, every variant is a one-character tweak (`>` vs `<`, left-to-right vs right-to-left).

## Why we use

- Collapses O(n²) naive scans to O(n) total with a single auxiliary stack.
- Each element is pushed and popped at most once — amortised O(1) per element.
- Uniform skeleton across all four variants (Next/Prev × Greater/Smaller).
- Pairs with arrays, sliding windows, and histograms for compound problems.

## How to implement

```
Next Greater Element (right-to-left, decreasing stack):
    res = [-1] * n
    stack = []
    for i from n-1 down to 0:
        while stack and stack[-1] <= a[i]: stack.pop()
        if stack: res[i] = stack[-1]
        stack.append(a[i])
    return res

(equivalent left-to-right, recording at pop:)
    res = [-1] * n
    stack = []                       # holds indices
    for i in 0..n-1:
        while stack and a[stack[-1]] < a[i]:
            res[stack.pop()] = a[i]
        stack.append(i)
    return res

To switch variants:
    > ↔ <        : Greater ↔ Smaller
    direction    : Next ↔ Previous
    inclusive    : <= or >= on the pop condition
```

Subpatterns in this folder:

- **01-Next-greater** — for each i, the next element to its right that is strictly greater.
- **02-Next-smaller** — for each i, the next element to its right that is strictly smaller.
- **03-Previous-variants** — Previous Greater / Previous Smaller, computed by mirroring the scan direction.

## Which problems this approach solves in the real world

- Stock-span and trading metrics (next higher close, previous lower).
- UI layout: nearest taller column for tooltips and overlays.
- Histogram-area problems (Largest Rectangle in Histogram).
- Daily temperature spikes / drops in monitoring.
- Order-book "nearest bid above" or "ask below".
- Skyline contour generation.

## Pros and cons

**Pros**
- O(n) total, O(n) extra space — optimal for the problem class.
- Single skeleton handles all four variants.
- Stack-only memory; no hashmaps or auxiliary structures needed.
- Amortised analysis is clean: each element is pushed/popped once.

**Cons**
- Direction errors (left vs right, greater vs smaller) are the top bug class.
- Inclusivity of comparison (`>` vs `>=`) silently flips ties.
- Storing indices vs values has different downstream uses — pick one consistently.
- Compound queries (e.g., "next greater within k") need extra bookkeeping.

## Limitations

- Doesn't answer "next K greater elements" — that needs different structures.
- Range-bounded variants (within a window) need monotone deque, not stack.
- 2D nearest-element queries need per-row / per-column passes.
- For sparse data, segment trees may be more flexible.
