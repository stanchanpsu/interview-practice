"""
Autocomplete System

Builds an autocomplete data structure from a file of words with frequencies.
Supports prefix-based search and top-k results sorted by frequency.

Example usage:
    builder = AutocompleteBuilder()
    builder.load_from_file("data/words.txt")
    ac = Autocomplete(builder.get_all_words())
    results = ac.search("car")
    top_results = ac.search_top_k("app", 3)
"""

from typing import List, Tuple


class AutocompleteBuilder:
    """
    Builds the autocomplete data structure from a file or manual input.

    Data format (CSV): word,frequency per line
    """

    def __init__(self):
        self.words = []

    def load_from_file(self, filepath: str) -> None:
        """
        Load words and frequencies from a CSV file.

        Each line in the file should be: word,frequency

        Args:
            filepath: Path to the CSV file with word,frequency per line.

        Returns:
            None (modifies internal state)
        """
        raise NotImplementedError()

    def add_word(self, word: str, frequency: int) -> None:
        """
        Add a single word with its frequency.

        Args:
            word: The word to add.
            frequency: Integer frequency count (e.g., search popularity).

        Returns:
            None (modifies internal state)
        """
        raise NotImplementedError()

    def get_all_words(self) -> List[Tuple[str, int]]:
        """
        Return all words with their frequencies.

        Returns:
            List of (word, frequency) tuples.
        """
        raise NotImplementedError()


class Autocomplete:
    """
    Autocomplete search over a fixed word list.

    Supports prefix-based search and top-k results sorted by frequency.
    """

    def __init__(self, words: List[Tuple[str, int]]):
        """
        Initialize with a list of (word, frequency) tuples.

        Args:
            words: List of (word, frequency) tuples from AutocompleteBuilder.
        """
        self.words = words

    def search(self, prefix: str) -> List[Tuple[str, int]]:
        """
        Find all words starting with the given prefix, sorted by frequency descending.

        Args:
            prefix: The prefix string to search for (e.g., "car").

        Returns:
            List of (word, frequency) tuples, sorted by frequency descending.
            Returns empty list if no matches found.
        """
        raise NotImplementedError()

    def search_top_k(self, prefix: str, k: int) -> List[Tuple[str, int]]:
        """
        Find the top k words starting with the given prefix, sorted by frequency descending.

        Args:
            prefix: The prefix string to search for.
            k: Maximum number of results to return.

        Returns:
            List of up to k (word, frequency) tuples, sorted by frequency descending.
            Returns empty list if no matches found.
        """
        raise NotImplementedError()