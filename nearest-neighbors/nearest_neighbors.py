"""
Nearest Neighbors

Example usage:
    index = SpatialIndex()
    index.load_from_file("data/places.txt")
    nearest = index.find_k_nearest("Central Park", k=3)
"""

from typing import List, Tuple, Dict, Optional
from utils import euclidean_distance

Point = Tuple[float, float]


class SpatialIndex:
    """
    Spatial index for efficient nearest neighbor queries using grid bucketing.
    Supports querying by place name or by coordinates.

    The index divides the 2D plane into cells of a given size.
    Points are hashed into cells based on their coordinates.
    Queries only search neighboring cells, avoiding full scan.
    """

    def __init__(self, cell_size: float = 1.0):
        """
        Initialize spatial index with given cell size.

        Cell size determines how fine the grid is. Smaller cells = more buckets
        but faster queries. Should be tuned based on expected point density
        and query radius.
        """
        self.cell_size = cell_size
        self.buckets = {}
        self.points = []
        self.name_to_coords = {}
        self.coords_to_name = {}

    def _get_bucket_key(self, point: Point) -> Tuple[int, int]:
        """Get bucket key for a point."""
        pass

    def insert(self, name: str, point: Point) -> None:
        """Insert a place with name and coordinates."""
        pass

    def load_from_file(self, filepath: str) -> None:
        """Load places from file. Format: name,lat,lon per line."""
        pass

    def find_k_nearest(self, name: str, k: int) -> List[Tuple[str, float]]:
        """
        Find k nearest places to a place by name.
        Returns list of (place_name, distance) tuples sorted by distance.
        """
        pass

    def find_within_radius(self, name: str, radius: float) -> List[Tuple[str, float]]:
        """
        Find all places within radius of a place by name.
        Returns list of (place_name, distance) tuples sorted by distance.
        """
        pass

    def get_all_places(self) -> Dict[str, Point]:
        """Return all places as dict mapping name to coordinates."""
        pass

    def get_coords(self, name: str) -> Optional[Point]:
        """Get coordinates for a place by name."""
        pass