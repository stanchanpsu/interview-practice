# Friendship Network

Coding interview practice problem.

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