"""
Friendship Network Analysis

Parses social network friendship data and answers queries like mutual friends,
degrees of separation, and strongest connections.

Data format (friendships.txt):
    person1:person2:strength

Where:
    - person1, person2: usernames
    - strength: integer 1-5 (higher = stronger connection)

Example:
    Alice:Bob:3
    Alice:Charlie:5
    Bob:David:4
"""

from typing import Dict, List, Optional, Tuple


def load_friendships(filepath: str = "data/friendships.txt") -> Dict[str, Dict[str, int]]:
    """
    Load friendships from a file and build an in-memory graph.

    The file contains one friendship per line in the format:
        person1:person2:strength

    The graph is bidirectional: if Alice-Bob exists, both Alice and Bob
    have each other as neighbors.

    Args:
        filepath: Path to the friendships data file.

    Returns:
        Graph as an adjacency dict where:
            - Keys are usernames (str)
            - Values are dicts mapping friend names to connection strength (int)
        Example return:
            {
                "Alice": {"Bob": 3, "Charlie": 5},
                "Bob": {"Alice": 3, "David": 4},
                ...
            }
    """
    raise NotImplementedError()


def get_friends(user: str, network: Dict[str, Dict[str, int]]) -> List[str]:
    """
    Get all direct friends of a user.

    Args:
        user: The username to look up.
        network: The graph from load_friendships().

    Returns:
        List of usernames who are direct friends of user.
        Returns empty list if user is not in the network.
    """
    raise NotImplementedError()


def get_friends_of_friends(user: str, network: Dict[str, Dict[str, int]]) -> List[str]:
    """
    Get friends-of-friends (FoF) for a user, excluding direct friends.

    A friend-of-friend is someone who is friends with one of the user's
    direct friends, but is not a direct friend of the user itself.

    Args:
        user: The username to look up.
        network: The graph from load_friendships().

    Returns:
        List of usernames who are friends-of-friends of user.
        Returns empty list if user has no FoF.
    """
    raise NotImplementedError()


def shortest_path(user1: str, user2: str,
                  network: Dict[str, Dict[str, int]]) -> int:
    """
    Find the minimum number of hops between two users (degrees of separation).

    Uses BFS to find the shortest path through the friendship graph.

    Args:
        user1: Starting username.
        user2: Target username.
        network: The graph from load_friendships().

    Returns:
        Minimum number of hops needed to reach user2 from user1.
        Returns 0 if user1 == user2 (same person).
        Returns -1 if no path exists between them.
    """
    raise NotImplementedError()


def strongest_connection(user: str,
                         network: Dict[str, Dict[str, int]]) -> Optional[Tuple[str, int]]:
    """
    Find the friend with the highest connection strength for a given user.

    Args:
        user: The username to look up.
        network: The graph from load_friendships().

    Returns:
        Tuple of (friend_name, strength) for the strongest connection.
        Returns None if user has no friends in the network.
    """
    raise NotImplementedError()