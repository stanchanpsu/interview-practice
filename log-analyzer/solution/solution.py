"""
Log Analyzer - Reference Implementation

This module provides functions to parse server access logs and answer
common analytical queries: error rates, top endpoints, slowest requests,
IP filtering, hourly traffic breakdown, and anomaly detection.

The log format is:
    timestamp | ip | method | path | status | response_time_ms

Example log line:
    2024-01-15 08:23:41 | 192.168.1.10 | GET | /api/users | 200 | 45
"""

from datetime import datetime


def load_logs(filepath):
    """
    Parse a log file and return a list of structured log entries.

    Each line is split by '|' and parsed into a dictionary with keys:
        timestamp, ip, method, path, status, response_time_ms

    Malformed lines (wrong number of fields, non-integer status/time,
    unparseable data) are silently skipped to handle real-world messy data.

    Args:
        filepath: Path to the log file.

    Returns:
        List of dicts, e.g.:
        [{
            "timestamp": "2024-01-15 08:23:41",
            "ip": "192.168.1.10",
            "method": "GET",
            "path": "/api/users",
            "status": 200,
            "response_time_ms": 45
        }, ...]
    """
    logs = []
    with open(filepath, "r") as f:
        for line in f:
            # Split by pipe, strip whitespace from each field
            parts = [p.strip() for p in line.split("|")]

            # Reject lines that don't have exactly 6 fields (malformed)
            if len(parts) != 6:
                continue

            try:
                timestamp, ip, method, path, status, response_time_ms = parts
                # Convert numeric fields; raise ValueError if parsing fails
                logs.append({
                    "timestamp": timestamp,
                    "ip": ip,
                    "method": method,
                    "path": path,
                    "status": int(status),
                    "response_time_ms": int(response_time_ms)
                })
            except (ValueError, IndexError):
                # Skip lines with non-numeric status or response time
                continue

    return logs


def get_error_rate(logs):
    """
    Calculate the percentage of requests that resulted in 4xx or 5xx errors.

    Uses status code >= 400 as the definition of "error" (covers client
    errors like 401/404 and server errors like 500/503).

    Args:
        logs: List of log dicts from load_logs().

    Returns:
        Float percentage (0.0 to 100.0) of requests that are errors.
        Returns 0.0 for empty log list.
    """
    if not logs:
        return 0.0

    # Count entries where status code is 400 or higher
    error_count = sum(1 for log in logs if log["status"] >= 400)

    # Express as a percentage of total requests
    return (error_count / len(logs)) * 100.0


def top_endpoints(logs, k):
    """
    Find the top K most-frequently accessed endpoints.

    Counts occurrences of each unique path, then returns them sorted
    in descending order by count.

    Args:
        logs: List of log dicts.
        k: Maximum number of endpoints to return.

    Returns:
        List of (path, count) tuples, sorted by count descending.
        e.g.: [("/api/users", 150), ("/api/products", 120), ...]
    """
    counts = {}
    for log in logs:
        path = log["path"]
        counts[path] = counts.get(path, 0) + 1

    sorted_paths = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_paths[:k]


def top_endpoints_heap(logs, k):
    """
    Find the top K most-frequently accessed endpoints using a max-heap.

    This is a heap-based approach that avoids sorting all (path, count)
    pairs. Instead, we maintain a heap of size k: for each path, if it
    belongs in the top k, we insert it; otherwise we skip it.

    Time:  O(n + m*log(k)) where n = len(logs), m = unique paths
    Space: O(m) for the count dict + O(k) for the heap
    vs. sorting approach: O(n + m*log(m)) time, O(m) space

    Args:
        logs: List of log dicts.
        k: Maximum number of endpoints to return.

    Returns:
        List of (path, count) tuples, sorted by count descending.
    """
    import heapq

    counts = {}
    for log in logs:
        path = log["path"]
        counts[path] = counts.get(path, 0) + 1

    # Heap stores (-count, path) tuples so largest count is at top
    # Using negative count because heapq is a min-heap
    heap = []
    for path, count in counts.items():
        if len(heap) < k:
            heapq.heappush(heap, (count, path))
        else:
            # If current path has higher count than smallest in heap, replace
            if count > heap[0][0]:
                heapq.heapreplace(heap, (count, path))

    # Heap now contains top k, but they're in arbitrary order
    # Extract and sort descending for consistent output
    result = sorted(heap, key=lambda x: x[0], reverse=True)
    return [(path, count) for count, path in result]


def slowest_requests(logs, k):
    """
    Find the K requests with the highest response times.

    Sorts all log entries by response_time_ms in descending order
    and returns the top K.

    Args:
        logs: List of log dicts.
        k: Maximum number of requests to return.

    Returns:
        List of log dicts sorted by response_time_ms descending.
        Each dict includes the full log entry (timestamp, ip, method,
        path, status, response_time_ms).
    """
    return sorted(logs, key=lambda x: x["response_time_ms"], reverse=True)[:k]


def filter_by_ip(logs, ip):
    """
    Return all log entries originating from a specific IP address.

    Simple linear filter through the log list.

    Args:
        logs: List of log dicts.
        ip: String IP address to filter by (exact match).

    Returns:
        List of log dicts where entry["ip"] == ip.
    """
    return [log for log in logs if log["ip"] == ip]


def requests_by_hour(logs):
    """
    Aggregate log entries by the hour of day (0-23).

    Extracts the hour from each timestamp (format: "YYYY-MM-DD HH:MM:SS")
    and counts how many requests occurred during each hour.

    Args:
        logs: List of log dicts.

    Returns:
        Dict mapping hour (int 0-23) to request count (int).
        e.g.: {8: 120, 9: 145, 10: 98, ...}
    """
    hourly = {}
    for log in logs:
        # Timestamp format: "2024-01-15 08:23:41"
        # Extract hour from position 11-13 (after the date and space)
        hour = int(log["timestamp"].split(":")[1])
        hourly[hour] = hourly.get(hour, 0) + 1

    return hourly


def detect_anomalies(logs, threshold):
    """
    Find all requests whose response time exceeds a given threshold.

    Useful for identifying slow endpoints, timeouts, or degraded
    service performance.

    Args:
        logs: List of log dicts.
        threshold: Response time in milliseconds. Entries with
                   response_time_ms > threshold are flagged as anomalies.

    Returns:
        List of log dicts where response_time_ms > threshold.
    """
    return [log for log in logs if log["response_time_ms"] > threshold]