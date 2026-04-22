"""
Friendship Network Analysis

Data format (friendships.txt):
person1:person2:strength
- person1, person2: usernames
- strength: integer 1-5 (higher = stronger connection)

TODO:
1. Parse the data file and load into an appropriate data structure
2. Implement get_friends(user) - returns list of direct friends
3. Implement get_friends_of_friends(user) - returns unique friends-of-friends (excluding direct friends)
4. Implement shortest_path(user1, user2) - BFS to find minimum connections
5. Implement strongest_connection(user) - find user's strongest friendship
"""

from pathlib import Path
from collections import deque
from typing import TextIO


def load_friendships(filepath: str) -> dict:
    """
    Load friendships from file into a data structure.

    TODO: Implement this function
    - Parse the text file
    - Build a graph representation (adjacency list)
    - Return the data structure
    """
    pass


def get_friends(user: str, network: dict) -> list:
    """
    Get list of direct friends for a user.

    TODO: Implement this function
    """
    pass


def get_friends_of_friends(user: str, network: dict) -> list:
    """
    Get friends-of-friends, excluding direct friends.

    TODO: Implement this function
    Hint: Can be done in O(V + E) using BFS
    """
    pass


def shortest_path(user1: str, user2: str, network: dict) -> int:
    """
    Find shortest path between two users (number of hops).
    Return -1 if no path exists.

    TODO: Implement this function
    Hint: Use BFS for unweighted graph
    """
    pass


def strongest_connection(user: str, network: dict) -> tuple:
    """
    Find user's strongest connection as (friend, strength).
    Return None if user has no friends.

    TODO: Implement this function
    """
    pass