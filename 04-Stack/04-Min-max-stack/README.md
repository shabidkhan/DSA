# Min/Max stack

## What is this

A min/max stack is a regular LIFO stack augmented to return the minimum (or maximum) of all currently held elements in O(1). The trick is to maintain a parallel "min stack" that stores, at each position, the minimum value of the main stack at the moment of that push.

Push and pop run in O(1); the `getMin()` query is also O(1) — just peek the top of the min stack.

## Why we use

- Constant-time min/max queries alongside O(1) push/pop.
- No need to scan the stack on each query.
- Foundation for "max in window" via two stacks (queue simulation).
- Useful in expression evaluators that need running min/max state.

## How to implement

```
data = []
mins = []
push(x):
    data.append(x)
    mins.append(min(x, mins[-1]) if mins else x)
pop():
    data.pop(); mins.pop()
top():    return data[-1]
getMin(): return mins[-1]
```

```python
class MinStack:
    def __init__(self):
        self.data = []
        self.mins = []

    def push(self, x):
        self.data.append(x)
        self.mins.append(x if not self.mins else min(x, self.mins[-1]))

    def pop(self):
        self.data.pop()
        self.mins.pop()

    def top(self):
        return self.data[-1]

    def getMin(self):
        return self.mins[-1]
```

```python
class MinStackCompact:
    """Store only when a new minimum is seen, with a count."""
    def __init__(self):
        self.data = []
        self.mins = []   # (value, count_of_consecutive_with_same_or_higher)

    def push(self, x):
        self.data.append(x)
        if not self.mins or x < self.mins[-1][0]:
            self.mins.append([x, 1])
        else:
            self.mins[-1][1] += 1

    def pop(self):
        self.data.pop()
        self.mins[-1][1] -= 1
        if self.mins[-1][1] == 0:
            self.mins.pop()

    def getMin(self):
        return self.mins[-1][0]
```

The compact variant trades a slightly more complex pop for less memory on inputs with many equal pushes.

## Which problems this approach solves in the real world

- Streaming "current min/max" queries on a stack-shaped data flow.
- Expression evaluator that needs current minimum of operand stack.
- Undo/redo stacks with running stat queries.
- Implementing a queue with O(1) amortized min via two min stacks.
- Trading systems: lowest bid in current pending stack of orders.

## Pros and cons

**Pros**
- O(1) push, pop, top, getMin.
- Trivial implementation with two arrays.
- Composable: two min stacks → O(1) amortized min queue.

**Cons**
- 2x memory of a plain stack.
- Compact variant requires deeper bookkeeping.
- Not directly useful when you need min across an arbitrary window (use deque instead).

## Limitations

- Not thread-safe by itself.
- Cannot answer "min after popping x more elements" without unwinding.
- A separate structure is needed for max — or store negatives in the same stack.

## One example

**Problem**: Design a stack that supports `push`, `pop`, `top`, and `getMin`, each in O(1).

**Input**: `push(-2); push(0); push(-3); getMin(); pop(); top(); getMin();`
**Output**: `[null, null, null, null, -3, null, 0, -2]`
**Constraints**: `pop`, `top`, `getMin` are called only after a `push`.

## Solution explanation

```python
class MinStack:
    def __init__(self):
        self.data = []
        self.mins = []
    def push(self, x):
        self.data.append(x)
        self.mins.append(x if not self.mins else min(x, self.mins[-1]))
    def pop(self):
        self.data.pop(); self.mins.pop()
    def top(self):
        return self.data[-1]
    def getMin(self):
        return self.mins[-1]
```

Walkthrough on the sequence above:

| op          | data            | mins            | returns |
|-------------|-----------------|-----------------|---------|
| push(-2)    | [-2]            | [-2]            | -       |
| push(0)     | [-2, 0]         | [-2, -2]        | -       |
| push(-3)    | [-2, 0, -3]     | [-2, -2, -3]    | -       |
| getMin()    | [-2, 0, -3]     | [-2, -2, -3]    | -3      |
| pop()       | [-2, 0]         | [-2, -2]        | -       |
| top()       | [-2, 0]         | [-2, -2]        | 0       |
| getMin()    | [-2, 0]         | [-2, -2]        | -2      |

Time per op: O(1). Space: O(n).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Min Stack (LeetCode 155) | https://leetcode.com/problems/min-stack/ |
| Medium | Max Stack (LeetCode 716) | https://leetcode.com/problems/max-stack/ |
| Hard | Sliding Window Maximum (LeetCode 239) | https://leetcode.com/problems/sliding-window-maximum/ |
