#!/usr/bin/env python3
"""
Test suite using only stdlib unittest.
Run with: python test_transactions.py              (boilerplate)
         python test_transactions.py --solution   (solution)
"""

import unittest
import sys
import os

SOLUTION_MODE = "--solution" in sys.argv
if SOLUTION_MODE:
    sys.argv.remove("--solution")

if SOLUTION_MODE:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "solution"))
    from solution import (
        load_transactions, group_by_merchant, find_weekly_recurring,
        find_monthly_recurring
    )
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from transactions import (
        load_transactions, group_by_merchant, find_weekly_recurring,
        find_monthly_recurring
    )


class TestLoadTransactions(unittest.TestCase):
    def setUp(self):
        self.transactions = load_transactions("data/transactions.txt")

    def test_returns_list(self):
        self.assertIsInstance(self.transactions, list)
        self.assertGreater(len(self.transactions), 0)

    def test_each_entry_has_keys(self):
        for entry in self.transactions:
            self.assertIn("date", entry)
            self.assertIn("merchant", entry)
            self.assertIn("amount", entry)
            self.assertIn("category", entry)

    def test_amounts_are_floats(self):
        for entry in self.transactions:
            self.assertIsInstance(entry["amount"], float)


class TestGroupByMerchant(unittest.TestCase):
    def setUp(self):
        self.transactions = load_transactions("data/transactions.txt")

    def test_returns_dict(self):
        result = group_by_merchant(self.transactions)
        self.assertIsInstance(result, dict)

    def test_keys_are_merchant_names(self):
        result = group_by_merchant(self.transactions)
        for merchant in result.keys():
            self.assertIsInstance(merchant, str)

    def test_values_are_lists(self):
        result = group_by_merchant(self.transactions)
        for txns in result.values():
            self.assertIsInstance(txns, list)

    def test_all_transactions_accounted(self):
        result = group_by_merchant(self.transactions)
        total = sum(len(txns) for txns in result.values())
        self.assertEqual(total, len(self.transactions))


class TestFindWeeklyRecurring(unittest.TestCase):
    def setUp(self):
        self.transactions = load_transactions("data/transactions.txt")

    def test_returns_list(self):
        result = find_weekly_recurring(self.transactions)
        self.assertIsInstance(result, list)

    def test_returns_empty_on_empty_input(self):
        result = find_weekly_recurring([])
        self.assertEqual(result, [])

    def test_result_entries_have_required_keys(self):
        result = find_weekly_recurring(self.transactions)
        for group in result:
            self.assertIn("merchant", group)
            self.assertIn("avg_amount", group)
            self.assertIn("count", group)
            self.assertIn("dates", group)

    def test_dates_list_matches_count(self):
        result = find_weekly_recurring(self.transactions)
        for group in result:
            self.assertEqual(len(group["dates"]), group["count"])

    def test_yoga_is_weekly_recurring(self):
        result = find_weekly_recurring(self.transactions)
        merchants = [g["merchant"] for g in result]
        self.assertIn("weekly_yoga_class", merchants)

    def test_rent_is_not_weekly_recurring(self):
        result = find_weekly_recurring(self.transactions)
        merchants = [g["merchant"] for g in result]
        self.assertNotIn("rent_payment", merchants)

    def test_spotify_is_not_weekly_recurring(self):
        result = find_weekly_recurring(self.transactions)
        merchants = [g["merchant"] for g in result]
        self.assertNotIn("spotify_premium", merchants)


class TestFindMonthlyRecurring(unittest.TestCase):
    def setUp(self):
        self.transactions = load_transactions("data/transactions.txt")

    def test_returns_list(self):
        result = find_monthly_recurring(self.transactions)
        self.assertIsInstance(result, list)

    def test_rent_is_monthly_recurring(self):
        result = find_monthly_recurring(self.transactions)
        merchants = [g["merchant"] for g in result]
        self.assertIn("rent_payment", merchants)

    def test_spotify_is_monthly_recurring(self):
        result = find_monthly_recurring(self.transactions)
        merchants = [g["merchant"] for g in result]
        self.assertIn("spotify_premium", merchants)

    def test_coffee_shop_is_not_monthly_recurring(self):
        result = find_monthly_recurring(self.transactions)
        merchants = [g["merchant"] for g in result]
        self.assertNotIn("coffee_shop", merchants)


if __name__ == "__main__":
    unittest.main()