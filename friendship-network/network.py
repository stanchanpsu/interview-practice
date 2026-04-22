"""
Friendship Network Analysis

Data format (friendships.txt):
person1:person2:strength
- person1, person2: usernames
- strength: integer 1-5 (higher = stronger connection)

TODO:
1. Parse the data file and load into an appropriate data structure
2. Implement get_friends(user) - returns list of direct friends
3. Implement get_friends_of_friends(user) - returns friends of friends (excluding direct friends)
4. Implement shortest_path(user1, user2) - find minimum connections between users
5. Implement strongest_connection(user) - find user's strongest friendship
"""

from collections import deque


def load_friendships() -> dict:
    """
    Load friendships from file.

    Returns:
        dict: Graph as adjacency list where keys are usernames (str)
              and values are dicts mapping friend names to connection strength (int).
              Example: {"Alice": {"Bob": 3, "Charlie": 5}, "Bob": {"Alice": 3}}
    """
    pass


def get_friends(user: str, network: dict) -> list:
    """
    Args:
        user: username string
        network: graph from load_friendships()

    Returns:
        list: usernames of direct friends, empty list if user not in network
    """
    pass


def get_friends_of_friends(user: str, network: dict) -> list:
    """
    Args:
        user: username string
        network: graph from load_friendships()

    Returns:
        list: usernames of friends-of-friends (excludes direct friends),
              empty list if user has no FoF
    """
    pass


def shortest_path(user1: str, user2: str, network: dict) -> int:
    """
    Args:
        user1: starting username
        user2: target username
        network: graph from load_friendships()

    Returns:
        int: minimum hops between users, 0 if same user, -1 if no path
    """
    pass


def strongest_connection(user: str, network: dict) -> tuple:
    """
    Args:
        user: username string
        network: graph from load_friendships()

    Returns:
        tuple: (friend_name: str, strength: int) of strongest connection,
              None if user has no friends
    """
    pass