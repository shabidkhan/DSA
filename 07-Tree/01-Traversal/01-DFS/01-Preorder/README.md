# Preorder traversal

## What is this

Preorder traversal is a depth-first traversal that visits nodes in the sequence **node → left subtree → right subtree**. The parent is processed before its children, which makes it the natural choice when child computations depend on accumulated state passed down from the root.

It is also the traversal used to serialize a tree by structure (paired with a marker for null children) so that the original tree can be reconstructed later.

## Why we use

- Lets you pass state from parent to children (e.g., depth, path-sum so far).
- Required for "top-down" recursion where the parent's decisions configure child traversal.
- Used as one half of "tree from preorder + inorder" reconstruction.
- Produces the prefix form of an expression tree (Polish notation).

## How to implement

```text
function preorder(node, out):
    if not node: return
    out.append(node.val)
    preorder(node.left, out)
    preorder(node.right, out)

function preorderIter(root):
    if not root: return []
    stack = [root]
    out = []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right: stack.push(node.right)
        if node.left:  stack.push(node.left)
    return out
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder_recursive(root: TreeNode) -> list[int]:
    out: list[int] = []
    def dfs(node: TreeNode | None) -> None:
        if not node:
            return
        out.append(node.val)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return out
```

```python
def preorder_iterative(root: TreeNode) -> list[int]:
    if not root:
        return []
    stack, out = [root], []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out
```

The iterative trick: push right child before left so that left is popped (and visited) first. The stack always contains the not-yet-visited "frontier" of the DFS.

## Which problems this approach solves in the real world

- Serializing trees for storage or RPC (e.g., serialize/deserialize binary tree LC 297).
- Pretty-printing nested structures (JSON, file trees) with proper indentation.
- Path-sum queries on trees (parent passes current path sum down).
- Copying / cloning a tree node-by-node.
- Configuring HTML/DOM trees during a top-down render pass.

## Pros and cons

**Pros**
- Each node is processed immediately when first reached — supports early termination.
- Lets parent context flow naturally into children.
- Iterative version is the simplest of the three DFS orders.

**Cons**
- Cannot aggregate child results without separate post-processing.
- Order is structure-sensitive; small changes in tree shape change the output a lot.
- Recursion depth `O(h)` on deep trees.

## Limitations

- Cannot directly compute height or subtree-aggregate values (use postorder).
- Not the right traversal for "in sorted order on a BST" (use inorder).
- Cannot be cleanly parallelized when children depend on shared root-down state.
- For `n`-ary trees, all children must be pushed in reverse order to preserve visit order.

## One example

Problem: Given the root of a binary tree, return its preorder traversal.

```
Input tree:
    1
     \
      2
     /
    3

Output: [1, 2, 3]
```

Constraints: number of nodes in the range `[0, 100]`; `-100 <= Node.val <= 100`.

## Solution explanation

```python
def preorder_traversal(root):
    if not root:
        return []
    stack, out = [root], []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out
```

Walkthrough for the sample tree:

| Step | stack | out | Action |
|------|-------|-----|--------|
| 0 | [1] | [] | start |
| 1 | [2] | [1] | pop 1, emit 1; push right=2 |
| 2 | [3] | [1, 2] | pop 2, emit 2; push left=3 |
| 3 | [] | [1, 2, 3] | pop 3, emit 3; no children |

Time: `O(n)`. Space: `O(h)` for the stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Binary Tree Preorder Traversal (LeetCode 144) | https://leetcode.com/problems/binary-tree-preorder-traversal/ |
| Medium | Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105) | https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/ |
| Hard | Serialize and Deserialize Binary Tree (LeetCode 297) | https://leetcode.com/problems/serialize-and-deserialize-binary-tree/ |
