"""
Nearest Neighbors

Spatial index for efficient location-based queries using grid bucketing.
Supports finding k nearest places and places within a radius.

Example usage:
    index = SpatialIndex()
    index.load_from_file("data/places.txt")
    nearest = index.find_k_nearest("Central Park", k=3)
    within_radius = index.find_within_radius("Times Square", radius=0.01)
"""

from typing import List, Tuple, Dict, Optional

from utils import euclidean_distance

Point = Tuple[float, float]


class SpatialIndex:
    """
    Spatial index for efficient nearest neighbor queries using grid bucketing.

    The index divides the 2D plane into cells of a given size.
    Points are hashed into cells based on their coordinates.
    Queries only search neighboring cells, avoiding a full scan.

    Attributes:
        cell_size: Size of each grid cell (in same units as coordinates).
    """

    def __init__(self, cell_size: float = 1.0):
        """
        Initialize spatial index with given cell size.

        Args:
            cell_size: Determines grid granularity. Smaller cells = more buckets
                      but faster queries. Should be tuned based on expected point
                      density and query radius.
        """
        self.cell_size = cell_size
        self.buckets: Dict[Tuple[int, int], List[Tuple[str, Point]]] = {}
        self.points: List[Tuple[str, Point]] = []
        self.name_to_coords: Dict[str, Point] = {}
        self.coords_to_name: Dict[Point, str] = {}

    def _get_bucket_key(self, point: Point) -> Tuple[int, int]:
        """
        Get the bucket key for a point based on its coordinates.

        The bucket key determines which cell in the grid the point
        belongs to. Points in the same cell are potential neighbors.

        Args:
            point: A (lat, lon) coordinate tuple.

        Returns:
            Tuple of (cell_x, cell_y) representing the grid cell.
        """
        raise NotImplementedError()

    def insert(self, name: str, point: Point) -> None:
        """
        Insert a place with its name and coordinates into the index.

        Args:
            name: The name of the place (e.g., "Central Park").
            point: A (lat, lon) coordinate tuple.
        """
        raise NotImplementedError()

    def load_from_file(self, filepath: str) -> None:
        """
        Load places from a CSV file.

        Expected format per line: name,lat,lon

        Args:
            filepath: Path to the CSV file.
        """
        raise NotImplementedError()

    def get_all_places(self) -> Dict[str, Point]:
        """
        Return all places as a dict mapping name to coordinates.

        Returns:
            Dict of {place_name: (lat, lon)} for all inserted places.
        """
        raise NotImplementedError()

    def get_coords(self, name: str) -> Optional[Point]:
        """
        Get the coordinates for a place by name.

        Args:
            name: The name of the place.

        Returns:
            A (lat, lon) coordinate tuple if found, None otherwise.
        """
        raise NotImplementedError()

    def find_k_nearest(self, name: str, k: int) -> List[Tuple[str, float]]:
        """
        Find the k nearest places to a given place by name.

        Args:
            name: The name of the reference place.
            k: Number of nearest places to return.

        Returns:
            List of (place_name, distance) tuples sorted by distance ascending.
            The reference place itself is included with distance 0.
        """
        raise NotImplementedError()

    def find_within_radius(self, name: str, radius: float) -> List[Tuple[str, float]]:
        """
        Find all places within a given radius of a reference place.

        Args:
            name: The name of the reference place.
            radius: Maximum distance to include (in same units as coordinates).

        Returns:
            List of (place_name, distance) tuples sorted by distance ascending.
            Only places within the radius are included.
        """
        raise NotImplementedError()