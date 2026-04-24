# Autocomplete

Real-world style interview problem involving prefix matching and data structure design.

## Context

You have a dictionary of words with frequency data (e.g., from search logs). Your task is to build an autocomplete system that efficiently finds all words matching a given prefix, sorted by frequency.

This problem involves string parsing and prefix matching.

## Data Format

The data file `data/words.txt` contains one word per line in CSV format:
```
word,frequency
```

Example:
```
apple,5000
application,3000
car,3500
card,3000
```

## Run Tests

```bash
# Test user implementation (should fail until implemented)
python3 tests/test_autocomplete.py

# Test solution
python3 tests/test_autocomplete.py --solution
```

Requires Python 3 only (uses stdlib `unittest`). No extra dependencies.

## Classes to Implement

**AutocompleteBuilder**
1. `load_from_file(filepath)` - Parse CSV file of word,frequency pairs
2. `add_word(word, frequency)` - Add a single word with its frequency
3. `get_all_words()` - Return all words as list of (word, frequency) tuples

**Autocomplete**
1. `search(prefix)` - Find all words starting with prefix, sorted by frequency descending
2. `search_top_k(prefix, k)` - Find top k words starting with prefix

## Usage Example

```python
builder = AutocompleteBuilder()
builder.load_from_file("data/words.txt")
words = builder.get_all_words()

ac = Autocomplete(words)
results = ac.search("car")
# Returns: [("car", 3500), ("card", 3000), ("care", 2500), ("career", 2000), ("carpet", 1500), ("cart", 1000)]

top_results = ac.search_top_k("app", 3)
# Returns: [("apple", 5000), ("app", 4000), ("application", 3000)]
```