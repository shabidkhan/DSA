# Binary search on the answer

## What is this

A technique where, instead of binary-searching over an **index** in a sorted array, you binary-search over the **value of the answer itself**. You define a candidate answer space `[lo, hi]`, and for each candidate `mid`, you run a `feasible(mid)` check that answers a yes/no question monotonically in `mid` (once it flips from false to true — or true to false — it stays). Then you converge on the smallest (or largest) feasible value in O(log(range) × cost(feasible)).

## Why we use

- Turns optimisation problems ("minimum capacity such that…", "largest k such that…") into a sequence of decision problems, each of which is much simpler.
- Replaces brute-force scans over the answer space with a logarithmic number of feasibility checks.
- Works on continuous answer spaces (binary search on doubles) and on discrete ones (integer answers) with the same skeleton.

## How to implement

```
lo, hi = minimum_possible_answer, maximum_possible_answer
while lo < hi:
    mid = lo + (hi - lo) // 2
    if feasible(mid):
        hi = mid          # mid works → try smaller
    else:
        lo = mid + 1      # mid doesn't work → must be larger
return lo
```

Python — minimum eating speed (Koko Eating Bananas style):

```python
import math

def min_speed(piles: list[int], hours: int) -> int:
    def can_finish(speed: int) -> bool:
        return sum(math.ceil(p / speed) for p in piles) <= hours

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_finish(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Invariant: at the end of every iteration, `lo` is "still possibly the answer or below it", and `hi` is "definitely feasible or just past the feasible boundary". The monotonicity of `feasible` is the only correctness requirement — if it isn't monotonic, the technique doesn't apply.

## Which problems this approach solves in the real world

- **Capacity planning**: minimum number of servers / trucks / shifts needed to clear a known workload within a deadline.
- **Rate limiting**: smallest request-per-second limit that keeps p99 latency under threshold (the feasibility check is a simulation).
- **Resource allocation**: smallest budget per group such that everyone gets at least their requirement.
- **Manufacturing tolerances**: largest part diameter such that all tolerance constraints still pass — feasibility runs the engineering check.
- **Scheduling deadlines**: smallest time bound `T` such that all jobs can be completed by `T`.

## Pros and cons

**Pros**
- Reduces a search over a huge answer range (up to `10^18`) to ~60 feasibility checks.
- Decouples optimisation from feasibility — you write the simpler "does X work?" function and the binary search handles the optimisation.
- Same code skeleton for "minimum feasible" and "maximum feasible" — just flip the `feasible` direction.

**Cons**
- Requires monotonicity. If `feasible(x)` is not monotonic in `x`, this fails silently with a wrong answer.
- The feasibility function must be cheap relative to the answer range — if `feasible` is O(n²) and the range is `10^9`, you're at ~60·n² which can still be slow.
- Bounding `lo` and `hi` correctly is sometimes subtle; if your bounds exclude the real answer, you'll converge on a wrong value.

## Limitations

- Doesn't apply when the answer space is not totally ordered (e.g. multi-objective optimisation).
- Floating-point versions require choosing a precision (`hi - lo < eps`) and can suffer accumulated error.
- If `feasible` itself requires global state (e.g. a graph rebuild), the constant factor may make a smarter algorithm preferable.

## One example

**Problem**: A conveyor belt ships packages within `D` days. Package `i` has weight `weights[i]`. The ship loads packages in order and its capacity must be the same every day. Return the **least** ship capacity that ships all packages within `D` days. Constraints: `1 ≤ D ≤ weights.length ≤ 5·10^4`, `1 ≤ weights[i] ≤ 500`.

**Input**: `weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`, `D = 5`
**Output**: `15`

## Solution explanation

```python
def ship_within_days(weights: list[int], D: int) -> int:
    def days_needed(capacity: int) -> int:
        days, load = 1, 0
        for w in weights:
            if load + w > capacity:
                days += 1
                load = 0
            load += w
        return days

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if days_needed(mid) <= D:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Walk-through on `weights = [1,...,10]`, D = 5. Answer space starts as `[10, 55]`.

| step | lo | hi | mid | days_needed(mid) | action |
|------|----|----|-----|------------------|--------|
| 0    | 10 | 55 | 32  | 2                | feasible → `hi = 32` |
| 1    | 10 | 32 | 21  | 3                | feasible → `hi = 21` |
| 2    | 10 | 21 | 15  | 5                | feasible → `hi = 15` |
| 3    | 10 | 15 | 12  | 6                | infeasible → `lo = 13` |
| 4    | 13 | 15 | 14  | 6                | infeasible → `lo = 15` |
| 5    | 15 | 15 | —   | —                | converged → **15** |

The lower bound `max(weights)` is the smallest physically possible capacity (must fit the heaviest single package). The upper bound `sum(weights)` is the trivial "ship everything in one day". The feasibility check is a greedy simulation: pack until you'd overflow, then start a new day. Monotonicity holds because more capacity can only reduce (or keep equal) the required days.

- **Time**: O(n · log(sum(weights))) — about 60 simulations of O(n) each.
- **Space**: O(1) — counters only.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy   | **Sqrt(x)** — return `floor(sqrt(x))` using binary search on the answer. | https://leetcode.com/problems/sqrtx/ |
| Medium | **Koko Eating Bananas** — find the minimum eating speed (bananas/hour) to finish piles within `h` hours. | https://leetcode.com/problems/koko-eating-bananas/ |
| Hard   | **Split Array Largest Sum** — split into `m` subarrays minimising the largest subarray sum. | https://leetcode.com/problems/split-array-largest-sum/ |
