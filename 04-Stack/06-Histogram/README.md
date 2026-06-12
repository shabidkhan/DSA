# Histogram (largest rectangle)

## What is this

The histogram pattern finds the largest rectangle that can be formed using consecutive bars in a histogram, where bar widths are 1 and heights are given by an array. A monotonic increasing stack of indices solves it in O(n): we pop a bar `h` only when a strictly smaller bar appears, at which point we know `h`'s "right boundary" is the current index and its "left boundary" is the index now on top of the stack.

This same pattern unlocks "maximal rectangle in a binary matrix" by treating each row as a histogram of column heights above it.

## Why we use

- O(n) — every bar pushed and popped at most once.
- Resolves left and right boundaries for every bar simultaneously.
- Extends to 2D for maximal rectangles in matrices.
- Foundation for "rain water trapped" and similar pile / boundary problems.

## How to implement

```
stack = []        # indices, heights strictly increasing
best = 0
for i in 0..n:
    h = heights[i] if i < n else 0   # sentinel
    while stack and heights[stack[-1]] > h:
        top = stack.pop()
        height = heights[top]
        width = i if not stack else i - stack[-1] - 1
        best = max(best, height * width)
    stack.append(i)
return best
```

```python
def largest_rectangle(heights):
    heights.append(0)         # sentinel forces final pop
    stack = []
    best = 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            top = stack.pop()
            height = heights[top]
            width = i if not stack else i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    heights.pop()
    return best
```

```python
def maximal_rectangle(matrix):
    if not matrix or not matrix[0]: return 0
    cols = len(matrix[0])
    heights = [0] * cols
    best = 0
    for row in matrix:
        for c in range(cols):
            heights[c] = heights[c] + 1 if row[c] == '1' else 0
        best = max(best, largest_rectangle(heights[:]))
    return best
```

The sentinel `0` at the end forces every remaining bar to be popped and finalized.

## Which problems this approach solves in the real world

- Maximal-area rectangle in image segmentation masks.
- Maximum-rate sustainable throughput across capacity bars.
- Heatmap-based hotspot detection by treating intensities as bar heights.
- Job-scheduling Gantt-chart "longest consecutive period at capacity ≥ X".
- Stress / load tolerance analysis on time-series staircases.

## Pros and cons

**Pros**
- O(n) — strictly better than O(n^2) brute force.
- Single pass with a clean invariant.
- Lifts to 2D for matrix problems.

**Cons**
- Monotonic-stack invariant is subtle.
- Sentinel handling is the most common bug.
- Index arithmetic for the width.

## Limitations

- Requires integer indices and non-negative heights.
- Streaming variant is awkward — you don't know future minima.
- Floating-point heights work but careful comparisons needed.

## One example

**Problem**: Given an array of integers `heights` representing histogram bar heights where the width of each bar is 1, return the area of the largest rectangle.

**Input**: `heights = [2, 1, 5, 6, 2, 3]`
**Output**: `10`
**Constraints**: `1 <= n <= 10^5`, `0 <= heights[i] <= 10^4`.

## Solution explanation

```python
def largestRectangleArea(heights):
    heights.append(0)
    stack = []
    best = 0
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            top = stack.pop()
            height = heights[top]
            width = i if not stack else i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    heights.pop()
    return best
```

Walkthrough on `[2, 1, 5, 6, 2, 3]` (with sentinel 0):

| i | h | stack before | pops & areas         | stack after   |
|---|---|--------------|----------------------|---------------|
| 0 | 2 | []           | -                    | [0]           |
| 1 | 1 | [0]          | pop 0: 2*1=2         | [1]           |
| 2 | 5 | [1]          | -                    | [1, 2]        |
| 3 | 6 | [1, 2]       | -                    | [1, 2, 3]     |
| 4 | 2 | [1, 2, 3]    | pop 3: 6*1=6; pop 2: 5*2=10 | [1, 4] |
| 5 | 3 | [1, 4]       | -                    | [1, 4, 5]     |
| 6 | 0 (sent) | [1, 4, 5] | pop 5: 3*1=3; pop 4: 2*4=8; pop 1: 1*6=6 | [6] |

Best = 10. Time: O(n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Trapping Rain Water II (related concept) — Easy: Make Array Strictly Increasing? Use simpler bar question | https://leetcode.com/problems/trapping-rain-water/ |
| Medium | Maximal Rectangle (LeetCode 85) | https://leetcode.com/problems/maximal-rectangle/ |
| Hard | Largest Rectangle in Histogram (LeetCode 84) | https://leetcode.com/problems/largest-rectangle-in-histogram/ |
