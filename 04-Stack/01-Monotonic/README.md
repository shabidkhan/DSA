# Monotonic stack

## Folder structure

```
01-Monotonic/
├── README.md
├── 01-Increasing/README.md
└── 02-Decreasing/README.md
```

## What is this

A monotonic stack maintains its elements in a strict (or non-strict) monotonic order — increasing or decreasing — by popping any element that would violate the order before pushing a new one. The popped elements typically yield the answer: the previous-or-next greater/smaller element for the popped index.

The technique runs in O(n) amortised time because each element is pushed and popped at most once. It is the standard tool for "next greater element", "largest rectangle in histogram", "daily temperatures", and many price-related problems.

## Why we use

- O(n) for problems that look quadratic ("for each element find nearest larger/smaller")
- Constant per-element work after amortisation
- Same skeleton solves four families: prev-greater, prev-smaller, next-greater, next-smaller
- Foundation for histogram/skyline and span queries

## How to implement

```
Next greater element (decreasing stack of indices):
    stack = []
    result = [-1] * n
    for i in 0..n-1:
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result
```

```python
def next_greater(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack: list[int] = []
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result
```

Largest rectangle in a histogram (classic monotonic-stack problem):

```python
def largest_rectangle(heights: list[int]) -> int:
    stack: list[int] = []   # indices of increasing heights
    best = 0
    heights = heights + [0]  # sentinel to flush the stack
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            top = stack.pop()
            left = stack[-1] if stack else -1
            width = i - left - 1
            best = max(best, heights[top] * width)
        stack.append(i)
    return best
```

Invariant for the increasing-stack variant: the values on the stack (read bottom-to-top) are strictly increasing. When a smaller value arrives, every popped element knows that the current value is its "next smaller", and the new top of stack (after the pop) is its "previous smaller".

## Which problems this approach solves in the real world

- Stock-span / price analysis: "how many days back was today's price first surpassed?"
- Histogram-area computations in image processing and chart rendering
- Skyline silhouette detection from a series of building heights
- Temperature warming-day queries in weather dashboards
- Browser-style "next bigger pop-up" rules in UI event handling

## Pros and cons

**Pros**
- O(n) amortised; each element pushed and popped once
- Tiny memory: O(n) for the stack at worst
- Easy to adapt by flipping comparisons for the four monotonic variants

**Cons**
- Off-by-one errors common in width/index arithmetic
- Strict vs non-strict comparisons subtly change results (handle equal values carefully)
- Doesn't generalise to multi-criteria comparisons (only one ordering at a time)

## Limitations

- Cannot handle online deletions from arbitrary positions
- Only one monotonic property per stack — multi-property problems need multiple stacks
- Range queries beyond "nearest greater/smaller" usually need segment trees instead

## One example

Problem: Given an array `temperatures` where `temperatures[i]` is the temperature on day `i`, return an array `answer` such that `answer[i]` is the number of days you have to wait after day `i` to get a warmer temperature. If no such day exists, set `answer[i] = 0`.

```
Input:  temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1, 1, 4, 2, 1, 1, 0, 0]
Constraints: 1 <= len(temperatures) <= 10^5, 30 <= temperatures[i] <= 100
```

## Solution explanation

```python
def daily_temperatures(temps: list[int]) -> list[int]:
    n = len(temps)
    answer = [0] * n
    stack: list[int] = []   # indices with non-increasing temperatures
    for i in range(n):
        while stack and temps[stack[-1]] < temps[i]:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer
```

Maintain a decreasing-by-temperature stack of indices. When today's temperature is warmer than the top, the top's "next warmer day" is today; pop and record the gap.

Walkthrough for `temps = [73, 74, 75, 71, 69, 72, 76, 73]`:

| i | temps[i] | stack before | pops (j -> answer[j])           | stack after |
|---|----------|--------------|----------------------------------|-------------|
| 0 | 73       | []           | —                                | [0]         |
| 1 | 74       | [0]          | 0 -> 1                           | [1]         |
| 2 | 75       | [1]          | 1 -> 1                           | [2]         |
| 3 | 71       | [2]          | —                                | [2, 3]      |
| 4 | 69       | [2, 3]       | —                                | [2, 3, 4]   |
| 5 | 72       | [2, 3, 4]    | 4 -> 1, 3 -> 2                   | [2, 5]      |
| 6 | 76       | [2, 5]       | 5 -> 1, 2 -> 4                   | [6]         |
| 7 | 73       | [6]          | —                                | [6, 7]      |

Remaining indices `[6, 7]` keep `answer = 0`. Final: `[1, 1, 4, 2, 1, 1, 0, 0]`. Time O(n), space O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Next Greater Element I (LeetCode 496) | https://leetcode.com/problems/next-greater-element-i/ |
| Medium | Daily Temperatures (LeetCode 739) | https://leetcode.com/problems/daily-temperatures/ |
| Hard | Largest Rectangle in Histogram (LeetCode 84) | https://leetcode.com/problems/largest-rectangle-in-histogram/ |
