# Two-pointer Patterns

## Folder structure

```
01-Two-pointer/
├── README.md
├── 01-Opposite-ends/README.md
├── 02-Same-direction/README.md
├── 03-Fast-slow/README.md
└── 04-Partition/README.md
```

## What is this

The two-pointer technique uses two indices that move through an array (or string, or linked list) in a coordinated way: opposite ends moving inward, both starting at the same end and moving at different speeds, or partitioning the array in place. The unifying idea is that two coordinated pointers replace the inner loop of a brute-force O(n²) scan with a single linear pass.

The three subpatterns here are: **opposite ends** (sorted arrays, palindrome checks, container with most water), **same direction / fast-slow** (linked-list cycle detection, find middle, remove duplicates), and **partition / Dutch flag** (three-way partitioning, sort colors).

## Why we use

- Collapses O(n²) brute force into O(n) or O(n log n) (after sort).
- O(1) extra space — both pointers are just indices.
- Cache-friendly: pointers move forward through memory.
- Works equally well on arrays, strings, and linked lists.

## How to implement

```
opposite ends:
    l, r = 0, n - 1
    while l < r:
        if condition(arr[l], arr[r]): adjust both
        elif need_larger: l += 1
        else: r -= 1

same direction:
    write = 0
    for read in 0..n-1:
        if keep(arr[read]):
            arr[write] = arr[read]; write += 1

partition (Dutch flag):
    lo, mid, hi = 0, 0, n - 1
    while mid <= hi:
        if arr[mid] < pivot: swap(arr[lo], arr[mid]); lo += 1; mid += 1
        elif arr[mid] == pivot: mid += 1
        else: swap(arr[mid], arr[hi]); hi -= 1
```

Subpatterns in this folder:

- **01-Opposite-ends** — l/r converging; sorted-input pair-finding and palindrome checks.
- **02-Same-direction** — read/write pointer; in-place dedup and compaction.
- **03-Fast-slow** — two speeds; cycle detection and find-middle.
- **04-Partition** — Dutch-flag three-way partition.

## Which problems this approach solves in the real world

- In-place removal of duplicates from a sorted list.
- Detecting cycles in service dependency chains.
- Three-color partitioning of records (e.g., status buckets).
- Two-sum / three-sum search after sorting.
- Container / area problems in geometry.
- Palindrome validation in editors and search.

## Pros and cons

**Pros**
- O(n) time and O(1) extra space.
- Simple, mechanical template once recognised.
- In-place modification keeps memory low.
- Cache-friendly forward traversal.

**Cons**
- Sorted input often required — sort cost may dominate.
- Tricky to write correct termination conditions (off-by-one on `l < r` vs `l <= r`).
- Doesn't generalise to k > 3 pointers without combinatorial pain.
- Modifying-in-place may break caller assumptions.

## Limitations

- Cannot solve problems that need random access to non-pointer positions.
- Fast-slow only detects cycles; finding cycle length needs extra steps.
- Partition variants require careful pivot choice on duplicates.
- For unsorted unique-element problems, hash maps often dominate.
