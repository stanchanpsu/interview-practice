# Friendship Network

Real-world style interview problem involving graph traversal and data parsing.

## Context

You have a dump of social network friendship data. Your task is to parse this data, build a friendship graph in memory, and answer common social network queries like finding mutual friends, degrees of separation, and strongest connections.

This problem tests file I/O and string parsing skills alongside graph algorithms.

## Run Tests

```bash
# Test user implementation (should fail until implemented)
python tests/test_network.py

# Test solution
python tests/test_network.py --solution
```

Requires Python 3 only (uses stdlib `unittest`). No extra dependencies.

## Functions to Implement

1. `load_friendships()` - Parse file, build graph
2. `get_friends(user, network)` - Direct friends
3. `get_friends_of_friends(user, network)` - Friends-of-friends
4. `shortest_path(user1, user2, network)` - Minimum hops between users
5. `strongest_connection(user, network)` - Find strongest connection