#!/usr/bin/env python3
"""
Test suite using only stdlib unittest.
Run with: python test_network.py              (boilerplate)
         python test_network.py --solution   (solution)
"""

import unittest
import sys
import os

SOLUTION_MODE = "--solution" in sys.argv
if SOLUTION_MODE:
    sys.argv.remove("--solution")

if SOLUTION_MODE:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "solution"))
    from solution import (
        load_friendships,
        get_friends,
        get_friends_of_friends,
        shortest_path,
        strongest_connection,
    )
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from network import (
        load_friendships,
        get_friends,
        get_friends_of_friends,
        shortest_path,
        strongest_connection,
    )


class TestLoadFriendships(unittest.TestCase):
    def test_loads_data(self):
        network = load_friendships()
        self.assertIsNotNone(network)

    def test_bidirectional(self):
        network = load_friendships()
        self.assertIn("Alice", network)
        self.assertIn("Bob", network["Alice"])


class TestGetFriends(unittest.TestCase):
    def test_alice_friends(self):
        network = load_friendships()
        friends = get_friends("Alice", network)
        self.assertIn("Bob", friends)
        self.assertIn("Charlie", friends)
        self.assertIn("Frank", friends)

    def test_no_friends(self):
        network = load_friendships()
        friends = get_friends("Nobody", network)
        self.assertEqual(friends, [])


class TestGetFriendsOfFriends(unittest.TestCase):
    def test_excludes_direct_friends(self):
        network = load_friendships()
        fof = get_friends_of_friends("Alice", network)
        self.assertNotIn("Bob", fof)
        self.assertNotIn("Charlie", fof)
        self.assertNotIn("Frank", fof)

    def test_includes_real_fof(self):
        network = load_friendships()
        fof = get_friends_of_friends("Alice", network)
        self.assertIn("David", fof)
        self.assertIn("Eve", fof)


class TestShortestPath(unittest.TestCase):
    def test_same_user(self):
        network = load_friendships()
        self.assertEqual(shortest_path("Alice", "Alice", network), 0)

    def test_direct_friend(self):
        network = load_friendships()
        self.assertEqual(shortest_path("Alice", "Bob", network), 1)

    def test_two_hops(self):
        network = load_friendships()
        self.assertEqual(shortest_path("Alice", "David", network), 2)

    def test_no_path(self):
        network = load_friendships()
        self.assertEqual(shortest_path("Alice", "NonExistent", network), -1)


class TestStrongestConnection(unittest.TestCase):
    def test_alice_strongest(self):
        network = load_friendships()
        friend, strength = strongest_connection("Alice", network)
        self.assertEqual(friend, "Frank")
        self.assertEqual(strength, 5)

    def test_no_friends(self):
        network = load_friendships()
        self.assertIsNone(strongest_connection("Nobody", network))


if __name__ == "__main__":
    unittest.main()