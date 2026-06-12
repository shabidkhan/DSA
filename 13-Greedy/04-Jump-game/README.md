# Jump game

## What is this

Jump-game problems give an array `nums` where `nums[i]` is the maximum forward jump from index `i`. Variants ask: can you reach the last index? What is the minimum number of jumps? What is the lexicographically smallest jump path?

The greedy solution maintains `max_reach`, the farthest index reachable so far. Walk left to right; if `i > max_reach` you are stuck. For minimum jumps, also track the current jump's *boundary* — when `i` passes it, you commit a jump and re-set the boundary to `max_reach`.

## Why we use

- O(n) single pass for both "can reach" and "min jumps".
- O(1) extra memory.
- Greedy proof is short: extending the reach with current step is always at least as good as choosing any smaller jump.
- Foundation for jump-game variants (max points, lexicographically smallest path).

## How to implement (can-reach)

```
max_reach = 0
for i in 0..n-1:
    if i > max_reach: return False
    max_reach = max(max_reach, i + nums[i])
return True
```

```python
def can_jump(nums):
    max_reach = 0
    for i, x in enumerate(nums):
        if i > max_reach:
            return False
        if i + x > max_reach:
            max_reach = i + x
    return True
```

```python
def min_jumps(nums):
    n = len(nums)
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(n - 1):
        if i + nums[i] > farthest:
            farthest = i + nums[i]
        if i == cur_end:
            jumps += 1
            cur_end = farthest
            if cur_end >= n - 1:
                break
    return jumps
```

The "current boundary" variable separates "what is reachable with the *current* jump count" from "where could the *next* jump land".

## Which problems this approach solves in the real world

- Minimum hops in network routing with bounded link length.
- Minimum trip count under per-segment max distance.
- Optimal placement of refueling stops.
- Page-flip / paginator problems with per-section step sizes.
- Game-board step counting under variable die / move size.

## Pros and cons

**Pros**
- O(n) time, O(1) memory.
- Simple greedy with a one-line invariant.
- Generalizes to jump-game II (min hops) with one extra variable.

**Cons**
- Greedy doesn't extend to "minimum cost path" with non-uniform costs.
- Off-by-one between `n-1` and `n` in the loop bound is the classic bug.
- Lexicographic / pathwise variants need extra state.

## Limitations

- Backward jumps require a different formulation.
- Negative step sizes invalidate the monotone reach analysis.
- Streaming variant needs windowed `max_reach`.

## One example

**Problem**: Given an integer array `nums` where `nums[i]` is the maximum forward jump length from index `i`, return the minimum number of jumps needed to reach the last index. You may assume the last index is always reachable.

**Input**: `nums = [2, 3, 1, 1, 4]`
**Output**: `2`
**Constraints**: `1 <= n <= 10^4`, `0 <= nums[i] <= 1000`.

## Solution explanation

```python
def jump(nums):
    n = len(nums)
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
            if cur_end >= n - 1:
                break
    return jumps
```

Walkthrough on `nums = [2, 3, 1, 1, 4]`:

| i | nums[i] | farthest after | cur_end before | hit boundary? | jumps after |
|---|---------|----------------|----------------|---------------|-------------|
| 0 | 2       | 2              | 0              | yes           | 1           |
| 1 | 3       | 4              | 2              | no            | 1           |
| 2 | 1       | 4              | 2              | yes           | 2 (cur_end=4 ≥ 4) → break |

Return 2. Time: O(n). Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Jump Game (LeetCode 55) | https://leetcode.com/problems/jump-game/ |
| Medium | Jump Game II (LeetCode 45) | https://leetcode.com/problems/jump-game-ii/ |
| Hard | Jump Game IV (LeetCode 1345) | https://leetcode.com/problems/jump-game-iv/ |
