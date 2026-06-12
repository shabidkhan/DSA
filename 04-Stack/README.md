# Stack Patterns

## Folder structure

```
04-Stack/
├── README.md
├── 01-Monotonic/
│   ├── README.md
│   ├── 01-Increasing/README.md
│   └── 02-Decreasing/README.md
├── 02-Nearest-element/
│   ├── README.md
│   ├── 01-Next-greater/README.md
│   ├── 02-Next-smaller/README.md
│   └── 03-Previous-variants/README.md
├── 03-Range-span/README.md
├── 04-Min-max-stack/README.md
├── 05-Expression-handling/README.md
├── 06-Histogram/README.md
└── 07-Parentheses/README.md
```

## What is this

A stack is a LIFO (last-in, first-out) container, and most stack problems exploit one specific property: when the next element invalidates one or more previous elements, the stack lets us pop them in O(1) and react to "what was the previous unresolved thing?" in O(1). The family centres on monotonic stacks (kept sorted by insertion), nearest-element queries (Next Greater / Next Smaller / Previous Greater/Smaller), range/span problems (e.g., stock spans), min/max stacks (constant-time current extreme), expression handling (operator/operand stacks), and histogram-area problems.

Stack problems often look complex at first glance but collapse to a five-line skeleton: push when the invariant is satisfied, pop while it isn't, record the answer at pop time. Once you see this skeleton, problems like Daily Temperatures, Largest Rectangle in Histogram, and Stock Span feel mechanical.

## Why we use

- LIFO matches the natural order of nesting (parentheses, function calls, undo history).
- Monotonic stacks give O(n) total time for nearest-element queries that look O(n²).
- Expression evaluation and parsing are textbook stack problems.
- Stack-based DFS replaces recursion when stack-overflow is a risk.

## How to implement

Pick the subpattern by what you're tracking:

```
monotonic       — keep stack increasing or decreasing; pop when new element breaks order
nearest element — process left-to-right with monotonic stack; record at pop time
range / span    — count "how far back is the previous bigger/smaller element"
min/max stack   — auxiliary stack tracks current min/max in O(1)
expression      — separate operator and operand stacks; pop on precedence resolve
histogram       — monotonic-stack technique to compute largest rectangle
```

Subpatterns in this folder:

- **01-Monotonic** — increasing and decreasing variants.
- **02-Nearest-element** — Next Greater, Next Smaller, Previous variants.
- **03-Range-span** — stock-span-style problems.
- **04-Min-max-stack** — constant-time current extreme.
- **05-Expression-handling** — operators, operands, parentheses.
- **06-Histogram** — Largest Rectangle in Histogram and related.
- **07-Parentheses** — matched/unmatched, longest valid, generation.

## Which problems this approach solves in the real world

- Function-call frames and recursion in language runtimes.
- Undo/redo stacks in editors and IDEs.
- Expression evaluators (calculators, formula engines, spreadsheets).
- Browser history navigation.
- Bracket matching and syntax highlighting in editors.
- Backtracking solvers (treat the stack as the recursion frame).

## Pros and cons

**Pros**
- O(1) push/pop/peek with trivial memory layout.
- Monotonic stack collapses many O(n²) brute forces to O(n).
- Mental model is intuitive: "process and resolve later" naturally fits LIFO.
- Pairs beautifully with arrays for nearest-element and span queries.

**Cons**
- Wrong monotone direction (increasing vs decreasing) is the most common bug.
- Knowing when to record the answer (push time vs pop time) is subtle.
- Two-stack designs (min stack, expression stacks) double the memory.
- Doesn't help for "next K" or "all previous elements" queries — those need other structures.

## Limitations

- Doesn't support random access; only the top is O(1).
- No useful merge/split operations.
- Recursive solutions often look cleaner but blow the call stack on big inputs.
- For "online" variants you must process strictly in order, no rewinding.
