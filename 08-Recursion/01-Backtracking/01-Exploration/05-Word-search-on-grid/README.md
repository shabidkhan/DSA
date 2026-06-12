# Word search on a 2D grid (DFS + backtracking)

## What is this

Given a 2D grid of characters and a target word, decide whether the word can be formed by traversing **adjacent** cells (up/down/left/right) without revisiting any cell within a single search. The solution: at every cell that matches the word's first letter, launch a DFS that tries each of the four neighbours, **marking cells as visited on entry and unmarking on backtrack**. The choose/explore/unchoose template adapted to a grid.

The two clever tricks:
1. **In-place marking**: temporarily overwrite the visited cell with a sentinel (e.g. `'#'`), restore on backtrack. Saves O(rows × cols) memory vs. a `visited` set.
2. **Early termination** when the search has matched all letters.

## Why we use

- Pure backtracking gives a clean, correct solution that scales fine for typical interview-sized grids.
- The marking trick avoids the extra `set` overhead — important when the grid is large.
- The same skeleton extends to "find all words", "longest path", "max points", etc.
- Pruning is natural — bail out the instant the current cell doesn't match the next letter.

## How to implement

```
def exist(board, word):
    rows, cols = dims(board)
    def dfs(r, c, k):                          # k = index in word
        if k == len(word): return True
        if r < 0 or c < 0 or r >= rows or c >= cols: return False
        if board[r][c] != word[k]: return False
        # CHOOSE: mark visited
        saved, board[r][c] = board[r][c], '#'
        found = (dfs(r+1, c, k+1) or
                 dfs(r-1, c, k+1) or
                 dfs(r, c+1, k+1) or
                 dfs(r, c-1, k+1))
        # UNCHOOSE: restore
        board[r][c] = saved
        return found
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0): return True
    return False
```

Python:

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, k: int) -> bool:
        if k == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[k]:
            return False
        saved = board[r][c]
        board[r][c] = '#'
        found = (
            dfs(r + 1, c, k + 1) or
            dfs(r - 1, c, k + 1) or
            dfs(r, c + 1, k + 1) or
            dfs(r, c - 1, k + 1)
        )
        board[r][c] = saved
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

JavaScript:

```javascript
function exist(board, word) {
  const rows = board.length, cols = board[0].length;
  function dfs(r, c, k) {
    if (k === word.length) return true;
    if (r < 0 || c < 0 || r >= rows || c >= cols) return false;
    if (board[r][c] !== word[k]) return false;
    const saved = board[r][c];
    board[r][c] = '#';
    const found =
      dfs(r + 1, c, k + 1) ||
      dfs(r - 1, c, k + 1) ||
      dfs(r, c + 1, k + 1) ||
      dfs(r, c - 1, k + 1);
    board[r][c] = saved;
    return found;
  }
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (dfs(r, c, 0)) return true;
    }
  }
  return false;
}
```

Invariant: at every recursive call, the path of cells leading to `(r, c)` is currently marked `'#'` on the board; on return, every one is restored to its original character.

## Visual

```
board:                  word: "ABCCED"
[ A B C E ]
[ S F C S ]
[ A D E E ]

path: (0,0) A → (0,1) B → (0,2) C → (1,2) C → (2,2) E → (2,1) D
```

## Which problems this approach solves in the real world

- **OCR / scrabble assistance**: find a word in a tile rack laid on a grid.
- **Crossword validation**: check whether a partial fill is consistent with the dictionary.
- **DNA / protein analysis**: find a motif walkable through a 2D alignment grid.
- **Game AI**: pathfinding on a grid where the path must spell something or avoid revisits.
- **Maze with state**: "can I reach the exit collecting these tokens in order?"
- **Test generation**: enumerate all valid words on a randomly seeded letter grid.

## Pros and cons

**Pros**
- Simple, recognisable backtracking template.
- O(1) extra memory beyond recursion stack — uses the board itself for visited marks.
- Early termination — first match wins, returns up the chain instantly.
- Adapts to "find all words" with minor tweaks (use a Trie, accumulate hits).

**Cons**
- In-place marking **mutates the input**; the caller may not expect that. Always restore (the unchoose step) before returning.
- Worst-case O(rows × cols × 4^L) where L = word length; can be slow for very long words.
- The four `dfs(...)` calls are easy to typo (wrong delta) — be careful with direction signs.

## Limitations

- For **multiple word queries** on the same board, this naïve approach repeats work; use Trie + DFS for "Word Search II" style problems.
- Doesn't extend to revisits — by definition, the path must be cell-disjoint.
- For very long words on small alphabets, branching explodes — heuristics or constraint propagation needed.

## One example

**Problem**: Given an `m × n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid. The word can be constructed from letters of sequentially **adjacent** cells (horizontally or vertically). The same letter cell may **not** be used more than once.
Constraints: `1 ≤ m, n ≤ 6`, `1 ≤ word.length ≤ 15`, letters are uppercase/lowercase English.

**Input**:
```
board = [["A","B","C","E"],
         ["S","F","C","S"],
         ["A","D","E","E"]]
word  = "ABCCED"
```
**Output**: `true`.

## Solution explanation

The code above. Walk-through, tracking `(r, c, k)` and the running marked path:

| step | (r, c, k) | board[r][c] | matches word[k]? | mark | next call           |
|------|-----------|--------------|--------------------|------|---------------------|
| 1    | (0,0,0)   | A            | A ✓                | #    | try down (1,0,1)   |
| 2a   | (1,0,1)   | S            | B ✗                | —    | return false       |
| 2b   | (0,1,1)   | B            | B ✓                | #    | try down (1,1,2)   |
| 3a   | (1,1,2)   | F            | C ✗                | —    | return false       |
| 3b   | (0,2,2)   | C            | C ✓                | #    | try down (1,2,3)   |
| 4    | (1,2,3)   | C            | C ✓                | #    | try down (2,2,4)   |
| 5    | (2,2,4)   | E            | E ✓                | #    | try down out, try up (back to (1,2,5)) etc., try right (2,3,5) |
| 6a   | (2,3,5)   | E            | D ✗                | —    | return false       |
| 6b   | (2,1,5)   | D            | D ✓                | #    | k+1 == len(word) → **true** |

Returns true. All marked cells are restored on the way back up.

Correctness: by induction on `k`. When the DFS at `(r, c, k)` returns true, we have matched `word[0..k]` along a path of marked cells ending at `(r, c)`. The marking ensures we never revisit a cell within the same path. Restoring on backtrack preserves the board for sibling explorations.

- **Time**: worst case O(rows · cols · 4^L) — each starting cell launches a tree of depth L and branching 4 (minus the cell you came from in practice).
- **Space**: O(L) recursion stack.

## Practice questions

| Difficulty | Problem | Link |
|------------|---------|------|
| Easy | **Flood Fill** — pure DFS on a grid; no backtracking but identical structure for grid traversal. | https://leetcode.com/problems/flood-fill/ |
| Medium | **Word Search** — the canonical problem above. | https://leetcode.com/problems/word-search/ |
| Hard | **Word Search II** — find all words in a list; build a Trie + DFS to share prefix work across queries. | https://leetcode.com/problems/word-search-ii/ |
