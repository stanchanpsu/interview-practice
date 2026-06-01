# Kingdomino

Real-world style interview problem involving grid traversal and connected components. Modeled after the end-game scoring of the boardgame **Kingdomino**.

## Context

In [Kingdomino](https://boardgamegeek.com/boardgame/204583/kingdomino), players spend the game drafting and placing domino-shaped tiles into their own 5x5 kingdom. Each tile square shows a terrain type and a number of crowns. By the end of the game, each player has a 5x5 grid of terrain squares — and that's when the scoring begins.

The rule is simple but rewarding: for each **region** of the same terrain (a 4-connected group — up, down, left, right; no diagonals), the score is the number of tiles in that region multiplied by the total number of crowns in that region. A lonely tile with no same-terrain neighbor is its own region of size 1. A single terrain can form multiple disconnected regions, and each is scored independently.

So the problem is: given a completed 5x5 kingdom, parse the grid, find all the regions, and compute the score for each one.

## Data Format

Input is a list of 25 strings in row-major order, top-left to bottom-right. Each string is `<terrain><crowns>`, where `<terrain>` is a single letter (a-e) and `<crowns>` is a non-negative integer.

Example:
```python
cells = [
    "a3", "a1", "b2", "c1", "d5",
    "a2", "a3", "b1", "c3", "d2",
    "c1", "a2", "b4", "d1", "d3",
    "b1", "a5", "c2", "c4", "d4",
    "e1", "e2", "e3", "a4", "d1",
]
```

## Worked Example

Lay out the 25 cells as a 5x5 grid, with the terrain letter in front and the crown count behind it:

```
       col0  col1  col2  col3  col4
row0:    a3    a1    b2    c1    d5
row1:    a2    a3    b1    c3    d2
row2:    c1    a2    b4    d1    d3
row3:    b1    a5    c2    c4    d4
row4:    e1    e2    e3    a4    d1
```

**Steps:** find all 4-connected groups of the same terrain, then for each region multiply the cell count by the sum of its crowns.

- Terrain `a` → 2 regions
- Terrain `b` → 2 regions
- Terrain `c` → 3 regions
- Terrain `d` → 1 region
- Terrain `e` → 1 region

That gives **9 regions** in total. Each one contributes to the kingdom's final score via `cell_count × total_crowns`:

| Region | Cells | Crowns | Score |
|---|---|---|---|
| `a` — top-left blob | 6 | 16 | 96 |
| `a` — lone tile at `(4,3)` | 1 | 4 | 4 |
| `b` — column at col 2 | 3 | 7 | 21 |
| `b` — lone tile at `(3,0)` | 1 | 1 | 1 |
| `c` — top pair `(0,3)–(1,3)` | 2 | 4 | 8 |
| `c` — lone tile at `(2,0)` | 1 | 1 | 1 |
| `c` — bottom pair `(3,2)–(3,3)` | 2 | 6 | 12 |
| `d` — right side, all 6 cells | 6 | 16 | 96 |
| `e` — bottom row | 3 | 6 | 18 |
| **Total** | **25** | **63** | **257** |

Note how the disconnected regions of the same terrain (e.g. the two `a` regions, or the three `c` regions) are listed and scored independently, then summed in. The kingdom's final score is **257**.

