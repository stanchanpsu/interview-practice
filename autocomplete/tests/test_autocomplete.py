#!/usr/bin/env python3
"""
Test suite using only stdlib unittest.
Run with: python test_autocomplete.py              (boilerplate)
         python test_autocomplete.py --solution   (solution)
"""

import unittest
import sys
import os

SOLUTION_MODE = "--solution" in sys.argv
if SOLUTION_MODE:
    sys.argv.remove("--solution")

if SOLUTION_MODE:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "solution"))
    from solution import AutocompleteBuilder, Autocomplete
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from autocomplete import AutocompleteBuilder, Autocomplete


class TestAutocompleteBuilder(unittest.TestCase):
    def test_load_from_file(self):
        builder = AutocompleteBuilder()
        builder.load_from_file("data/words.txt")
        words = builder.get_all_words()
        self.assertGreater(len(words), 50)

    def test_add_word(self):
        builder = AutocompleteBuilder()
        builder.add_word("test", 100)
        words = builder.get_all_words()
        self.assertEqual(len(words), 1)
        self.assertEqual(words[0], ("test", 100))


class TestAutocompleteSearch(unittest.TestCase):
    def setUp(self):
        self.builder = AutocompleteBuilder()
        self.builder.load_from_file("data/words.txt")
        self.ac = Autocomplete(self.builder.get_all_words())

    def test_search_car(self):
        results = self.ac.search("car")
        self.assertGreater(len(results), 0)
        words = [w for w, f in results]
        self.assertIn("car", words)
        self.assertIn("card", words)
        self.assertIn("care", words)
        self.assertIn("career", words)

    def test_search_cat(self):
        results = self.ac.search("cat")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "cat")

    def test_search_no_match(self):
        results = self.ac.search("xyz")
        self.assertEqual(len(results), 0)

    def test_search_apple(self):
        results = self.ac.search("app")
        self.assertGreater(len(results), 0)
        words = [w for w, f in results]
        self.assertIn("apple", words)
        self.assertIn("app", words)
        self.assertIn("application", words)
        self.assertIn("apply", words)

    def test_search_sorted_by_frequency(self):
        results = self.ac.search("car")
        freqs = [f for w, f in results]
        self.assertEqual(freqs, sorted(freqs, reverse=True))


class TestAutocompleteTopK(unittest.TestCase):
    def setUp(self):
        self.builder = AutocompleteBuilder()
        self.builder.load_from_file("data/words.txt")
        self.ac = Autocomplete(self.builder.get_all_words())

    def test_top_k(self):
        results = self.ac.search_top_k("car", 2)
        self.assertLessEqual(len(results), 2)
        self.assertEqual(results[0][0], "car")

    def test_top_k_exact(self):
        results = self.ac.search_top_k("app", 3)
        self.assertEqual(len(results), 3)

    def test_top_k_more_than_exists(self):
        results = self.ac.search_top_k("car", 100)
        all_results = self.ac.search("car")
        self.assertEqual(len(results), len(all_results))


if __name__ == "__main__":
    unittest.main()