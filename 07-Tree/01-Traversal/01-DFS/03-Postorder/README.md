# Postorder traversal

## What is this

Postorder traversal is a depth-first traversal that visits nodes in the sequence **left subtree → right subtree → node**. The parent is processed only after both its subtrees are fully done, which is exactly the order needed when a node's result depends on aggregated child results.

It is the natural traversal for "compute something bottom-up": tree height, sum of subtree, diameter, deletion, and serialization-by-shape problems.

## Why we use

- Lets a parent combine its children's already-computed answers in `O(1)`.
- Required for safe deletion: free children before freeing the parent.
- Used by recursion-on-tree problems where the recurrence is `f(node) = g(f(left), f(right), node.val)`.
- Produces the postfix form of an expression tree.

## How to implement

```text
function postorder(node, out):
    if not node: return
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.val)

function postorderIter(root):
    if not root: return []
    stack = [root]
    out = []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.left:  stack.push(node.left)
        if node.right: stack.push(node.right)
    return reverse(out)
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def postorder_recursive(root: TreeNode) -> list[int]:
    out: list[int] = []
    def dfs(node: TreeNode | None) -> None:
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        out.append(node.val)
    dfs(root)
    return out
```

```python
def postorder_iterative(root: TreeNode) -> list[int]:
    if not root:
        return []
    stack, out = [root], []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return out[::-1]
```

The two-stack / reverse trick works because pushing left-then-right and appending the root yields a "root → right → left" order; reversing produces "left → right → root", i.e., postorder.

## Which problems this approach solves in the real world

- Computing total disk usage of a directory tree (parent size = sum of children sizes).
- Garbage collection / reference counting — free children before parents.
- Evaluating arithmetic expressions stored as expression trees.
- Computing the height/diameter of an org chart bottom-up.
- Compiling: emit machine code for child expressions before combining at the parent.

## Pros and cons

**Pros**
- Natural fit for bottom-up tree DP.
- Each child returns once with a fully computed answer.
- Two-stack iterative form is short and avoids tricky state.

**Cons**
- Cannot stop "early" once you find a target — must visit children first.
- Iterative single-stack version with the proper postorder is fiddly (visited markers).
- Recursive stack depth is `O(h)`; deep trees may need an explicit stack.

## Limitations

- Not useful when the answer flows top-down (use pre-order for those).
- Output order is not human-readable for general inspection.
- Cannot be parallelized across siblings naively if children mutate a shared structure.
- For very large `n`, the reverse-trick allocates the full output list; a generator may be preferable.

## One example

Problem: Given the root of a binary tree, return its postorder traversal.

```
Input tree:
    1
     \
      2
     /
    3

Output: [3, 2, 1]
```

Constraints: number of nodes in the range `[0, 100]`; `-100 <= Node.val <= 100`.

## Solution explanation

```python
def postorder_traversal(root):
    if not root:
        return []
    stack, out = [root], []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return out[::-1]
```

Walkthrough for the sample tree:

| Step | stack | out | Action |
|------|-------|-----|--------|
| 0 | [1] | [] | start |
| 1 | [2] | [1] | pop 1, push right=2 |
| 2 | [3] | [1, 2] | pop 2, push left=3 (no right) |
| 3 | [] | [1, 2, 3] | pop 3, no children |
| 4 | reverse → [3, 2, 1] | | final result |

Time: `O(n)`. Space: `O(h)` stack plus `O(n)` for the output list.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Maximum Depth of Binary Tree (LeetCode 104) | https://leetcode.com/problems/maximum-depth-of-binary-tree/ |
| Medium | Binary Tree Postorder Traversal (LeetCode 145) | https://leetcode.com/problems/binary-tree-postorder-traversal/ |
| Hard | Binary Tree Maximum Path Sum (LeetCode 124) | https://leetcode.com/problems/binary-tree-maximum-path-sum/ |
