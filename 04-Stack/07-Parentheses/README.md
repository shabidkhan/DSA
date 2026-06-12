# Parentheses matching (stack)

## What is this

Parentheses matching uses a stack to validate or process nested bracket structures. Push every opening bracket; on every closing bracket pop the top and verify it pairs correctly. The stack is empty if and only if the input is balanced.

The same pattern handles mixed bracket types (`()[]{}`), evaluates arithmetic expressions, processes nested function calls in tokenizers, and supports edits that compute the longest valid parenthesis substring.

## Why we use

- O(n) one-pass validation
- Trivial implementation; central to every tokenizer / parser
- Generalises to expression evaluation (Shunting-Yard) and AST construction
- Backbone of "longest valid parentheses" and "minimum add to make valid" problems

## How to implement

```
match = {')': '(', ']': '[', '}': '{'}
stack = []
for c in s:
    if c in '([{':
        stack.append(c)
    else:
        if not stack or stack.pop() != match[c]:
            return False
return not stack
```

```python
def is_valid(s: str) -> bool:
    match = {')': '(', ']': '[', '}': '{'}
    stack: list[str] = []
    for c in s:
        if c in '([{':
            stack.append(c)
        elif c in match:
            if not stack or stack.pop() != match[c]:
                return False
    return not stack
```

Longest valid parentheses substring (stack of indices, sentinel `-1` for the base):

```python
def longest_valid(s: str) -> int:
    stack: list[int] = [-1]
    best = 0
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best
```

Invariant for `is_valid`: at any moment, the stack holds exactly the unmatched opening brackets seen so far, in left-to-right order. A closing bracket either matches the top or proves invalidity.

## Which problems this approach solves in the real world

- Source-code editors / linters checking brace balance live as you type
- Tokenizers in JSON / XML / template engines verifying structural correctness
- Expression evaluators in spreadsheets and calculator apps
- LISP/Scheme readers building the AST node-by-node
- Markdown / BBCode parsers that need to ensure tags close in the right order

## Pros and cons

**Pros**
- O(n) time, O(n) memory in the worst case
- Code reads almost like the spec
- Easily extended to evaluate operator-precedence expressions

**Cons**
- Stack-only check ignores semantic mismatches (e.g. mismatched quote types)
- For very long inputs without balancing, stack grows linearly
- Doesn't natively handle escape sequences inside string literals — need a separate state

## Limitations

- Cannot validate context-sensitive grammars (e.g. matching opening/closing tag *names*) without storing the tag itself
- Linear-time stack approach cannot answer arbitrary range "is balanced?" queries (needs segment tree)
- Single-thread sequential — not naturally parallel

## One example

Problem: Given a string `s` containing just the characters `(`, `)`, `{`, `}`, `[`, `]`, determine if it is valid. An input is valid if open brackets are closed by the same type and in the correct order.

```
Input:  s = "{[()]}"
Output: True

Input:  s = "{[(])}"
Output: False
Constraints: 1 <= len(s) <= 10^4
```

## Solution explanation

```python
def is_valid(s: str) -> bool:
    match = {')': '(', ']': '[', '}': '{'}
    stack: list[str] = []
    for c in s:
        if c in '([{':
            stack.append(c)
        elif c in match:
            if not stack or stack.pop() != match[c]:
                return False
    return not stack
```

Push opens; for each close, pop and check correspondence. End-of-input must leave an empty stack.

Walkthrough for `s = "{[()]}"`:

| i | char | action            | stack after |
|---|------|-------------------|-------------|
| 0 | {    | push              | ['{']       |
| 1 | [    | push              | ['{', '[']  |
| 2 | (    | push              | ['{', '[', '('] |
| 3 | )    | pop '(' OK        | ['{', '['] |
| 4 | ]    | pop '[' OK        | ['{'] |
| 5 | }    | pop '{' OK        | []          |

End: stack empty -> `True`. Time O(n), space O(n) (best case O(1) when no opens accumulate).

Counter-example for `"{[(])}"`: when `)` is encountered, top is `[` so mismatch -> `False`.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Valid Parentheses (LeetCode 20) | https://leetcode.com/problems/valid-parentheses/ |
| Medium | Minimum Add to Make Parentheses Valid (LeetCode 921) | https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/ |
| Hard | Longest Valid Parentheses (LeetCode 32) | https://leetcode.com/problems/longest-valid-parentheses/ |
