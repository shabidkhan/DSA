# Lowest Common Ancestor (LCA)

## What is this

The Lowest Common Ancestor of two nodes `p` and `q` in a tree is the deepest node that has both `p` and `q` as descendants (a node is also considered a descendant of itself). LCA queries appear constantly in tree problems: ancestor checks, path lengths between nodes, and tree-edit distance.

For a generic binary tree, LCA is found with a single DFS in `O(n)`. For a BST it drops to `O(h)` because the BST property tells us which side `p` and `q` lie on. For repeated queries on a static tree, Binary Lifting or Euler-tour + RMQ gives `O(log n)` or `O(1)` per query after preprocessing.

## Why we use

- LCA is the unique meeting point of root-to-`p` and root-to-`q` paths.
- The distance between `p` and `q` equals `depth(p) + depth(q) - 2 * depth(LCA)`.
- It is the building block for many tree queries (ancestor, on-path, subtree).
- For BSTs, the LCA can be found without recursion in `O(h)`.

## How to implement

```text
function lcaBinaryTree(root, p, q):
    if not root or root == p or root == q: return root
    left  = lcaBinaryTree(root.left, p, q)
    right = lcaBinaryTree(root.right, p, q)
    if left and right: return root      # split point
    return left if left else right

function lcaBST(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val: root = root.left
        elif p.val > root.val and q.val > root.val: root = root.right
        else: return root
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left if left else right
```

```python
def lca_bst(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    cur = root
    while cur:
        if p.val < cur.val and q.val < cur.val:
            cur = cur.left
        elif p.val > cur.val and q.val > cur.val:
            cur = cur.right
        else:
            return cur
    return None
```

The binary-tree algorithm relies on a simple invariant: any subtree returns "the LCA of `p`/`q` if both are inside it, otherwise whichever one (if any) it contains." The first node whose left and right subtrees both return non-null is the split point — the LCA.

## Which problems this approach solves in the real world

- Computing distance between two employees on an org chart.
- Finding the most-specific common category in a taxonomy (e.g., product catalog: "Electronics → Audio → Headphones").
- Resolving the nearest common module in a dependency tree for incremental builds.
- Computing minimum-edit distance between phylogenetic species via tree paths.
- Git: finding the merge base of two branches (LCA in the commit DAG, special-cased).

## Pros and cons

**Pros**
- Single DFS, `O(n)` time, `O(h)` recursion stack.
- BST variant is iterative, no recursion needed, `O(h)` time.
- The pattern (return non-null from either subtree, parent decides) generalizes to many tree problems.

**Cons**
- Recursive form may hit recursion limits on deep skewed trees.
- For many queries on the same tree, naive LCA is expensive — use Binary Lifting.
- Requires both nodes to exist in the tree; missing-node handling needs extra logic.

## Limitations

- Doesn't work for DAGs without modification (multiple paths exist).
- Repeated queries warrant preprocessing (`O(n log n)` build + `O(log n)` per query via Binary Lifting).
- For trees with parent pointers, two-pointer ancestor walk is simpler than DFS.
- For very large trees (`n >= 10^7`), use iterative DFS to avoid stack overflow.

## One example

Problem: Given a binary tree and two nodes `p` and `q`, return their lowest common ancestor.

```
Input tree:
        3
       / \
      5   1
     / \ / \
    6  2 0  8
       / \
      7   4

p = 5, q = 1   →  LCA = 3
p = 5, q = 4   →  LCA = 5
```

Constraints: number of nodes in `[2, 10^5]`; all `Node.val` are unique; `p` and `q` exist in the tree.

## Solution explanation

```python
def lowest_common_ancestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left if left else right
```

Walkthrough for `p = 5`, `q = 1` on the sample tree:

| Call | left result | right result | Return |
|------|-------------|--------------|--------|
| dfs(6) | None | None | None |
| dfs(7) | None | None | None |
| dfs(4) | None | None | None |
| dfs(2) | dfs(7)=None | dfs(4)=None | None |
| dfs(5) | dfs(6)=None | dfs(2)=None | 5 (root == p) |
| dfs(0) | None | None | None |
| dfs(8) | None | None | None |
| dfs(1) | dfs(0)=None | dfs(8)=None | 1 (root == q) |
| dfs(3) | dfs(5)=5 | dfs(1)=1 | 3 (both non-null → LCA) |

Time: `O(n)`. Space: `O(h)` recursion stack, where `h` is tree height.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Lowest Common Ancestor of a Binary Search Tree (LeetCode 235) | https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/ |
| Medium | Lowest Common Ancestor of a Binary Tree (LeetCode 236) | https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/ |
| Hard | Lowest Common Ancestor of a Binary Tree III (LeetCode 1650) | https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/ |
