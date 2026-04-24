"""
Autocomplete System

Example usage:
    builder = AutocompleteBuilder()
    builder.load_from_file("data/words.txt")
    ac = Autocomplete(builder.get_all_words())
    results = ac.search("car")
    top_results = ac.search_top_k("app", 3)
"""

from typing import List


class AutocompleteBuilder:
    """
    Builds the autocomplete data structure from a file.

    Each line in the file is: word,frequency
    """

    def __init__(self):
        self.words = []

    def load_from_file(self, filepath: str) -> None:
        """
        Load words and frequencies from a CSV file.
        Each line: word,frequency
        """
        pass

    def add_word(self, word: str, frequency: int) -> None:
        """Add a single word with its frequency."""
        pass

    def get_all_words(self) -> List[tuple]:
        """Return all words with frequencies as list of (word, frequency) tuples."""
        pass


class Autocomplete:
    def __init__(self, words: List[tuple]):
        self.words = words

    def search(self, prefix: str) -> List[tuple]:
        """
        Find all words starting with prefix, sorted by frequency descending.
        Returns list of (word, frequency) tuples.
        """
        pass

    def search_top_k(self, prefix: str, k: int) -> List[tuple]:
        """
        Find top k words starting with prefix, sorted by frequency descending.
        Returns list of (word, frequency) tuples.
        """
        pass