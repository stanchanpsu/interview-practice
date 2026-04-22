"""
Solution: Friendship Network Analysis

Example usage:
    network = load_friendships()
    friends = get_friends("Alice", network)
"""

import os
from collections import deque

DATA_FILE = "../data/friendships.txt"


def load_friendships() -> dict:
    """
    Build an undirected graph from the data file.
    Each person maps to a dict of {neighbor: strength} for O(1) lookups.
    """
    network = {}
    with open(DATA_FILE) as f:
        for line in f:
            person1, person2, strength = line.strip().split(":")
            strength = int(strength)
            if person1 not in network:
                network[person1] = {}
            if person2 not in network:
                network[person2] = {}
            network[person1][person2] = strength
            network[person2][person1] = strength
    return network


def get_friends(user: str, network: dict) -> list:
    """
    Direct lookup in the adjacency list. O(1) to check existence, O(k) to list friends.
    """
    if user not in network:
        return []
    return list(network[user].keys())


def get_friends_of_friends(user: str, network: dict) -> list:
    """
    For each direct friend, collect their friends (excluding self and direct friends).
    Uses set for O(1) membership checks. Overall O(V + E) where V=users, E=friendships.
    """
    if user not in network:
        return []

    direct_friends = set(network[user].keys())
    visited = set([user]) | direct_friends

    fof = set()
    for friend in direct_friends:
        for fof_candidate in network[friend]:
            if fof_candidate not in visited:
                fof.add(fof_candidate)

    return list(fof)


def shortest_path(user1: str, user2: str, network: dict) -> int:
    """
    BFS from user1 until user2 is found. Returns shortest distance (number of hops).
    Uses visited set to avoid revisiting nodes. O(V + E) time, O(V) space.
    """
    if user1 == user2:
        return 0

    visited = set([user1])
    queue = deque([(user1, 0)])

    while queue:
        person, dist = queue.popleft()
        for friend in network.get(person, {}):
            if friend == user2:
                return dist + 1
            if friend not in visited:
                visited.add(friend)
                queue.append((friend, dist + 1))

    return -1


def strongest_connection(user: str, network: dict) -> tuple:
    """
    Find the friend with highest connection strength. Uses max() with key function.
    Returns None if user has no friends. O(k) where k = number of friends.
    """
    if user not in network or not network[user]:
        return None
    friend = max(network[user], key=network[user].get)
    return (friend, network[user][friend])