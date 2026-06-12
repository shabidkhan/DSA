# Recursion Patterns

## Folder structure

```
02-Recursion-patterns/
├── README.md
├── 01-Top-down/README.md
└── 02-Bottom-up/README.md
```

## What is this

Almost every non-trivial tree problem reduces to one of two recursion shapes: top-down, where the parent passes state down to its children, and bottom-up, where children return values back up to the parent. The difference is where the information lives: in the call's *arguments* (top-down) or in the call's *return value* (bottom-up). Picking the wrong shape forces awkward globals or repeated traversals.

These two patterns are the building blocks of all tree DP, path-based aggregation, and structural validation problems. A clean tree solution is almost always the right pattern applied to the right invariant — not a clever data structure.

## Why we use

- Top-down is natural when each subtree's answer depends on something coming from above (current depth, running path sum, allowed range for BST values).
- Bottom-up is natural when each parent's answer depends on its children's answers (height, max-path, subtree size, "is this a valid BST").
- Choosing the right direction eliminates the need for global accumulators and second passes.
- Both share the same recursion skeleton — the choice is about *where the state flows*.

## How to implement

```text
# Top-down — pass info DOWN as arguments
function topDown(node, stateFromParent):
    if node is null: return
    newState = update(stateFromParent, node.val)
    if node is leaf: record(newState)
    topDown(node.left, newState)
    topDown(node.right, newState)

# Bottom-up — return info UP
function bottomUp(node):
    if node is null: return baseValue
    left  = bottomUp(node.left)
    right = bottomUp(node.right)
    return combine(node.val, left, right)
```

Subpatterns in this folder:

- `01-Top-down/` — state flows from parent to child via arguments. Examples: path sum, max depth with depth-carrying arg, BST validity with `(low, high)` range.
- `02-Bottom-up/` — state flows from child to parent via return value. Examples: tree height, diameter, balanced check, subtree sum.

## Which problems this approach solves in the real world

- Validating hierarchical permission trees where each child's allowed scope is bounded by its parent.
- Computing rollups in org charts (total headcount, total cost per department).
- Detecting cycles or invalid states in build-dependency graphs that have been collapsed into a spanning tree.
- Verifying that a serialized JSON document satisfies a nested schema where rules propagate downward.
- Calculating cumulative weights in routing tables modeled as trees.
- Evaluating expression trees where each internal node combines its children's evaluated results.

## Pros and cons

**Pros**
- Zero scratch storage beyond the call stack itself.
- The recursion contract makes correctness easy to prove inductively.
- Avoids the temptation to use error-prone globals or instance variables.
- Reads top-to-bottom — the recursive case mirrors the structural definition of the tree.

**Cons**
- Top-down with mutable shared accumulators is easy to get wrong (must reset on the way back up).
- Bottom-up that needs *two* values per node (e.g., diameter wants height AND best diameter so far) requires returning tuples or carrying a non-local.
- Recursion depth equals tree height — skewed trees blow the stack.
- The mental switch between "down" and "up" trips beginners; mixing them in one function often signals a bad decomposition.

## Limitations

- Doesn't apply cleanly to problems that need level/distance information — use BFS instead.
- Top-down with side effects can double-count if the same node is shared across paths (e.g., DAGs).
- Bottom-up cannot start producing answers before reaching the leaves — bad for streaming/incremental use.
- Both patterns assume a fixed tree shape; mutating the tree during recursion needs careful pre/post placement of writes.
