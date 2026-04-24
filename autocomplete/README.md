# Autocomplete

Real-world style interview problem involving prefix matching and data structure design.

## Context

You have a dictionary of words with frequency data (e.g., from search logs). Your task is to build an autocomplete system that efficiently finds all words matching a given prefix, sorted by frequency.

Your task is to build an autocomplete system that finds all words matching a given prefix, sorted by frequency.

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

See `solution/solution.py` for a reference implementation.

Requires Python 3 only (uses stdlib `unittest`). No extra dependencies.

## Implementation Guidance

### Core (MVP - 20-30 min)
These must pass for a basic solution:

1. **`AutocompleteBuilder.load_from_file(filepath)`** - Parse CSV file
2. **`AutocompleteBuilder.add_word(word, frequency)`** - Add single word
3. **`AutocompleteBuilder.get_all_words()`** - Return all words as list
4. **`Autocomplete.search(prefix)`** - Find all matching words sorted by frequency

### Followups (if time permits)
These add full functionality for a complete solution:

1. **`Autocomplete.search_top_k(prefix, k)`** - Find top k matches by frequency
2. **Performance optimization** - Improve prefix lookup speed for large datasets
3. **Case insensitivity** - Handle "APP" -> "apple"
4. **Empty/no-match handling** - Return empty list for no matches

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