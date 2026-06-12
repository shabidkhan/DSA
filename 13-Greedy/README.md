# Greedy Patterns

## Folder structure

```
13-Greedy/
├── README.md
├── 01-Interval-greedy/
│   ├── 01-Activity-selection/README.md
│   ├── 02-Non-overlapping/README.md
│   ├── 03-Min-removals/README.md
│   └── 04-Interval-scheduling/README.md
├── 02-Scheduling-greedy/
│   ├── 01-Deadline-based/README.md
│   └── 02-Profit-based/README.md
├── 03-Resource-allocation/
│   ├── 01-Min-platforms/README.md
│   └── 02-Meeting-rooms/README.md
├── 04-Jump-game/README.md
└── 05-Huffman-merge-cost/README.md
```

## What is this

A greedy algorithm makes the locally optimal choice at each step and proves (via an exchange argument or matroid theory) that the resulting sequence of local choices is globally optimal. Greedy is faster, simpler, and uses less memory than DP — but it only works when the problem has the "greedy choice property". When it does, you get O(n log n) or even O(n) solutions to problems that would otherwise need DP.

The five families here are: interval greedy (activity selection, non-overlapping intervals, min removals), scheduling greedy (deadline-driven, profit-driven), resource allocation (min platforms, meeting rooms), Jump Game, and Huffman / merge-cost greedies. The unifying skeleton is "sort by the right key, then make one pass keeping a running invariant".

## Why we use

- O(n log n) solutions to problems that DP would solve in O(n²) or worse.
- One pass, one running variable — minimal memory footprint.
- Provably optimal when the greedy-choice property holds.
- Each subpattern has a recognisable "sort by X" trick that unlocks the solution.

## How to implement

```
1. Identify the greedy choice (sort by end? sort by start? sort by deadline?).
2. Prove (or trust) the exchange argument.
3. One pass:
       for item in sorted_items:
           if item compatible with current state:
               accept
           else:
               reject (or replace, for some variants)
4. Return the accumulated answer.
```

Subpatterns in this folder:

- **01-Interval-greedy** — activity selection, non-overlapping intervals, min removals, interval scheduling.
- **02-Scheduling-greedy** — deadline-based, profit-based.
- **03-Resource-allocation** — minimum platforms, meeting rooms.
- **04-Jump-game** — reach-end with min jumps / can-reach.
- **05-Huffman-merge-cost** — Huffman coding and minimum-merge-cost problems.

## Which problems this approach solves in the real world

- Airline gate / runway allocation (minimum platforms).
- Job scheduling on a single machine to maximise profit / minimise tardiness.
- Bandwidth allocation in networking.
- Coin-change for canonical coin systems (greedy works for USD).
- Disk-arm scheduling (SCAN, C-SCAN).
- File compression (Huffman in zip, JPEG, PNG).

## Pros and cons

**Pros**
- O(n log n) typical complexity; O(1) extra space.
- Trivial to implement once the sort key is known.
- Proofs are short when they exist.
- Easy to combine with heaps for online variants.

**Cons**
- Doesn't work for every problem — you must prove the greedy choice.
- Wrong sort key gives wrong results silently.
- Subtle edge cases on equality / ties.
- Hard to know in advance whether greedy or DP is right — requires intuition.

## Limitations

- Coin change with arbitrary denominations needs DP, not greedy.
- Knapsack 0/1 needs DP; only fractional knapsack is greedy.
- Problems with weighted intervals usually need DP.
- Greedy on adversarial inputs can produce arbitrarily bad results without a proof.
