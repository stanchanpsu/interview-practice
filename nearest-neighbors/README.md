# Nearest Neighbors

Real-world style interview problem involving spatial indexing and hash-based bucketing.

## Context

You have a set of named places with coordinates (e.g., locations of stores, landmarks, or sensors). Your task is to build a spatial index that can efficiently answer queries like "find the K nearest places" or "find all places within radius R" of a query place or coordinates.

This problem involves building a spatial index for efficient location queries.

## Data Format

The data file `data/places.txt` contains one place per line in CSV format:
```
name,lat,lon
```

Example:
```
Central Park,40.7829,-73.9654
Times Square,40.7580,-73.9855
Grand Central,40.7527,-73.9772
```

## Run Tests

```bash
# Test user implementation (should fail until implemented)
python3 tests/test_nearest_neighbors.py

# Test solution
python3 tests/test_nearest_neighbors.py --solution
```

See `solution/solution.py` for a reference implementation.

Requires Python 3 only (uses stdlib `unittest`). No extra dependencies.

## Implementation Guidance

### Core (MVP - 20-30 min)
These must pass for a basic solution:

1. **`insert(name, point)`** - Store a place with its coordinates
2. **`load_from_file(filepath)`** - Load places from CSV file
3. **`get_all_places()`** - Return all places as dict
4. **`get_coords(name)`** - Lookup coordinates by place name
5. **`find_within_radius(name, radius)`** - Find all places within radius

### Followups (if time permits)
These add full functionality for a complete solution:

1. **`find_k_nearest(name, k)`** - Find k nearest places by place name

## Usage Example

```python
index = SpatialIndex()
index.load_from_file("data/places.txt")

nearest = index.find_k_nearest("Times Square", k=3)
# Returns: [("Times Square", 0.0), ...]
# Each result is (name, distance) tuple
```