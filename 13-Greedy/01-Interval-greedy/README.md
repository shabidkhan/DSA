# Interval Greedy

## Folder structure

```
01-Interval-greedy/
├── README.md
├── 01-Activity-selection/README.md
├── 02-Non-overlapping/README.md
├── 03-Min-removals/README.md
└── 04-Interval-scheduling/README.md
```

## What is this

Interval greedy is a family of greedy strategies that operate on a collection of intervals (each a `[start, end]` pair) and pick or discard intervals in a fixed order to optimize some count or coverage. The defining trick is the sort key: sort by **earliest end time** when you want to fit the most non-overlapping intervals, sort by **earliest start time** when you scan for conflicts in time order, and sort by **length** or **start** when the goal is coverage.

The reason these problems yield to greedy is a clean exchange argument: at every step, committing to the locally best choice (the interval that ends first, the one that starts first) cannot lose any feasible solution. Replacing any optimal interval with the greedy pick keeps the answer valid and frees up the most remaining room for future picks. That property removes the need for DP or backtracking; one sort plus one linear scan solves the problem.

## Why we use

- Reduces interval-scheduling problems to O(n log n) sort + O(n) sweep
- Avoids exponential search over subsets of intervals
- Works without lookahead — each decision uses only the current interval and one piece of state
- The sort key encodes the optimality argument directly, making correctness easy to reason about

## How to implement

```text
function maxNonOverlapping(intervals):
    sort intervals by end ascending
    count = 0
    lastEnd = -infinity
    for each [s, e] in intervals:
        if s >= lastEnd:
            count += 1
            lastEnd = e
    return count
```

Variants change only the comparison and the accumulator:

```text
# count REMOVALS needed instead of kept
removals = n - maxNonOverlapping(intervals)

# detect any conflict in time order
sort by start ascending
for each [s, e]:
    if s < prevEnd: report conflict
```

Subpatterns in this folder:

- **01-Activity-selection** — classic "maximum non-overlapping intervals" via earliest-end-time sort
- **02-Non-overlapping** — count the largest subset of mutually compatible intervals
- **03-Min-removals** — flip side of activity selection: minimum intervals to delete to make the rest compatible
- **04-Interval-scheduling** — general framework covering both maximize-kept and minimize-removed phrasings

## Which problems this approach solves in the real world

- Conference room single-track scheduling
- CPU job scheduling without preemption
- Booking maximum number of non-overlapping reservations
- Selecting non-overlapping ad slots in a broadcast window
- Choosing a maximum set of non-conflicting tasks for one worker
- Cleaning a calendar by removing the fewest conflicting events

## Pros and cons

**Pros**

- Linear scan after sorting — O(n log n) total
- O(1) extra state beyond the sorted array
- Proofs are short (exchange argument)
- Composes well: same scan handles "keep max" and "remove min"

**Cons**

- Picks one specific optimum; ties can hide alternative valid plans
- Wrong sort key (e.g., earliest start) silently produces wrong answers
- Doesn't return the schedule's structure unless you also track picks
- Adapting to weighted intervals usually breaks greedy and requires DP

## Limitations

- Fails when intervals carry weights — use weighted interval scheduling (DP) instead
- Cannot handle resource counts > 1; that becomes a heap / sweep-line problem
- Sensitive to inclusive vs exclusive end-time conventions
- Doesn't extend to 2D intervals (rectangles) without additional structure
