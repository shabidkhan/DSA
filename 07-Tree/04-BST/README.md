# Binary Search Tree (BST)

## What is this

A binary search tree is a binary tree with the BST invariant: for every node, all values in its left subtree are strictly less, and all values in its right subtree are strictly greater. The invariant gives O(h) search, insert, and delete, where `h` is the tree height — O(log n) on balanced trees, O(n) on degenerate ones.

In practice, raw BSTs degrade to linked lists on sorted input; production code uses self-balancing variants (AVL, red-black, treap). The pattern here focuses on the textbook operations: search, insert, delete, validate-BST, and in-order traversal (which yields sorted order).

## Why we use

- O(log n) search / insert / delete on balanced inputs.
- In-order traversal yields sorted output for free.
- Successor / predecessor queries in O(h).
- Foundation for order statistics, range queries, and balanced-tree libraries.

## How to implement

```
search(node, key):
    if node is None or node.val == key: return node
    if key < node.val: return search(node.left, key)
    else:              return search(node.right, key)

insert(node, key):
    if node is None: return Node(key)
    if key < node.val: node.left  = insert(node.left, key)
    elif key > node.val: node.right = insert(node.right, key)
    return node

delete(node, key):
    if node is None: return None
    if key < node.val: node.left = delete(node.left, key)
    elif key > node.val: node.right = delete(node.right, key)
    else:
        if not node.left: return node.right
        if not node.right: return node.left
        succ = leftmost(node.right)
        node.val = succ.val
        node.right = delete(node.right, succ.val)
    return node
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def insert(root, key):
    if root is None: return TreeNode(key)
    if key < root.val:  root.left  = insert(root.left, key)
    elif key > root.val: root.right = insert(root.right, key)
    return root

def search(root, key):
    while root and root.val != key:
        root = root.left if key < root.val else root.right
    return root

def is_valid_bst(root):
    def go(node, lo, hi):
        if node is None: return True
        if not (lo < node.val < hi): return False
        return go(node.left, lo, node.val) and go(node.right, node.val, hi)
    return go(root, float('-inf'), float('inf'))
```

The `is_valid_bst` lo/hi window is the workhorse — it propagates the strict bounds down each recursion.

## Which problems this approach solves in the real world

- Database indexes (B-trees and B+ trees are BST generalizations).
- File system directory indexes.
- In-memory ordered maps (`std::map`, Java `TreeMap`).
- Interval and segment query trees.
- Maintaining the smallest k unique elements with insertion order.

## Pros and cons

**Pros**
- O(log n) operations on balanced inputs.
- In-order traversal gives sorted output.
- Predecessor / successor in O(h).

**Cons**
- Degrades to O(n) on adversarial / sorted input.
- Self-balancing variants have meaningful constant-factor overhead.
- Pointer-heavy — bad cache behavior vs flat arrays.

## Limitations

- Without balancing, performance is unpredictable.
- Duplicate handling needs an explicit convention (multiset vs set).
- Persistent / lock-free variants are non-trivial.

## One example

**Problem**: Validate whether a binary tree is a valid binary search tree. Each node's value must be strictly greater than all values in its left subtree and strictly less than all in its right subtree.

**Input**: `root = [2, 1, 3]`
**Output**: `True`
**Constraints**: `1 <= nodes <= 10^4`, `-2^31 <= node.val <= 2^31 - 1`.

## Solution explanation

```python
def isValidBST(root):
    def go(node, lo, hi):
        if node is None: return True
        if not (lo < node.val < hi): return False
        return go(node.left, lo, node.val) and go(node.right, node.val, hi)
    return go(root, float('-inf'), float('inf'))
```

Walkthrough on `[5, 1, 4, null, null, 3, 6]` (root 5, left 1, right 4 with children 3,6 — invalid):

| call (node, lo, hi)           | check                  | result |
|-------------------------------|------------------------|--------|
| (5, -inf, +inf)               | -inf < 5 < +inf        | recurse |
| (1, -inf, 5)                  | -inf < 1 < 5           | True (no children) |
| (4, 5, +inf)                  | 5 < 4 < +inf → fails   | False  |

Return False (matches expected). Time: O(n). Space: O(h).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Search in a Binary Search Tree (LeetCode 700) | https://leetcode.com/problems/search-in-a-binary-search-tree/ |
| Medium | Validate Binary Search Tree (LeetCode 98) | https://leetcode.com/problems/validate-binary-search-tree/ |
| Hard | Recover Binary Search Tree (LeetCode 99) | https://leetcode.com/problems/recover-binary-search-tree/ |
