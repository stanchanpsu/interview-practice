#!/usr/bin/env python3
"""
Test suite using only stdlib unittest.
Run with: python test_analyzer.py              (boilerplate)
         python test_analyzer.py --solution   (solution)
"""

import unittest
import sys
import os

SOLUTION_MODE = "--solution" in sys.argv
if SOLUTION_MODE:
    sys.argv.remove("--solution")

if SOLUTION_MODE:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "solution"))
    from solution import load_logs, get_error_rate, top_endpoints, slowest_requests
    from solution import filter_by_ip, requests_by_hour, detect_anomalies
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from analyzer import load_logs, get_error_rate, top_endpoints, slowest_requests
    from analyzer import filter_by_ip, requests_by_hour, detect_anomalies


class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.logs = load_logs("data/logs.txt")

    def test_load_logs_returns_list(self):
        self.assertIsInstance(self.logs, list)
        self.assertGreater(len(self.logs), 0)

    def test_load_logs_returns_dict_entries(self):
        for entry in self.logs:
            self.assertIn("timestamp", entry)
            self.assertIn("ip", entry)
            self.assertIn("method", entry)
            self.assertIn("path", entry)
            self.assertIn("status", entry)
            self.assertIn("response_time_ms", entry)

    def test_get_error_rate_returns_float(self):
        rate = get_error_rate(self.logs)
        self.assertIsInstance(rate, float)
        self.assertGreaterEqual(rate, 0.0)
        self.assertLessEqual(rate, 100.0)

    def test_get_error_rate_is_reasonable(self):
        rate = get_error_rate(self.logs)
        self.assertLess(rate, 50.0)

    def test_top_endpoints_returns_list(self):
        result = top_endpoints(self.logs, 3)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 3)

    def test_top_endpoints_sorted_by_count(self):
        result = top_endpoints(self.logs, 5)
        counts = [count for _, count in result]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_top_endpoints_contains_tuples(self):
        result = top_endpoints(self.logs, 3)
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], int)

    def test_slowest_requests_returns_k_items(self):
        result = slowest_requests(self.logs, 5)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)

    def test_slowest_requests_sorted_by_time(self):
        result = slowest_requests(self.logs, 10)
        times = [entry["response_time_ms"] for entry in result]
        self.assertEqual(times, sorted(times, reverse=True))

    def test_slowest_requests_returns_dicts(self):
        result = slowest_requests(self.logs, 3)
        for entry in result:
            self.assertIsInstance(entry, dict)
            self.assertIn("response_time_ms", entry)


class TestFollowups(unittest.TestCase):
    def setUp(self):
        self.logs = load_logs("data/logs.txt")

    def test_filter_by_ip_exists(self):
        result = filter_by_ip(self.logs, "192.168.1.10")
        self.assertIsInstance(result, list)

    def test_filter_by_ip_returns_matching_ips(self):
        result = filter_by_ip(self.logs, "192.168.1.10")
        for entry in result:
            self.assertEqual(entry["ip"], "192.168.1.10")

    def test_filter_by_ip_no_match(self):
        result = filter_by_ip(self.logs, "255.255.255.255")
        self.assertEqual(len(result), 0)

    def test_requests_by_hour_exists(self):
        result = requests_by_hour(self.logs)
        self.assertIsInstance(result, dict)

    def test_requests_by_hour_has_hour_keys(self):
        result = requests_by_hour(self.logs)
        for hour in result.keys():
            self.assertIn(hour, range(24))

    def test_detect_anomalies_exists(self):
        result = detect_anomalies(self.logs, 1000)
        self.assertIsInstance(result, list)

    def test_detect_anomalies_returns_entries_above_threshold(self):
        anomalies = detect_anomalies(self.logs, 1000)
        for entry in anomalies:
            self.assertGreater(entry["response_time_ms"], 1000)


class TestLogParserEdgeCases(unittest.TestCase):
    def test_skips_malformed_lines(self):
        logs = load_logs("data/logs.txt")
        valid_entries = all(
            len(entry) == 6 and all(k in entry for k in
                ["timestamp", "ip", "method", "path", "status", "response_time_ms"])
            for entry in logs
        )
        self.assertTrue(valid_entries)


if __name__ == "__main__":
    unittest.main()