# Scheduling Greedy

## Folder structure

```
02-Scheduling-greedy/
├── README.md
├── 01-Deadline-based/README.md
└── 02-Profit-based/README.md
```

## What is this

Scheduling greedy covers problems where each job has a profit (or penalty) and a deadline, and you must choose a subset and an order that respects deadlines while maximizing profit. The optimal strategy combines two ideas: process jobs in **decreasing order of profit** (so the most valuable jobs get first claim on a slot) and use a structure — a boolean slot array, a min-heap, or a union-find — to track which time slots are still free.

The greedy is correct because any feasible schedule that omits a high-profit job in favor of a lower-profit one can be improved by swapping them, as long as the swap doesn't break the deadlines of the rest. That exchange argument is the backbone of every job-sequencing-with-deadlines proof, and it generalizes naturally to the variant where you can preempt and replace a previously scheduled cheaper job with a newly arriving more valuable one (the heap-based version).

## Why we use

- Maximizes total profit without enumerating subsets
- Handles unit-time jobs cleanly in O(n log n)
- The heap variant supports streaming arrivals: keep top-k profitable jobs that still fit
- Avoids the exponential blowup of "try every order"

## How to implement

```text
# Deadline-based, unit-time jobs
function jobSequencing(jobs):
    sort jobs by profit descending
    maxDeadline = max(j.deadline for j in jobs)
    slot = array of size maxDeadline filled with empty
    total = 0
    for j in jobs:
        for t = min(maxDeadline, j.deadline) down to 1:
            if slot[t] is empty:
                slot[t] = j
                total += j.profit
                break
    return total
```

```text
# Profit-based with heap (course schedule III style)
function maxJobs(courses):
    sort by deadline ascending
    heap = max-heap (or by duration)
    time = 0
    for [duration, deadline] in courses:
        time += duration
        push duration into heap
        while time > deadline:
            time -= heap.pop()  # drop the longest-so-far
    return heap.size
```

Subpatterns in this folder:

- **01-Deadline-based** — sort by deadline, schedule jobs in their latest possible slot; uses a slot array or union-find for the "find latest free slot ≤ d" query
- **02-Profit-based** — sort by profit descending; the heap variant accepts each job tentatively and evicts the worst one when capacity is exceeded

## Which problems this approach solves in the real world

- Scheduling marketing offers each with a redemption deadline and revenue
- CPU batch processing where each task has a hard deadline and a value
- Choosing the most profitable orders to fulfill before delivery cutoffs
- Course-schedule planning under a time budget
- Print-queue ordering when each job has a "must-print-by" time
- Selecting which freelance gigs to take when each pays differently and has a deadline

## Pros and cons

**Pros**

- O(n log n) total time using a heap or sort
- Easy to extend to streaming: the heap variant accepts arrivals online
- Proof generalizes the activity-selection exchange argument
- No DP table; constant extra memory beyond the heap

**Cons**

- Assumes unit-time jobs (or single-machine, non-preemptive); multi-machine versions need different structures
- Tie-breaking between equal profits is implementation-defined
- Slot-array form is wasteful when deadlines are huge — union-find is cleaner
- "Best schedule" is one of many; doesn't enumerate alternatives

## Limitations

- Multi-machine scheduling becomes NP-hard for general processing times
- Variable-duration jobs require the heap-eviction variant, not the slot variant
- Doesn't handle dependencies between jobs — that's topological-sort territory
- Penalties for missing deadlines (instead of zero profit) need a different formulation
