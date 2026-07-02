# Opposite ends (left + right)

## What is this

A two-pointer technique where two indices start at **opposite ends** of a sorted (or symmetric) array — one at the leftmost element (`left = 0`), one at the rightmost (`right = n - 1`) — and walk toward each other based on a comparison rule. The pointers meet (or cross) when the scan is done, giving the algorithm a single linear pass.

## Why we use

- It collapses problems that look like O(n²) (pair sums, range queries) into **O(n) time, O(1) extra space**.
- It exploits an existing ordering (sorted input, palindrome symmetry, etc.) so you can rule out whole sub-ranges with one comparison.
- It avoids index arithmetic and nested loops, which makes the code small and easy to reason about.

## How to implement

```
left  = 0
right = n - 1
while left < right:
    examine arr[left] and arr[right]
    if some_condition is satisfied:
        record the result (or return)
    if we should grow the sum / move right side smaller:
        right -= 1
    else:
        left += 1
```

Python — classic two-sum on a sorted array:

```python
def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None
```

JavaScript — palindrome check:

```javascript
function isPalindrome(s) {
  let left = 0;
  let right = s.length - 1;
  while (left < right) {
    if (s[left] !== s[right]) return false;
    left += 1;
    right -= 1;
  }
  return true;
}
```

Invariant: everything **outside** `[left, right]` has already been validated; everything **inside** is still under consideration. The loop ends when the window is empty.

## Which problems this approach solves in the real world

- **Pair / triplet matching on sorted catalogs**: finding two products whose prices add to a target budget without scanning every pair.
- **Palindromic / mirror checks**: validating numeric account numbers or DNA strands that must read the same forwards and backwards.
- **Container / area maximisation**: choosing two reservoir walls to maximise water trapped between them (the classic "container with most water" problem).
- **Trimming / deduplicating sorted logs in place**: filtering or compacting a buffer without allocating a second array — useful in embedded or memory-constrained pipelines.
- **3-sum and k-sum reductions**: fixing one element and using opposite-ends two-pointer on the remainder is the standard way to find triples in O(n²) instead of O(n³).

## Pros and cons

**Pros**
- O(n) time, O(1) extra space.
- Each element is visited at most twice; trivial to reason about cache locality.
- Branch-light: usually two or three comparisons per iteration.
- Easy to combine with other techniques (sort + opposite-ends is the foundation of 3-sum / 4-sum).

**Cons**
- Requires sorted input (or a known symmetric structure). Sorting an unsorted array first is O(n log n), which can dominate.
- The "move which pointer" rule must be provably correct for the problem; an off-by-one logic bug silently returns the wrong answer.
- Doesn't generalise well to data structures without random indexed access (e.g. singly linked lists — use fast/slow pointers instead).

## Limitations

- Only works when the comparison at the two boundaries gives you enough information to **safely discard one side**. If you can't prove "moving `left` right never skips a valid answer", the technique doesn't apply.
- Cannot be used on a stream — both ends must be addressable.
- For multi-dimensional / non-linear data (graphs, trees), the analog is BFS or DFS, not opposite-ends.
- Sorted-input requirement means you may lose the original index ordering; preserve original indices alongside the value if the caller needs them.

## One example

**Problem**: Given a sorted array `nums` of integers and a target `t`, return the **indices** of two numbers whose sum equals `t`. Each input has exactly one solution. Constraints: `2 ≤ nums.length ≤ 2 × 10^4`, `-10^9 ≤ nums[i] ≤ 10^9`.

**Input**: `nums = [1, 3, 4, 5, 7, 11]`, `t = 9`
**Output**: `(1, 4)` because `nums[1] + nums[4] = 3 + 7 = 9`.

## Solution explanation

```python
def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int]:
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    raise ValueError("no pair sums to target")
```

Walk-through on `[1, 3, 4, 5, 7, 11]`, target = 9:

| step | left | right | sum | action |
|------|------|-------|-----|--------|
| 0    | 0 (1) | 5 (11) | 12 | sum > target → `right -= 1` |
| 1    | 0 (1) | 4 (7)  | 8  | sum < target → `left += 1`  |
| 2    | 1 (3) | 4 (7)  | 10 | sum > target → `right -= 1` |
| 3    | 1 (3) | 3 (5)  | 8  | sum < target → `left += 1`  |
| 4    | 2 (4) | 3 (5)  | 9  | **match — return (2, 3)**   |

The correctness argument: when `nums[left] + nums[right] < target`, the **only** way to grow the sum is to increase one of the operands. Since `nums[right]` is already the largest remaining candidate, the only useful move is `left += 1` — moving `right` left would only decrease the sum further. Symmetric reasoning for `sum > target`. Every move provably preserves the invariant "if a pair exists, it lies in `[left, right]`", so the algorithm terminates with the answer or proves none exists.

