"""
Shared utilities for nearest neighbors problem.
"""

import math
from typing import Tuple

Point = Tuple[float, float]


def euclidean_distance(p1: Point, p2: Point) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
