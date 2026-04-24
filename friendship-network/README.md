# Friendship Network

Real-world style interview problem involving graph traversal and data parsing.

## Context

You have a dump of social network friendship data. Your task is to parse this data, build a friendship graph in memory, and answer common social network queries like finding mutual friends, degrees of separation, and strongest connections.

This problem tests file I/O and string parsing skills alongside graph algorithms.

## Data Format

The data file `data/friendships.txt` contains one friendship per line in colon-delimited format:
```
person1:person2:strength
```

Example:
```
Alice:Bob:3
Alice:Charlie:2
Bob:David:4
```

## Run Tests

```bash
# Test user implementation (should fail until implemented)
python tests/test_network.py

# Test solution
python tests/test_network.py --solution
```

Requires Python 3 only (uses stdlib `unittest`). No extra dependencies.

## Functions to Implement

1. `load_friendships()` - Parse file, return network graph as dict
2. `get_friends(user, network)` - Get direct friends of user, returns list
3. `get_friends_of_friends(user, network)` - Get friends-of-friends, excludes direct friends
4. `shortest_path(user1, user2, network)` - Find minimum hops, returns -1 if unreachable
5. `strongest_connection(user, network)` - Find friend with highest connection strength

## Usage Example

```python
network = load_friendships()
# network is a dict: {person: {friend: strength, ...}, ...}

friends = get_friends("Alice", network)
# Returns: ["Bob", "Charlie", "Frank"]

fof = get_friends_of_friends("Alice", network)
# Returns: ["David", "Eve"] (excludes Alice's direct friends)

distance = shortest_path("Alice", "David", network)
# Returns: 2 (Alice -> Bob -> David)

connection = strongest_connection("Alice", network)
# Returns: ("Frank", 5)
```