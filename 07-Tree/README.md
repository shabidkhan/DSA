# Tree Patterns

## Folder structure

```
07-Tree/
├── README.md
├── 01-Traversal/
│   ├── README.md
│   ├── 01-DFS/
│   │   ├── 01-Preorder/README.md
│   │   ├── 02-Inorder/README.md
│   │   └── 03-Postorder/README.md
│   └── 02-BFS/
│       ├── README.md
│       ├── 01-Level-order/README.md
│       ├── 02-Zigzag/README.md
│       └── 03-Right-side-view/README.md
├── 02-Recursion-patterns/
│   ├── 01-Top-down/README.md
│   └── 02-Bottom-up/README.md
├── 03-Path-based/
│   ├── 01-Path-sum/README.md
│   └── 02-Diameter/README.md
├── 04-BST/README.md
└── 05-LCA/README.md
```

## What is this

A tree is a connected acyclic graph with a designated root, where every non-root node has exactly one parent. Trees are the data structure of hierarchies — file systems, DOM, organisation charts, expression trees, and decision processes. Tree problems split into four families: traversal (how do you visit every node in a specific order?), recursion patterns (top-down vs bottom-up signal flow), path-based questions (sums, diameters, ancestors), and BST-specific algorithms that exploit the sorted-by-key invariant.

The single most important mental shift for tree problems is the recursion direction: top-down passes information *down* through parameters, bottom-up gathers information *up* through return values. Almost every tree question is naturally one or the other, and choosing wrong leads to messy code with global state.

## Why we use

- Hierarchies are everywhere — file systems, JSON/XML, DOM, taxonomies.
- Trees give O(log n) operations when balanced (BST, heap, B-tree).
- Recursion makes tree code remarkably short — often 5-10 lines.
- They're the visual model for backtracking and decision-tree search.

## How to implement

Pick the subpattern that fits your question:

```
traversal           — DFS (pre/in/post) for recursive shape; BFS for level info
recursion patterns  — top-down (pass state down) vs bottom-up (return up)
path-based          — root-to-leaf or any-to-any sums and diameters
BST                 — exploit sorted in-order invariant for log n ops
```

Subpatterns in this folder:

- **01-Traversal** — DFS (preorder, inorder, postorder) and BFS (level-order, zigzag, right-side-view).
- **02-Recursion-patterns** — top-down (push state) and bottom-up (pull values).
- **03-Path-based** — path sums and diameter.
- **04-BST** — binary search tree operations using sorted invariant.
- **05-LCA** — lowest common ancestor queries.

## Which problems this approach solves in the real world

- File-system traversal (find, du, recursive copy).
- DOM rendering and event bubbling in browsers.
- Database B-trees and B+-trees for indexed queries.
- Expression evaluation in compilers and calculators.
- AI decision trees in games and rule engines.
- Hierarchical organisation reporting (manager → reports).

## Pros and cons

**Pros**
- Recursive code is short and matches the structure naturally.
- Balanced trees give O(log n) for many operations.
- BFS gives shortest-path semantics on unweighted hierarchies.
- DFS uses O(h) stack — usually much less than n.

**Cons**
- Recursion depth can exceed the stack on skewed trees.
- Choosing the right traversal order is critical and error-prone.
- Top-down vs bottom-up confusion leads to ugly global-state hacks.
- Mutable parent pointers complicate reasoning.

## Limitations

- Unbalanced trees degrade to O(n) — must be balanced or rebuilt.
- Concurrent updates require lock coupling or persistent structures.
- General graphs need different techniques (cycles break tree assumptions).
- Path-aggregation problems on trees with weights need careful Euler-tour or LCA setup.
