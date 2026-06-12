# Huffman encoding (heap)

## What is this

Huffman coding builds an optimal prefix-free binary code for a set of symbols with known frequencies. Repeatedly pop the two least-frequent symbols (or subtrees) from a min-heap, combine them into a new tree with summed frequency, and push the combined tree back. After n-1 merges the heap contains a single tree; symbol codes are the root-to-leaf paths (0 for left, 1 for right). Total time O(n log n).

The optimality is the merge-cost interpretation: the sum of all combined frequencies equals the weighted external path length, which equals the expected code length per symbol.

## Why we use

- Optimal prefix-free encoding given known frequencies.
- O(n log n) heap-based construction.
- Forms the entropy-coding stage of many compressors (DEFLATE, BZIP2).
- Generalizes to the "minimum merge cost" greedy pattern.

## How to implement

```
heap = min-heap of (freq, node)
while len(heap) > 1:
    f1, a = heappop(heap)
    f2, b = heappop(heap)
    parent = Node(f1 + f2, a, b)
    heappush(heap, (f1 + f2, parent))
root = heap[0][1]
emit codes by DFS, left='0', right='1'
```

```python
import heapq
from collections import Counter

class HuffNode:
    __slots__ = ("freq", "ch", "l", "r")
    def __init__(self, freq, ch=None, l=None, r=None):
        self.freq = freq; self.ch = ch; self.l = l; self.r = r
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman(text):
    if not text: return {}, None
    counts = Counter(text)
    heap = [HuffNode(f, ch=c) for c, f in counts.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        only = heapq.heappop(heap)
        root = HuffNode(only.freq, l=only)
    else:
        while len(heap) > 1:
            a = heapq.heappop(heap)
            b = heapq.heappop(heap)
            heapq.heappush(heap, HuffNode(a.freq + b.freq, l=a, r=b))
        root = heap[0]

    codes = {}
    def walk(n, path):
        if n is None: return
        if n.ch is not None:
            codes[n.ch] = path or "0"
            return
        walk(n.l, path + "0")
        walk(n.r, path + "1")
    walk(root, "")
    return codes, root
```

```python
def huffman_encode(text):
    codes, root = build_huffman(text)
    return "".join(codes[c] for c in text), codes
```

When only one distinct character exists, special-case the codebook (everyone gets the single bit "0").

## Which problems this approach solves in the real world

- Entropy coding stage of ZIP / GZIP / DEFLATE / BZIP2.
- JPEG and PNG image compression's entropy stages.
- Optimal merge cost in the "merge piles with cost = sum" greedy pattern.
- Constructing optimal binary search codes for known query frequencies.
- Network message header compression (HPACK, QPACK use Huffman tables).

## Pros and cons

**Pros**
- Provably optimal prefix-free code for static symbol probabilities.
- O(n log n) construction.
- Compact codebook representation.

**Cons**
- Static — does not adapt to changing distributions (use adaptive Huffman or arithmetic coding).
- Bit-level I/O is fiddly to implement correctly.
- Symbol counts must be known up front.

## Limitations

- Suboptimal vs arithmetic coding when codebook is small.
- One-pass adaptive variants are more complex.
- Cannot directly handle symbols with extremely skewed probabilities efficiently.

## One example

**Problem**: Given a string `text`, construct a Huffman code for its characters and return the codebook plus the total encoded bit length.

**Input**: `text = "aaabbc"`
**Output**: codebook like `{'a': '0', 'b': '10', 'c': '11'}`, length = 3*1 + 2*2 + 1*2 = 9 bits.
**Constraints**: 1 <= text length <= 10^5.

## Solution explanation

```python
def encode(text):
    codes, _ = build_huffman(text)
    bits = "".join(codes[c] for c in text)
    return codes, len(bits)
```

Walkthrough on `text = "aaabbc"` (counts a:3, b:2, c:1):

| step | heap (sorted by freq) | action                              |
|------|-----------------------|-------------------------------------|
| init | [c:1, b:2, a:3]       | -                                   |
| 1    |                       | pop c:1, b:2 → merge as cb:3; push  |
|      | [a:3, cb:3]           |                                     |
| 2    |                       | pop a:3, cb:3 → merge as root:6     |
|      | [root:6]              |                                     |

Codes from root: a='0', cb-branch='1', b='10', c='11'. Encoded bits = `0 0 0 10 10 11` (9 bits).

Time: O(n log k). Space: O(k).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Last Stone Weight (LeetCode 1046) | https://leetcode.com/problems/last-stone-weight/ |
| Medium | Minimum Cost to Connect Sticks (LeetCode 1167) | https://leetcode.com/problems/minimum-cost-to-connect-sticks/ |
| Hard | Reorganize String (LeetCode 767) | https://leetcode.com/problems/reorganize-string/ |
