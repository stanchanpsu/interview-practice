"""
Kingdomino - Reference Implementation

This module parses a 5x5 Kingdomino grid and computes the score for
each 4-connected region of the same terrain.

Key algorithms:
- Parsing each cell string ("a3" -> ("a", 3))
- Iterative DFS to find 4-connected components
- Score per region = cell_count * sum_of_crowns

The grid format is a flat list of 25 "<terrain><crowns>" strings in
row-major order. The default input is the worked example from the README.
"""

from typing import List, Tuple, Dict


CELLS = [
    "a3", "a1", "b2", "c1", "d5",
    "a2", "a3", "b1", "c3", "d2",
    "c1", "a2", "b4", "d1", "d3",
    "b1", "a5", "c2", "c4", "d4",
    "e1", "e2", "e3", "a4", "d1",
]

GRID_SIZE = 5


def parse_cells(cells: List[str]) -> List[List[Tuple[str, int]]]:
    """
    Parse the flat 25-cell list into a 5x5 grid of (terrain, crowns) tuples.

    Args:
        cells: Flat list of 25 strings in row-major order, each of the form
               "<terrain><crowns>".

    Returns:
        5x5 list of lists, where each entry is a (terrain, crowns) tuple.
    """
    return [
        [(c[0], int(c[1:])) for c in cells[r * GRID_SIZE:(r + 1) * GRID_SIZE]]
        for r in range(GRID_SIZE)
    ]


def _flood(
    grid: List[List[Tuple[str, int]]],
    visited: List[List[bool]],
    terrain: str,
    r: int,
    c: int,
) -> Tuple[int, int]:
    """
    Recursively flood-fill a 4-connected region of the given terrain,
    starting at (r, c). Marks visited cells in-place.

    Args:
        grid: 5x5 grid of (terrain, crowns) tuples from parse_cells().
        visited: 5x5 boolean grid tracking which cells have been claimed.
        terrain: The terrain letter to match against neighbors.
        r, c: Starting cell coordinates.

    Returns:
        (cell_count, total_crowns) for the flooded region.
    """
    visited[r][c] = True
    count = 1
    points = grid[r][c][1]
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if (0 <= nr < GRID_SIZE
                and 0 <= nc < GRID_SIZE
                and not visited[nr][nc]
                and grid[nr][nc][0] == terrain):
            sub_count, sub_points = _flood(grid, visited, terrain, nr, nc)
            count += sub_count
            points += sub_points
    return count, points


def calculate_regions(cells: List[str]) -> List[Dict]:
    """
    Find all 4-connected regions of the same terrain in the 5x5 grid
    and compute each region's score.

    A region is a maximal 4-connected group of cells sharing the same
    terrain (up/down/left/right; no diagonals). A lone cell with no
    same-terrain neighbor is its own region. Disconnected groups of
    the same terrain are scored independently.

    Score formula: cell_count * sum_of_crowns_in_region.

    Args:
        cells: Flat list of 25 strings in row-major order, each of the form
               "<terrain><crowns>".

    Returns:
        List of region dicts, in row-major discovery order, each containing:
            - terrain: str
            - cell_count: int
            - total_points: int (sum of crowns in the region)
            - score: int (cell_count * total_points)
    """
    grid = parse_cells(cells)
    visited = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    regions = []

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if visited[r][c]:
                continue
            terrain, _ = grid[r][c]
            cell_count, total_points = _flood(grid, visited, terrain, r, c)
            regions.append({
                "terrain": terrain,
                "cell_count": cell_count,
                "total_points": total_points,
                "score": cell_count * total_points,
            })
    return regions


if __name__ == "__main__":
    regions = calculate_regions(CELLS)
    total_score = sum(r["score"] for r in regions)
    for r in regions:
        print(f"{r['terrain']}: {r['cell_count']} cells, "
              f"{r['total_points']} crowns, score {r['score']}")
    print(f"\nTotal: {len(regions)} regions, score {total_score}")
