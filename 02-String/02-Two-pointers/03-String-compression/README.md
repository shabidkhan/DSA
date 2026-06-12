# String compression

## What is this

Run-length encoding (RLE) and its in-place variant compress a string by replacing each run of consecutive identical characters with the character followed by the run length. For example `"aaabbc"` becomes `"a3b2c1"` (or `"a3b2c"` if singletons drop the 1).

The pattern is a two-pointer scan: `read` walks through the input, `write` advances only when finalizing a run. With the right discipline, the compression happens in place with O(1) extra space.

## Why we use

- O(n) time, O(1) extra space (in-place).
- Highly effective on data with long runs.
- Simple to encode and decode — no header / no tables.
- Foundation for line-level encoding in many image formats (BMP, TIFF).

## How to implement

```
read = write = 0
while read < n:
    j = read
    while j < n and s[j] == s[read]: j += 1
    s[write] = s[read]; write += 1
    run = j - read
    if run > 1:
        for d in str(run):
            s[write] = d; write += 1
    read = j
return write
```

```python
def compress(chars):
    n = len(chars)
    read = write = 0
    while read < n:
        j = read
        while j < n and chars[j] == chars[read]:
            j += 1
        chars[write] = chars[read]; write += 1
        run = j - read
        if run > 1:
            for d in str(run):
                chars[write] = d; write += 1
        read = j
    return write
```

```python
def decompress(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]; i += 1
        j = i
        while j < len(s) and s[j].isdigit():
            j += 1
        count = int(s[i:j]) if j > i else 1
        out.append(c * count)
        i = j
    return "".join(out)
```

Multi-digit runs need to be written digit-by-digit; you cannot just write `"12"` as one character.

## Which problems this approach solves in the real world

- BMP / TIFF / PCX image RLE encoding for long runs of identical pixels.
- Faxing protocols (run-length of black/white pixels).
- Streaming-protocol compression of repeated control characters.
- Compact representation of game-board states with many empty cells.
- Quick compaction of telemetry messages with repeated tokens.

## Pros and cons

**Pros**
- Trivial encode / decode.
- In-place compression with two pointers.
- Excellent on data with long runs.

**Cons**
- Useless on random / high-entropy data (expands rather than compresses).
- Single-digit runs save no space; multi-digit runs cost log10 chars.
- Not a general-purpose compressor (use LZ77 / Huffman for that).

## Limitations

- Worst case: every character distinct → output longer than input.
- Multi-byte characters complicate the inner equality check.
- Streaming variant must buffer the current run.

## One example

**Problem**: Given an array of characters `chars`, compress it in place. Return the new length. The algorithm must use only constant extra space.

**Input**: `chars = ['a', 'a', 'b', 'b', 'c', 'c', 'c']`
**Output**: `6`, `chars` becomes `['a','2','b','2','c','3', ...]`
**Constraints**: `1 <= chars.length <= 2000`, characters are letters or digits.

## Solution explanation

```python
def compress(chars):
    n = len(chars)
    read = write = 0
    while read < n:
        j = read
        while j < n and chars[j] == chars[read]:
            j += 1
        chars[write] = chars[read]; write += 1
        run = j - read
        if run > 1:
            for d in str(run):
                chars[write] = d; write += 1
        read = j
    return write
```

Walkthrough on `['a','a','b','b','c','c','c']`:

| read | j | run | write before | chars after write | write after |
|------|---|-----|--------------|-------------------|-------------|
| 0    | 2 | 2   | 0            | ['a',...]         | 1           |
|      |   |     |              | ['a','2',...]     | 2           |
| 2    | 4 | 2   | 2            | ['a','2','b',...] | 3           |
|      |   |     |              | ['a','2','b','2',...] | 4       |
| 4    | 7 | 3   | 4            | ['a','2','b','2','c',...] | 5   |
|      |   |     |              | ['a','2','b','2','c','3',...] | 6 |

Return 6. Time: O(n). Space: O(1).

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | Count Binary Substrings (LeetCode 696) | https://leetcode.com/problems/count-binary-substrings/ |
| Medium | String Compression (LeetCode 443) | https://leetcode.com/problems/string-compression/ |
| Hard | Encode String with Shortest Length (LeetCode 471) | https://leetcode.com/problems/encode-string-with-shortest-length/ |
