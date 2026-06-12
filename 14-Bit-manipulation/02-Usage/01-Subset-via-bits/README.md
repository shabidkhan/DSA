# Subsets via Bitmask Enumeration

## What is this

Subset-via-bits enumerates all 2^n subsets of an n-element list by iterating an integer mask from `0` to `(1 << n) - 1`. Each mask is a bit pattern where **bit i = 1** means "include element i" and **bit i = 0** means "exclude element i". Because every distinct integer in that range corresponds to a unique inclusion/exclusion vector, the integers themselves are a perfect index over the powerset.

Compared to recursive backtracking, the bitmask form is iterative, cache-friendly, and trivially parallelisable: each mask is independent. It is also the only practical way to do **subset DP** for n up to ~20, where masks become dictionary keys for memoizing per-subset state (e.g., Travelling Salesman, Bitmask DP).

## Why we use

- It turns subset enumeration into a single `for mask in range(1<<n)` loop — no recursion stack.
- The integer mask can be used as a hash key for **O(1)** subset-state lookup in DP.
- Bit operations (`mask & (1<<i)`, `__builtin_popcount`) are extremely fast at the CPU level.
- It composes cleanly with other bit tricks: subset-of-subset iteration, complement, lowest-bit isolation.

## How to implement

```
for mask in 0 .. (1<<n) - 1:
    subset = []
    for i in 0 .. n-1:
        if mask & (1 << i):
            subset.append(arr[i])
    process(subset)
```

```python
def all_subsets(nums):
    n = len(nums)
    out = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        out.append(subset)
    return out
```

```javascript
function allSubsets(nums) {
    const n = nums.length, out = [];
    for (let mask = 0; mask < (1 << n); mask++) {
        const subset = [];
        for (let i = 0; i < n; i++) {
            if (mask & (1 << i)) subset.push(nums[i]);
        }
        out.push(subset);
    }
    return out;
}
```

Invariant: bit `i` in `mask` corresponds to element `nums[i]`. The integer `mask` and the chosen subset are in one-to-one correspondence, so iterating masks once visits every subset exactly once.

## Which problems this approach solves in the real world

- Bitmask DP for TSP and assignment problems with n <= 20.
- Brute-force feature-flag exploration when the flag count is small.
- Enumerating role permission combinations for access-control matrix testing.
- Hardware test vectors over a fixed set of bit lines.
- Cost-minimization over small subsets of products/services.
- Generating power sets for combinatorics utilities in libraries.

## Pros and cons

**Pros**
- Iterative, no recursion or stack growth.
- Each subset has a canonical integer ID — perfect for DP memoisation.
- Easy to parallelise: split the mask range across workers.
- Very fast inner loop due to native bit operations.

**Cons**
- Hard limit: n must satisfy `1 << n` fitting in a machine word (n <= 30 in JS; n <= 62 in Python).
- Cost is fundamentally exponential — only viable for small n.
- The subset materialisation (`[nums[i] for ...]`) can dominate runtime; avoid when you can work directly with the mask.
- Off-by-one in `(1 << n)` is a classic bug.

## Limitations

- Not suitable for n > ~25; exponential blowup is unavoidable.
- Requires elements to be addressable by a fixed index 0..n-1.
- Encoding multi-state per element (3 choices per item) requires base-3 masks, not bitmasks.
- Subset-of-subset iteration is correct but trickier than naive `for s in 0..mask`.

## One example

**Problem**: Given an integer array `nums` of unique elements, return all possible subsets (the power set). The result must not contain duplicate subsets; order of subsets and elements does not matter.

Constraints: 1 <= n <= 10; -10 <= nums[i] <= 10; all `nums[i]` are unique.

**Input**: `nums = [1, 2, 3]`

**Output**: `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`

## Solution explanation

```python
def subsets(nums):
    n = len(nums)
    out = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        out.append(subset)
    return out
```

For `nums = [1,2,3]` we iterate `mask` from `0` to `7` (binary `000` to `111`):

| mask | binary | bit2 (val 3) | bit1 (val 2) | bit0 (val 1) | subset |
|------|--------|--------------|--------------|--------------|--------|
| 0 | 000 | - | - | - | [] |
| 1 | 001 | - | - | 1 | [1] |
| 2 | 010 | - | 2 | - | [2] |
| 3 | 011 | - | 2 | 1 | [1,2] |
| 4 | 100 | 3 | - | - | [3] |
| 5 | 101 | 3 | - | 1 | [1,3] |
| 6 | 110 | 3 | 2 | - | [2,3] |
| 7 | 111 | 3 | 2 | 1 | [1,2,3] |

Correctness: every subset of a finite set is uniquely determined by its characteristic vector (1 = in, 0 = out). The masks `0..2^n - 1` enumerate every such vector exactly once, so the output is the complete power set.

- **Time**: O(n * 2^n) to materialise; O(2^n) if you only need the masks.
- **Space**: O(n * 2^n) for the output; O(1) extra during iteration.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Medium | Subsets | https://leetcode.com/problems/subsets/ |
| Medium | Subsets II | https://leetcode.com/problems/subsets-ii/ |
| Hard | Partition to K Equal Sum Subsets | https://leetcode.com/problems/partition-to-k-equal-sum-subsets/ |
