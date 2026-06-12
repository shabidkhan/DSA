# Bitmask dynamic programming

## What is this

Bitmask DP encodes a subset of up to ~20 elements as an integer where bit `k` is set if element `k` is included. The state is typically `dp[mask]` or `dp[i][mask]`, where the bitmask compactly represents "which items have been used / visited so far". Transitions flip a single bit to mark inclusion or exclusion.

The pattern works when the number of relevant items is small (usually n <= 20-22), because there are only `2^n` subsets. Each subset can be evaluated against neighbours that differ by one bit, giving polynomial-time algorithms for problems that are exponential in the worst case but still feasible at small n.

## Why we use

- Encodes "which subset is taken" in a single machine word
- Bitwise operations make subset transitions O(1)
- Replaces nested set-membership checks with single bit tests
- Makes problems like Travelling Salesman tractable at n <= 20

## How to implement

```
1. Map each element to a bit position 0..n-1
2. Define dp[mask] = best/count answer using exactly the elements in mask
3. Iterate masks in increasing numeric order (subset DP) or use BFS over states
4. For each mask, try adding/removing one element using bitwise ops:
     new_mask = mask | (1 << k)   # add element k
     has_k    = mask & (1 << k)   # test element k
5. Return dp[(1 << n) - 1] (full mask) or aggregate as needed
```

Count number of ways to assign n people to n jobs (each person does exactly one job, cost matters):

```python
def assign_jobs(cost: list[list[int]]) -> int:
    n = len(cost)
    INF = float("inf")
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        i = bin(mask).count("1")  # next person to assign
        if i == n:
            continue
        for j in range(n):
            if not (mask & (1 << j)):
                new_mask = mask | (1 << j)
                dp[new_mask] = min(dp[new_mask], dp[mask] + cost[i][j])
    return dp[(1 << n) - 1]
```

Travelling Salesman (minimum-cost Hamiltonian cycle starting at 0):

```python
def tsp(dist: list[list[int]]) -> int:
    n = len(dist)
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0
    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF or not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])
    full = (1 << n) - 1
    return min(dp[full][v] + dist[v][0] for v in range(1, n))
```

Invariant: `dp[mask][v]` is final once every mask with fewer bits has been processed, because transitions only add bits.

## Which problems this approach solves in the real world

- Vehicle routing for small fleets (TSP with up to ~20 stops)
- Optimal job/person assignment in small teams
- Bitmask scheduling of dependent tasks on a single machine
- DNA fragment assembly when fragments are few but combinations explode
- Circuit synthesis: covering boolean functions with a minimal set of gates

## Pros and cons

**Pros**
- Compact representation: a 20-element subset fits in one int
- Bitwise transitions are constant-time and cache-friendly
- Often the only polynomial-ish way to handle "subset of items" state

**Cons**
- Hard cap around n <= 22 due to `2^n` blow-up
- Bitmask code is dense and easy to off-by-one
- Reconstructing the chosen subset needs backpointers

## Limitations

- Infeasible above ~22 elements due to memory and time
- Requires that the order of inclusion can be normalized (otherwise state space explodes)
- Not suitable when elements are continuous or unbounded

## One example

Problem: Given `n` workers and `n` tasks with a cost matrix `cost[i][j]` for worker `i` doing task `j`, assign each worker to exactly one distinct task minimizing total cost.

```
Input:  cost = [[9, 2, 7], [6, 4, 3], [5, 8, 1]]
Output: 7    (worker 0 -> task 1, worker 1 -> task 0, worker 2 -> task 2: 2 + 6 + 1 = 9 NO;
              actually worker 0 -> task 1, worker 1 -> task 2, worker 2 -> task 0 = 2 + 3 + 5 = 10;
              optimal is worker 0 -> task 1 (2), worker 1 -> task 2 (3), worker 2 -> task 0 (5) = 10... see walkthrough)
Constraints: 1 <= n <= 20, 0 <= cost[i][j] <= 10^4
```

## Solution explanation

```python
def min_assignment(cost: list[list[int]]) -> int:
    n = len(cost)
    INF = float("inf")
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        i = bin(mask).count("1")
        if i == n:
            continue
        for j in range(n):
            if not (mask & (1 << j)):
                dp[mask | (1 << j)] = min(dp[mask | (1 << j)], dp[mask] + cost[i][j])
    return dp[(1 << n) - 1]
```

State: `dp[mask]` = min total cost when the workers `0..popcount(mask)-1` have been assigned to exactly the tasks indicated by `mask`. Worker `i = popcount(mask)` is the next one to assign.

Walkthrough for `cost = [[9, 2, 7], [6, 4, 3], [5, 8, 1]]`:

| mask (bits) | popcount = worker | best dp[mask] | transitions |
|-------------|-------------------|---------------|-------------|
| 000         | 0                 | 0             | worker 0 -> task 0/1/2: dp[001]=9, dp[010]=2, dp[100]=7 |
| 010         | 1                 | 2             | worker 1 -> task 0/2: dp[011]=2+6=8, dp[110]=2+3=5 |
| 110         | 2                 | 5             | worker 2 -> task 0: dp[111]=5+5=10 |
| ...         |                   |               | other branches dominated |

Result `dp[111] = 10`. Time O(2^n * n), space O(2^n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Count Number of Maximum Bitwise-OR Subsets | https://leetcode.com/problems/count-number-of-maximum-bitwise-or-subsets/ |
| Medium | Partition to K Equal Sum Subsets | https://leetcode.com/problems/partition-to-k-equal-sum-subsets/ |
| Hard | Find Minimum Time to Finish All Jobs | https://leetcode.com/problems/find-minimum-time-to-finish-all-jobs/ |
