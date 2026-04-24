"""
Solution: Autocomplete System

This solution demonstrates two approaches:
1. Brute force - simple filtering and sorting
2. Optimized - Trie data structure for efficient prefix search

The Trie approach reduces search from O(N log N) per query to O(M + K log K)
where M is prefix length and K is number of results.
"""

from typing import List
import csv


class AutocompleteBuilder:
    def __init__(self):
        self.words = []

    def load_from_file(self, filepath: str) -> None:
        with open(filepath, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                word, freq = row[0], int(row[1])
                self.words.append((word, freq))

    def add_word(self, word: str, frequency: int) -> None:
        self.words.append((word, frequency))

    def get_all_words(self) -> List[tuple]:
        return self.words


class TrieNode:
    def __init__(self):
        self.children = {}
        self.frequency = 0
        self.is_word = False
        self.word = ""


class Trie:
    """
    Trie (prefix tree) for efficient prefix-based lookups.

    Each node represents a character. Words are stored by marking nodes
    as word endings and storing frequency at that node.

    Time complexity:
    - Insert: O(M) where M is word length
    - Search prefix: O(M) to traverse to prefix node
    - Get top-k: O(K log K) to collect and sort results

    Space complexity: O(total characters) = O(N * M_avg)

    vs Brute force:
    - Brute force search: O(N * M) to check each word's prefix
    - Plus O(N log N) to sort all matches
    - Trie reduces this to O(M + K log K) where K is typically << N
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, frequency: int) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
        node.frequency = frequency
        node.word = word

    def _collect_all(self, node: TrieNode) -> List[tuple]:
        results = []
        if node.is_word:
            results.append((node.frequency, node.word))
        for char, child in node.children.items():
            results.extend(self._collect_all(child))
        return results

    def search_prefix(self, prefix: str) -> List[tuple]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_all(node)


class Autocomplete:
    def __init__(self, words: List[tuple]):
        self.words = words
        self.trie = Trie()
        for word, freq in words:
            self.trie.insert(word, freq)

    def search(self, prefix: str) -> List[tuple]:
        results = self.trie.search_prefix(prefix)
        return [(word, freq) for freq, word in sorted(results, reverse=True)]

    def search_top_k(self, prefix: str, k: int) -> List[tuple]:
        results = self.trie.search_prefix(prefix)
        return [(word, freq) for freq, word in sorted(results, reverse=True)[:k]]


def brute_force_search(words: List[tuple], prefix: str) -> List[tuple]:
    """
    Brute force approach: filter all words, then sort.

    Time: O(N * M) to check prefix + O(N log N) to sort matches
    Space: O(N) for the filtered list

    Where N = number of words, M = average word length
    """
    matches = [(w, f) for w, f in words if w.startswith(prefix)]
    return sorted(matches, key=lambda x: x[1], reverse=True)


def brute_force_top_k(words: List[tuple], prefix: str, k: int) -> List[tuple]:
    """
    Brute force top-k: filter all, sort, take k.

    Time: O(N * M) to check prefix + O(N log N) to sort + O(k) to slice
    Space: O(N) for the filtered list
    """
    matches = [(w, f) for w, f in words if w.startswith(prefix)]
    return sorted(matches, key=lambda x: x[1], reverse=True)[:k]