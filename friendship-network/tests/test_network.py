import pytest
from pathlib import Path
from network import (
    load_friendships,
    get_friends,
    get_friends_of_friends,
    shortest_path,
    strongest_connection,
)


FIXTURES = Path(__file__).parent.parent / "data" / "friendships.txt"


class TestLoadFriendships:
    def test_loads_data(self):
        network = load_friendships(str(FIXTURES))
        assert network is not None

    def test_bidirectional(self):
        network = load_friendships(str(FIXTURES))
        assert "Alice" in network
        assert "Bob" in network["Alice"]


class TestGetFriends:
    def test_alice_friends(self):
        network = load_friendships(str(FIXTURES))
        friends = get_friends("Alice", network)
        assert "Bob" in friends
        assert "Charlie" in friends
        assert "Frank" in friends

    def test_no_friends(self):
        network = load_friendships(str(FIXTURES))
        friends = get_friends("Nobody", network)
        assert friends == []


class TestGetFriendsOfFriends:
    def test_excludes_direct_friends(self):
        network = load_friendships(str(FIXTURES))
        fof = get_friends_of_friends("Alice", network)
        assert "Bob" not in fof
        assert "Charlie" not in fof
        assert "Frank" not in fof

    def test_includes_real_fof(self):
        network = load_friendships(str(FIXTURES))
        fof = get_friends_of_friends("Alice", network)
        assert "David" in fof
        assert "Eve" in fof


class TestShortestPath:
    def test_same_user(self):
        network = load_friendships(str(FIXTURES))
        assert shortest_path("Alice", "Alice", network) == 0

    def test_direct_friend(self):
        network = load_friendships(str(FIXTURES))
        assert shortest_path("Alice", "Bob", network) == 1

    def test_two_hops(self):
        network = load_friendships(str(FIXTURES))
        assert shortest_path("Alice", "David", network) == 2

    def test_no_path(self):
        network = load_friendships(str(FIXTURES))
        assert shortest_path("Alice", "NonExistent", network) == -1


class TestStrongestConnection:
    def test_alice_strongest(self):
        network = load_friendships(str(FIXTURES))
        friend, strength = strongest_connection("Alice", network)
        assert friend == "Charlie"
        assert strength == 2

    def test_no_friends(self):
        network = load_friendships(str(FIXTURES))
        assert strongest_connection("Nobody", network) is None