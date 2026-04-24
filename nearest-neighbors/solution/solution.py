"""
Solution: Nearest Neighbors

Spatial index using grid bucketing for efficient nearest neighbor queries.
Supports querying by place name or by coordinates.

This solution demonstrates a practical approach to spatial indexing that avoids
checking every point for each query. Instead, points are organized into a grid,
allowing O(1) average lookup for nearby points.

Key concepts:
- Grid bucketing: divide plane into cells, hash points into buckets
- Spatial hashing: O(1) average insert and query
- Expanding search: start small, grow until we find enough results
- Place names: maintain bidirectional mapping between names and coordinates
"""

import csv
from typing import List, Tuple, Dict, Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import euclidean_distance

Point = Tuple[float, float]


class SpatialIndex:
    """
    Spatial index using grid bucketing for efficient nearest neighbor queries.

    This data structure is commonly used in:
    - GPS systems (finding nearby drivers, restaurants)
    - Game collision detection
    - Recommendation systems
    - GIS and mapping applications

    The key insight is that instead of checking every point for a query,
    we only check buckets that could possibly contain nearby points.

    Supports both coordinate-based queries and place name queries.

    Time complexity:
    - insert: O(1) average - just hash and append
    - find_k_nearest: O(1) average per bucket, expands until k found
    - find_within_radius: O(1) average per bucket checked

    Space: O(n) for storing all points in buckets
    """

    def __init__(self, cell_size: float = 0.01):
        """
        Initialize spatial index with given cell size.

        Default cell_size of 0.01 is appropriate for geographic coordinates
        (approximately 1km cells at Earth's surface).

        Args:
            cell_size: Size of each grid cell in coordinate units
        """
        self.cell_size = cell_size
        self.buckets = {}
        self.points = []
        self.name_to_coords = {}
        self.coords_to_name = {}

    def _get_bucket_key(self, point: Point) -> Tuple[int, int]:
        """
        Map a point to its bucket key using integer division.

        Args:
            point: (lat, lon) coordinates

        Returns:
            (bucket_lat, bucket_lon) integer tuple
        """
        return (int(point[0] / self.cell_size), int(point[1] / self.cell_size))

    def insert(self, name: str, point: Point) -> None:
        """
        Insert a place with name and coordinates.

        Maintains bidirectional mapping between names and coordinates
        to support both name-based and coordinate-based queries.

        Args:
            name: Place name (e.g., "Central Park")
            point: (lat, lon) coordinates
        """
        bucket_key = self._get_bucket_key(point)
        if bucket_key not in self.buckets:
            self.buckets[bucket_key] = []
        self.buckets[bucket_key].append(point)
        self.points.append(point)
        self.name_to_coords[name] = point
        self.coords_to_name[point] = name

    def load_from_file(self, filepath: str) -> None:
        """
        Load places from a CSV file.

        Expected format: name,latitude,longitude per line

        Args:
            filepath: Path to CSV file
        """
        with open(filepath, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                name = row[0]
                lat, lon = float(row[1]), float(row[2])
                self.insert(name, (lat, lon))

    def _get_neighbor_buckets(self, query: Point, radius: float) -> List[Tuple[int, int]]:
        """
        Find all bucket keys that could contain points within radius.

        Args:
            query: Center point of the query
            radius: Search radius in coordinate units

        Returns:
            List of bucket (lat, lon) keys to check
        """
        min_bucket = (int((query[0] - radius) / self.cell_size),
                     int((query[1] - radius) / self.cell_size))
        max_bucket = (int((query[0] + radius) / self.cell_size),
                     int((query[1] + radius) / self.cell_size))

        buckets = []
        for bx in range(min_bucket[0], max_bucket[0] + 1):
            for by in range(min_bucket[1], max_bucket[1] + 1):
                buckets.append((bx, by))
        return buckets

    def _resolve_query(self, query: str) -> Point:
        """
        Resolve a query string to coordinates.

        If query looks like coordinates (contains comma), parse it.
        Otherwise, look up by place name.

        Args:
            query: Place name or "lat,lon" string

        Returns:
            (lat, lon) tuple

        Raises:
            ValueError: if place not found or invalid coordinates
        """
        if "," in query:
            try:
                parts = query.split(",")
                return (float(parts[0].strip()), float(parts[1].strip()))
            except (ValueError, IndexError):
                raise ValueError(f"Invalid coordinates: {query}")
        else:
            if query not in self.name_to_coords:
                raise ValueError(f"Place not found: {query}")
            return self.name_to_coords[query]

    def find_k_nearest(self, query: str, k: int) -> List[Tuple[str, float]]:
        """
        Find the k nearest places to query.

        Query can be a place name or "lat,lon" coordinates.

        Strategy: expand search radius exponentially until we find k points.
        - Start at cell_size
        - Double the radius each iteration
        - Stop when we have at least k candidates
        - Sort candidates and return top k

        Args:
            query: Place name or "lat,lon" coordinates
            k: Number of nearest neighbors to find

        Returns:
            List of (place_name, distance) tuples sorted by distance

        Raises:
            ValueError: if k exceeds number of places or place not found
        """
        if k > len(self.points):
            raise ValueError(f"k={k} exceeds number of places={len(self.points)}")

        query_point = self._resolve_query(query)

        candidates = []
        search_radius = self.cell_size
        checked_buckets = set()

        while len(candidates) < k:
            neighbor_buckets = self._get_neighbor_buckets(query_point, search_radius)

            for bucket_key in neighbor_buckets:
                if bucket_key not in checked_buckets:
                    checked_buckets.add(bucket_key)
                    if bucket_key in self.buckets:
                        for point in self.buckets[bucket_key]:
                            dist = euclidean_distance(point, query_point)
                            name = self.coords_to_name.get(point, "Unknown")
                            candidates.append((name, dist))

            search_radius *= 2

        candidates.sort(key=lambda x: x[1])
        return candidates[:k]

    def find_within_radius(self, query: str, radius: float) -> List[Tuple[str, float]]:
        """
        Find all places within given radius of query.

        Query can be a place name or "lat,lon" coordinates.

        Args:
            query: Place name or "lat,lon" coordinates
            radius: Maximum distance to search

        Returns:
            List of (place_name, distance) tuples sorted by distance
        """
        query_point = self._resolve_query(query)
        neighbor_buckets = self._get_neighbor_buckets(query_point, radius)

        results = []
        for bucket_key in neighbor_buckets:
            if bucket_key in self.buckets:
                for point in self.buckets[bucket_key]:
                    if point == query_point:
                        continue
                    dist = euclidean_distance(point, query_point)
                    if dist <= radius:
                        name = self.coords_to_name.get(point, "Unknown")
                        results.append((name, dist))

        results.sort(key=lambda x: x[1])
        return results

    def get_all_places(self) -> Dict[str, Point]:
        """
        Return all places as dict mapping name to coordinates.

        Returns:
            Dict of {place_name: (lat, lon)}
        """
        return self.name_to_coords.copy()

    def get_coords(self, name: str) -> Optional[Point]:
        """
        Get coordinates for a place by name.

        Args:
            name: Place name

        Returns:
            (lat, lon) tuple or None if not found
        """
        return self.name_to_coords.get(name)