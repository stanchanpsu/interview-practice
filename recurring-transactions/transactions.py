"""
Recurring Transactions Analysis

Analyzes transaction data to identify recurring patterns like weekly and monthly
subscriptions, payments, and recurring charges.

Data format (transactions.txt):
    date | merchant | amount | category

Where:
    - date: YYYY-MM-DD format
    - merchant: name of the merchant
    - amount: transaction amount as float
    - category: transaction category

Example:
    2023-01-03 | rent_payment | 1500.00 | housing
    2023-01-07 | netflix_subscription | 15.99 | entertainment
    2023-01-10 | coffee_shop | 6.50 | food
"""

from typing import List, Dict


def load_transactions(filepath: str) -> List[Dict]:
    """
    Load transactions from a file and parse into structured data.

    Args:
        filepath: Path to the transactions data file.

    Returns:
        List of transaction dicts with keys: date, merchant, amount, category.
        Example:
            [
                {"date": "2023-01-03", "merchant": "rent_payment", "amount": 1500.00, "category": "housing"},
                {"date": "2023-01-07", "merchant": "netflix_subscription", "amount": 15.99, "category": "entertainment"},
                ...
            ]
    """
    raise NotImplementedError()


def group_by_merchant(transactions: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group transactions by merchant name.

    Args:
        transactions: List of transaction dicts from load_transactions().

    Returns:
        Dict mapping merchant name to list of their transactions.
        Example:
            {
                "netflix_subscription": [
                    {"date": "2023-01-07", "merchant": "netflix_subscription", "amount": 15.99, "category": "entertainment"},
                    {"date": "2023-02-07", "merchant": "netflix_subscription", "amount": 15.99, "category": "entertainment"},
                    ...
                ],
                "rent_payment": [...]
            }
    """
    raise NotImplementedError()


def find_weekly_recurring(transactions: List[Dict], tolerance_days: int = 3) -> List[Dict]:
    """
    Find transactions that recur roughly weekly.

    A transaction is considered weekly recurring if it appears from the same
    merchant at approximately 7-day intervals, within the tolerance window.

    Args:
        transactions: List of transaction dicts from load_transactions().
        tolerance_days: Allowed variance in days between recurring transactions (default: 3).

    Returns:
        List of recurring transaction groups, each containing:
            {
                "merchant": str,
                "avg_amount": float,
                "count": int,
                "dates": list of date strings
            }
        Example:
            [
                {
                    "merchant": "coffee_shop",
                    "avg_amount": 6.50,
                    "count": 52,
                    "dates": ["2023-01-10", "2023-01-17", "2023-01-24", ...]
                },
                ...
            ]
    """
    raise NotImplementedError()


def find_monthly_recurring(transactions: List[Dict], tolerance_days: int = 3) -> List[Dict]:
    """
    Find transactions that recur roughly monthly.

    A transaction is considered monthly recurring if it appears from the same
    merchant at approximately 30-day intervals, within the tolerance window.

    Args:
        transactions: List of transaction dicts from load_transactions().
        tolerance_days: Allowed variance in days between recurring transactions (default: 3).

    Returns:
        List of recurring transaction groups, each containing:
            {
                "merchant": str,
                "avg_amount": float,
                "count": int,
                "dates": list of date strings
            }
        Example:
            [
                {
                    "merchant": "rent_payment",
                    "avg_amount": 1500.00,
                    "count": 24,
                    "dates": ["2023-01-03", "2023-02-03", "2023-03-03", ...]
                },
                ...
            ]
    """
    raise NotImplementedError()