- **Time**: O(n) — each iteration moves one pointer; together they traverse the array once.
- **Space**: O(1) — two integer indices.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Valid Palindrome** — check if a string reads the same forwards and backwards, ignoring non-alphanumerics and case. | https://leetcode.com/problems/valid-palindrome/ |
| Easy | **Two Sum II - Input Array Is Sorted** — return 1-indexed positions of the two numbers in a sorted array that add up to a target. | https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/ |
| Easy | **Reverse String** — reverse a character array in place using two pointers swapping from both ends. | https://leetcode.com/problems/reverse-string/ |
| Easy | **Reverse Vowels of a String** — swap only the vowels in a string, leaving other characters in place. | https://leetcode.com/problems/reverse-vowels-of-a-string/ |
| Easy | **Squares of a Sorted Array** — given a sorted array, return a sorted array of the squares. (Largest squares come from extremes — fill output from the back.) | https://leetcode.com/problems/squares-of-a-sorted-array/ |
| Easy | **Merge Sorted Array** — merge `nums2` into `nums1` in place, filling from the right using two pointers from the ends of both arrays. | https://leetcode.com/problems/merge-sorted-array/ |
| Easy | **Valid Palindrome II** — return true if the string can become a palindrome by deleting at most one character. | https://leetcode.com/problems/valid-palindrome-ii/ |
| Easy | **Reverse Only Letters** — reverse only the alphabetic characters in a string, leaving non-letters in their original positions. | https://leetcode.com/problems/reverse-only-letters/ |
| Easy | **Sort Array By Parity** — rearrange the array so all even integers come before odd ones, using two pointers from each end. | https://leetcode.com/problems/sort-array-by-parity/ |
| Easy | **DI String Match** — reconstruct a permutation from an "I"/"D" pattern by picking the smallest remaining for "I" and the largest for "D". | https://leetcode.com/problems/di-string-match/ |
| Easy | **Intersection of Two Arrays II** — return the intersection of two arrays as a multiset. (Sort both, then walk two pointers inward from the starts/ends.) | https://leetcode.com/problems/intersection-of-two-arrays-ii/ |
| Medium | **Container With Most Water** — given `n` heights, find two lines that together with the x-axis form a container holding the most water. (Opposite ends; always move the shorter side inward.) | https://leetcode.com/problems/container-with-most-water/ |
| Medium | **3Sum** — return all unique triplets `(a, b, c)` in the array such that `a + b + c = 0`. (Sort, then fix one and opposite-ends the rest.) | https://leetcode.com/problems/3sum/ |
| Medium | **3Sum Closest** — find the triplet whose sum is closest to a target. (Same sort-fix-opposite-ends loop as 3Sum; track the closest seen sum.) | https://leetcode.com/problems/3sum-closest/ |
| Medium | **4Sum** — find all unique quadruplets summing to a target. (Sort, fix two elements with nested loops, then opposite-ends on the inner pair.) | https://leetcode.com/problems/4sum/ |
| Medium | **Valid Triangle Number** — count the number of triplets from a sorted array that can form a triangle. (Fix the largest side, then opposite-ends count pairs whose sum exceeds it.) | https://leetcode.com/problems/valid-triangle-number/ |
| Medium | **3Sum With Multiplicity** — count the number of ordered index triplets `(i, j, k)` with `arr[i] + arr[j] + arr[k] = target`. (Sort + fix + opposite-ends counting, accumulate pair frequencies.) | https://leetcode.com/problems/3sum-with-multiplicity/ |
| Medium | **Boats to Save People** — find the minimum number of boats to carry all people, each boat holding at most two if their total weight ≤ limit. (Sort; pair heaviest with lightest if possible using opposite ends.) | https://leetcode.com/problems/boats-to-save-people/ |
| Medium | **Bag of Tokens** — maximise token score: play face-up (spend power) or face-down (gain power). (Sort; opposite ends — greedily spend cheapest or buy with most expensive.) | https://leetcode.com/problems/bag-of-tokens/ |
| Medium | **Find K Closest Elements** — return the `k` closest integers to `x` from a sorted array. (Shrink a window from the ends: always remove whichever endpoint is farther from `x`.) | https://leetcode.com/problems/find-k-closest-elements/ |
| Medium | **Number of Subsequences That Satisfy the Given Sum Condition** — count subsequences where `min + max ≤ target`. (Sort; opposite-ends: when `nums[l] + nums[r] ≤ target`, all 2^(r−l) subsequences rooted at `l` qualify.) | https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/ |
| Hard | **Trapping Rain Water** — given an array of bar heights, compute how much water is trapped after raining. (Two pointers from each end tracking running max heights.) | https://leetcode.com/problems/trapping-rain-water/ |
