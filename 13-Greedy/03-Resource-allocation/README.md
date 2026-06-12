# Resource Allocation

## Folder structure

```
03-Resource-allocation/
├── README.md
├── 01-Min-platforms/README.md
└── 02-Meeting-rooms/README.md
```

## What is this

Resource-allocation greedy answers "how many resources do I need to satisfy all requests?" — given a set of intervals or events, count the peak number of concurrent occupants. The two implementation techniques are the **sweep line** (split each interval into a `+1` start event and a `-1` end event, sort by time, accumulate a running counter, track its maximum) and the **min-heap of end times** (sort intervals by start; for each interval pop ended ones, then push the new end; the heap size is the rooms in use).

The result is the chromatic number of the interval graph, which for intervals equals the maximum clique, which equals the peak concurrency — a rare moment where a greedy count is provably optimal. That equivalence means the sweep-line answer is exact, not an approximation, and there is no need to consider sophisticated assignment strategies; allocation is forced by counting.

## Why we use

- Computes the minimum number of resources without enumeration
- Linear after sorting, so O(n log n) end to end
- The heap variant also gives a valid assignment (which room each meeting uses)
- Generalizes to "can one person attend everything?" as the same scan with a different reporter

## How to implement

```text
# Sweep-line (count peak only)
function minRooms(intervals):
    events = []
    for [s, e] in intervals:
        events.append((s, +1))
        events.append((e, -1))
    sort events by (time, delta)   # -1 before +1 ties to reuse rooms
    peak = current = 0
    for (_, d) in events:
        current += d
        peak = max(peak, current)
    return peak

# Heap-of-end-times (also gives assignment)
function minRoomsHeap(intervals):
    sort intervals by start ascending
    heap = min-heap of end times
    for [s, e] in intervals:
        if heap not empty and heap.top <= s:
            heap.pop()  # reuse that room
        heap.push(e)
    return heap.size
```

Subpatterns in this folder:

- **01-Min-platforms** — train arrivals/departures at a station; peak concurrent occupancy = platforms required
- **02-Meeting-rooms** — interview classic: I (can one person attend all?), II (how many rooms?), each reduces to this pattern

## Which problems this approach solves in the real world

- Sizing a meeting-room pool for a calendar of bookings
- Sizing a fleet (taxis, ambulances, delivery vehicles) for known demand
- Picking server pool size from request-arrival/departure logs
- Counting peak concurrent connections on a network port
- Planning platform count at a station from train timetable
- Sizing parallel-build agents from job arrival/duration logs

## Pros and cons

**Pros**

- O(n log n) — the sort dominates
- Two equivalent implementations; pick the one your team finds clearest
- Heap variant also produces a feasible assignment, not just a count
- Provably optimal — no approximation gap

**Cons**

- Both variants require care with inclusive vs exclusive end times
- Sweep-line tie-breaking (end-before-start vs start-before-end) flips answers
- Doesn't model setup/teardown between sequential users of the same room
- Doesn't handle heterogeneous rooms (different capacities or features)

## Limitations

- Resource is fungible; can't model "Alice can only use Room A"
- Doesn't optimize for fairness or any secondary objective
- Adding hard deadlines or arrival-order constraints moves the problem out of pure greedy
- Multi-dimensional capacity (rooms + projectors) needs a different formulation
