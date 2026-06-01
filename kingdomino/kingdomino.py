"""
Kingdomino

Given a 5x5 Kingdomino grid, parse the cells and compute the score for
each 4-connected region of the same terrain.

Data format:
    A flat list of 25 "<terrain><crowns>" strings in row-major order, e.g.
    "a3" means terrain "a" with 3 crowns.

    Example:
        [
            "a3", "a1", "b2", "c1", "d5",
            "a2", "a3", "b1", "c3", "d2",
            "c1", "a2", "b4", "d1", "d3",
            "b1", "a5", "c2", "c4", "d4",
            "e1", "e2", "e3", "a4", "d1",
        ]

Scoring rule:
    A region is a 4-connected group (up/down/left/right; no diagonals) of
    cells sharing the same terrain. A lone cell with no same-terrain
    neighbor is its own region. Disconnected groups of the same terrain
    are scored independently.

    Score per region = cell_count * sum_of_crowns_in_region.
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
               "<terrain><crowns>" (e.g. "a3" -> ("a", 3)).

    Returns:
        5x5 list of lists, where each entry is a (terrain, crowns) tuple.
        Example:
            [
                [("a", 3), ("a", 1), ("b", 2), ("c", 1), ("d", 5)],
                [("a", 2), ("a", 3), ("b", 1), ("c", 3), ("d", 2)],
                ...
            ]
    """
    raise NotImplementedError()


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
        List of region dicts, one per region, each containing:
            - terrain: str
            - cell_count: int
            - total_points: int (sum of crowns in the region)
            - score: int (cell_count * total_points)
        Example (for the worked example in the README):
            [
                {"terrain": "a", "cell_count": 6, "total_points": 16, "score": 96},
                {"terrain": "a", "cell_count": 1, "total_points": 4,  "score": 4},
                {"terrain": "b", "cell_count": 3, "total_points": 7,  "score": 21},
                {"terrain": "b", "cell_count": 1, "total_points": 1,  "score": 1},
                {"terrain": "c", "cell_count": 2, "total_points": 4,  "score": 8},
                {"terrain": "c", "cell_count": 1, "total_points": 1,  "score": 1},
                {"terrain": "c", "cell_count": 2, "total_points": 6,  "score": 12},
                {"terrain": "d", "cell_count": 6, "total_points": 16, "score": 96},
                {"terrain": "e", "cell_count": 3, "total_points": 6,  "score": 18},
            ]
    """
    raise NotImplementedError()
