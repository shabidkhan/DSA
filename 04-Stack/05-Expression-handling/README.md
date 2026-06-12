# Expression handling

## What is this

Expression-handling patterns use stacks to evaluate or transform arithmetic / logical expressions: infix evaluation, conversion to postfix (Reverse Polish Notation), postfix evaluation, and operator-precedence parsing (shunting-yard). The unifying primitive: maintain a stack of operands and a stack of operators (or a single operand stack for postfix), and apply an operator only when the next token's precedence forces it.

This pattern is the backbone of every calculator, every SQL/regex/JSON parser using precedence climbing, and every interpreter's expression layer.

## Why we use

- Single linear pass over the input — O(n).
- Cleanly separates operand storage from operator precedence handling.
- Postfix evaluation is dead simple (push values, apply operators to top two).
- Shunting-yard converts complex infix to postfix without recursion.

## How to implement

```
postfix_eval(tokens):
    st = []
    for t in tokens:
        if t is operator:
            b = st.pop(); a = st.pop()
            st.append(apply(a, b, t))
        else:
            st.append(int(t))
    return st[-1]
```

```python
def eval_rpn(tokens):
    st = []
    for t in tokens:
        if t in {'+', '-', '*', '/'}:
            b = st.pop(); a = st.pop()
            if   t == '+': st.append(a + b)
            elif t == '-': st.append(a - b)
            elif t == '*': st.append(a * b)
            else:          st.append(int(a / b))     # truncate toward zero
        else:
            st.append(int(t))
    return st[-1]
```

```python
def shunting_yard(expr):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}
    out, ops = [], []
    i, n = 0, len(expr)
    while i < n:
        c = expr[i]
        if c.isdigit():
            j = i
            while j < n and expr[j].isdigit(): j += 1
            out.append(int(expr[i:j])); i = j; continue
        elif c in prec:
            while ops and ops[-1] != '(' and prec.get(ops[-1], 0) >= prec[c]:
                out.append(ops.pop())
            ops.append(c)
        elif c == '(':
            ops.append(c)
        elif c == ')':
            while ops and ops[-1] != '(':
                out.append(ops.pop())
            ops.pop()
        i += 1
    while ops:
        out.append(ops.pop())
    return out
```

For infix evaluation directly, two stacks (values + ops) and the same precedence rule produce the answer in one pass.

## Which problems this approach solves in the real world

- Spreadsheet formula evaluators.
- Compiler / interpreter expression parsers (precedence climbing variant).
- Database query expression engines.
- Embedded calculator hardware and pocket-calculator firmware.
- Validating balanced parentheses inside larger parsers.

## Pros and cons

**Pros**
- Linear time, O(n) memory.
- Cleanly separates operand and operator concerns.
- Postfix evaluation eliminates precedence at runtime.

**Cons**
- Precedence + associativity tables must be carefully maintained.
- Unary operators (e.g. negation) need special handling.
- Floating-point evaluation accumulates rounding errors.

## Limitations

- Not directly suitable for right-associative operators without rule adjustments.
- Complex grammars (function calls, ternaries) need recursive-descent supplements.
- Streaming evaluation only works after a complete token has been read.

## One example

**Problem**: Evaluate the value of an arithmetic expression in Reverse Polish Notation. Tokens are integers or one of `+ - * /`. Division truncates toward zero.

**Input**: `tokens = ["2", "1", "+", "3", "*"]`
**Output**: `9`  (i.e. (2 + 1) * 3)
**Constraints**: `1 <= tokens.length <= 10^4`.

## Solution explanation

```python
def evalRPN(tokens):
    st = []
    for t in tokens:
        if t in {'+', '-', '*', '/'}:
            b = st.pop(); a = st.pop()
            if   t == '+': st.append(a + b)
            elif t == '-': st.append(a - b)
            elif t == '*': st.append(a * b)
            else:          st.append(int(a / b))
        else:
            st.append(int(t))
    return st[-1]
```

Walkthrough on `["2", "1", "+", "3", "*"]`:

| token | stack after |
|-------|-------------|
| 2     | [2]         |
| 1     | [2, 1]      |
| +     | [3]         |
| 3     | [3, 3]      |
| *     | [9]         |

Result: 9. Time: O(n). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Baseball Game (LeetCode 682) | https://leetcode.com/problems/baseball-game/ |
| Medium | Evaluate Reverse Polish Notation (LeetCode 150) | https://leetcode.com/problems/evaluate-reverse-polish-notation/ |
| Hard | Basic Calculator (LeetCode 224) | https://leetcode.com/problems/basic-calculator/ |
