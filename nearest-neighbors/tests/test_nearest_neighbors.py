#!/usr/bin/env python3
"""
Test suite using only stdlib unittest.
Run with: python test_nearest_neighbors.py              (boilerplate)
         python test_nearest_neighbors.py --solution   (solution)
"""

import unittest
import sys
import os
import math

SOLUTION_MODE = "--solution" in sys.argv
if SOLUTION_MODE:
    sys.argv.remove("--solution")

if SOLUTION_MODE:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from utils import euclidean_distance
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "solution"))
    from solution import SpatialIndex
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from utils import euclidean_distance
    from nearest_neighbors import SpatialIndex


class TestEuclideanDistance(unittest.TestCase):
    def test_zero_distance(self):
        self.assertAlmostEqual(euclidean_distance((0, 0), (0, 0)), 0.0)

    def test_correct_distance(self):
        self.assertAlmostEqual(euclidean_distance((0, 0), (3, 4)), 5.0)

    def test_negative_coordinates(self):
        self.assertAlmostEqual(euclidean_distance((-1, -1), (2, 3)), 5.0)


class TestSpatialIndexInsert(unittest.TestCase):
    def test_insert_single_place(self):
        index = SpatialIndex()
        index.insert("Times Square", (40.758, -73.9855))
        self.assertEqual(len(index.get_all_places()), 1)

    def test_insert_multiple_places(self):
        index = SpatialIndex()
        index.insert("Times Square", (40.758, -73.9855))
        index.insert("Central Park", (40.7829, -73.9654))
        self.assertEqual(len(index.get_all_places()), 2)


class TestSpatialIndexLoadFromFile(unittest.TestCase):
    def test_loads_all_places(self):
        index = SpatialIndex()
        index.load_from_file("data/places.txt")
        self.assertEqual(len(index.get_all_places()), 20)


class TestSpatialIndexGetCoords(unittest.TestCase):
    def setUp(self):
        self.index = SpatialIndex()
        self.index.load_from_file("data/places.txt")

    def test_get_coords_by_name(self):
        coords = self.index.get_coords("Central Park")
        self.assertIsNotNone(coords)
        self.assertAlmostEqual(coords[0], 40.7829)
        self.assertAlmostEqual(coords[1], -73.9654)

    def test_get_coords_not_found(self):
        coords = self.index.get_coords("NonExistent Place")
        self.assertIsNone(coords)


class TestSpatialIndexKNearest(unittest.TestCase):
    def setUp(self):
        self.index = SpatialIndex()
        self.index.load_from_file("data/places.txt")

    def test_finds_exact_k(self):
        results = self.index.find_k_nearest("Times Square", k=3)
        self.assertEqual(len(results), 3)

    def test_results_sorted(self):
        results = self.index.find_k_nearest("Times Square", k=5)
        distances = [d for n, d in results]
        self.assertEqual(distances, sorted(distances))

    def test_k_less_than_total(self):
        results = self.index.find_k_nearest("Times Square", k=1)
        self.assertEqual(len(results), 1)

    def test_query_at_place_location(self):
        results = self.index.find_k_nearest("Central Park", k=1)
        self.assertAlmostEqual(results[0][1], 0.0, places=5)

    def test_query_by_coordinates(self):
        results = self.index.find_k_nearest("40.758,-73.9855", k=3)
        self.assertEqual(len(results), 3)


class TestSpatialIndexWithinRadius(unittest.TestCase):
    def setUp(self):
        self.index = SpatialIndex()
        self.index.load_from_file("data/places.txt")

    def test_finds_places_in_radius(self):
        results = self.index.find_within_radius("Times Square", radius=0.02)
        self.assertGreater(len(results), 0)
        for name, dist in results:
            self.assertLessEqual(dist, 0.02)

    def test_results_sorted(self):
        results = self.index.find_within_radius("Times Square", radius=0.05)
        distances = [d for n, d in results]
        self.assertEqual(distances, sorted(distances))

    def test_no_places_in_radius(self):
        results = self.index.find_within_radius("Times Square", radius=0.0001)
        self.assertEqual(len(results), 0)

    def test_query_by_coordinates(self):
        results = self.index.find_within_radius("40.758,-73.9855", radius=0.02)
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()