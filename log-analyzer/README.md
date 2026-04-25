# Log Analyzer

Real-world style interview problem involving log parsing, aggregation, and anomaly detection.

## Context

You have raw server access logs with mixed formats, timestamps, HTTP methods, status codes, and response times. Your task is to parse these logs, build an in-memory index, and answer analytical queries like "what's the error rate?", "which endpoints are slowest?", and "detect traffic spikes by time window."

Your task is to parse the logs, compute statistics, and surface anomalies.

## Data Format

The data file `data/logs.txt` contains one request per line in a semi-structured format:

```
timestamp | ip | method | path | status | response_time_ms
```

Example:
```
2024-01-15 08:23:41 | 192.168.1.10 | GET | /api/users | 200 | 45
2024-01-15 08:23:42 | 10.0.0.5 | POST | /api/login | 401 | 12
2024-01-15 08:24:01 | 192.168.1.10 | GET | /api/products | 500 | 3200
```

Note: Some lines may have missing fields, extra whitespace, or malformed timestamps to simulate real-world messy data.

## Run Tests

```bash
# Test user implementation (should fail until implemented)
python3 tests/test_analyzer.py

# Test solution
python3 tests/test_analyzer.py --solution
```

See `solution/solution.py` for a reference implementation.

Requires Python 3 only (uses stdlib `unittest`). No extra dependencies.

## Implementation Guidance

### Core (MVP - 20-30 min)
These must pass for a basic solution:

1. **`load_logs(filepath)`** - Parse the log file into a list of structured entries, skipping malformed lines
2. **`get_error_rate(logs)`** - Calculate the percentage of 4xx/5xx responses
3. **`top_endpoints(logs, k)`** - Return the top `k` endpoints by request count
4. **`slowest_requests(logs, k)`** - Return the `k` requests with the highest response times, sorted descending

### Followups (if time permits)
These add full functionality for a complete solution:

1. **`requests_by_hour(logs)`** - Aggregate request counts per hour
2. **`detect_anomalies(logs, threshold)`** - Find requests where response times exceed the threshold
3. **`filter_by_ip(logs, ip)`** - Return all requests from a given IP
4. **`top_endpoints_heap(logs, k)`** - Find top k endpoints using a max-heap instead of sorting (O(n + m*log(k)) vs O(n + m*log(m)))
5. **Robust parsing** - Handle edge cases: missing fields, extra delimiters, timezone variations

## Usage Example

```python
logs = load_logs("data/logs.txt")
# Each entry is a dict: {timestamp, ip, method, path, status, response_time_ms}

error_pct = get_error_rate(logs)
# Returns: 12.5  # 12.5% of requests were 4xx/5xx

top = top_endpoints(logs, 3)
# Returns: [("/api/users", 150), ("/api/products", 120), ("/api/login", 80)]

slow = slowest_requests(logs, 5)
# Returns: [{"path": "/api/reports", "response_time_ms": 5200}, ...]
# Each entry is a full log dict sorted by response time descending
```
