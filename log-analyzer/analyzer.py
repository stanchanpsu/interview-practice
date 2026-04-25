"""
Log Analyzer

Parses server access logs and answers analytical queries: error rates,
top endpoints, slowest requests, IP filtering, hourly traffic breakdown,
and anomaly detection.

The log format per line is:
    timestamp | ip | method | path | status | response_time_ms

Example:
    2024-01-15 08:23:41 | 192.168.1.10 | GET | /api/users | 200 | 45
"""

from typing import List, Dict, Tuple


def load_logs(filepath: str) -> List[Dict[str, any]]:
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
    raise NotImplementedError()


def get_error_rate(logs: List[Dict[str, any]]) -> float:
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
    raise NotImplementedError()


def top_endpoints(logs: List[Dict[str, any]], k: int) -> List[Tuple[str, int]]:
    """
    Find the top k most-frequently accessed endpoints.

    Counts occurrences of each unique path, then returns them sorted
    in descending order by count.

    Args:
        logs: List of log dicts.
        k: Maximum number of endpoints to return.

    Returns:
        List of (path, count) tuples, sorted by count descending.
        e.g.: [("/api/users", 150), ("/api/products", 120), ...]
    """
    raise NotImplementedError()


def slowest_requests(logs: List[Dict[str, any]], k: int) -> List[Dict[str, any]]:
    """
    Find the k requests with the highest response times, sorted descending.

    Args:
        logs: List of log dicts.
        k: Maximum number of requests to return.

    Returns:
        List of up to k log dicts sorted by response_time_ms descending.
        Each dict includes: timestamp, ip, method, path, status, response_time_ms.
    """
    raise NotImplementedError()


def filter_by_ip(logs: List[Dict[str, any]], ip: str) -> List[Dict[str, any]]:
    """
    Return all log entries originating from a specific IP address.

    Args:
        logs: List of log dicts.
        ip: String IP address to filter by (exact match).

    Returns:
        List of log dicts where entry["ip"] == ip.
    """
    raise NotImplementedError()


def requests_by_hour(logs: List[Dict[str, any]]) -> Dict[int, int]:
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
    raise NotImplementedError()


def detect_anomalies(logs: List[Dict[str, any]], threshold: float) -> List[Dict[str, any]]:
    """
    Find all requests whose response time exceeds a given threshold.

    Useful for identifying slow endpoints, timeouts, or degraded service.

    Args:
        logs: List of log dicts.
        threshold: Response time in milliseconds. Entries with
                   response_time_ms > threshold are flagged as anomalies.

    Returns:
        List of log dicts where response_time_ms > threshold.
    """
    raise NotImplementedError()