"""
Solution: Friendship Network Analysis
"""

from collections import deque


def load_friendships(filepath: str) -> dict:
    network = {}
    with open(filepath) as f:
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
    if user not in network:
        return []
    return list(network[user].keys())


def get_friends_of_friends(user: str, network: dict) -> list:
    if user not in network:
        return []

    visited = set([user])
    visited.update(network[user].keys())

    queue = deque([(user, 0)])
    queue.extend((friend, 1) for friend in network[user])

    fof = []
    while queue:
        person, depth = queue.popleft()
        if person in visited:
            continue
        visited.add(person)
        if depth == 1:
            fof.append(person)
        for friend in network.get(person, {}):
            if friend not in visited:
                queue.append((friend, depth + 1))

    return fof


def shortest_path(user1: str, user2: str, network: dict) -> int:
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
    if user not in network or not network[user]:
        return None
    friend = max(network[user], key=network[user].get)
    return (friend, network[user][friend])