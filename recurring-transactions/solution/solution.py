"""
Recurring Transactions - Reference Implementation

This module provides functions to parse card transaction data and identify
recurring transactions (weekly and monthly patterns).

Key algorithms:
- Grouping by merchant using a hash map
- Detecting weekly recurrence by analyzing gaps between transaction dates
  using a sliding window / two-pointer approach
- Variance calculation for amount consistency

The log format is:
    date | merchant | amount | category

Example:
    2023-01-03 | rent_payment | 1500.00 | housing
"""

from datetime import datetime, timedelta
from collections import defaultdict


def load_transactions(filepath):
    """
    Parse a transaction file and return a list of structured entries.

    Each line is split by '|' and parsed into a dictionary with keys:
        date, merchant, amount, category

    Malformed lines (wrong number of fields, non-numeric amount) are
    silently skipped.

    Args:
        filepath: Path to the transaction file.

    Returns:
        List of dicts, e.g.:
        [{
            "date": "2023-01-03",
            "merchant": "rent_payment",
            "amount": 1500.00,
            "category": "housing"
        }, ...]
    """
    transactions = []
    with open(filepath, "r") as f:
        for line in f:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                continue
            try:
                date, merchant, amount, category = parts
                transactions.append({
                    "date": date,
                    "merchant": merchant,
                    "amount": float(amount),
                    "category": category
                })
            except (ValueError, IndexError):
                continue
    return transactions


def group_by_merchant(transactions):
    """
    Group all transactions by merchant name.

    Uses a hash map (dict) where keys are merchant names and values
    are lists of transactions for that merchant.

    Args:
        transactions: List of transaction dicts.

    Returns:
        Dict mapping merchant name (str) to list of transaction dicts.
        e.g.: {"netflix": [tx1, tx2], "rent": [tx3, tx4]}
    """
    groups = defaultdict(list)
    for txn in transactions:
        groups[txn["merchant"]].append(txn)
    return dict(groups)


def _parse_date(date_str):
    """
    Parse a date string in YYYY-MM-DD format to a datetime.date object.
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def _is_roughly_periodic(dates, period_days, tolerance_days):
    """
    Check if a list of sorted dates follows a recurring periodic pattern.

    Uses a sliding window / two-pointer approach: for each consecutive pair
    of dates, we check if the gap is within [period_days - tolerance_days,
    period_days + tolerance_days]. A valid periodic sequence should have
    at least min_valid_gaps of such matches.

    Args:
        dates: List of date strings, sorted in ascending order.
        period_days: Expected period between transactions (e.g., 7 for weekly).
        tolerance_days: Acceptable deviation from the exact period.

    Returns:
        Tuple of (is_periodic: bool, valid_gap_count: int, total_gaps: int)
    """
    if len(dates) < 2:
        return False, 0, 0

    min_valid_gaps = len(dates) - 1

    valid_gaps = 0
    for i in range(len(dates) - 1):
        d1 = _parse_date(dates[i])
        d2 = _parse_date(dates[i + 1])
        gap = (d2 - d1).days

        if abs(gap - period_days) <= tolerance_days:
            valid_gaps += 1

    return valid_gaps >= min_valid_gaps, valid_gaps, len(dates) - 1


def find_weekly_recurring(transactions, tolerance_days=3):
    """
    Find transactions that recur on a roughly weekly basis.

    A transaction is considered "weekly recurring" if:
    1. The merchant has at least 3 transactions in the dataset
    2. The gaps between consecutive transactions are approximately
       7 days (within tolerance_days)

    Uses group_by_merchant to bucket transactions, then applies
    _is_roughly_periodic with period_days=7 to detect the cadence.

    Args:
        transactions: List of transaction dicts.
        tolerance_days: Max deviation from exact period (default 3 days).
                       So gaps of 4-10 days are accepted for weekly recurrence.

    Returns:
        List of recurring groups, each dict containing:
            - merchant: str
            - avg_amount: float (mean of transaction amounts)
            - count: int (number of occurrences)
            - dates: list of date strings (sorted ascending)
            - amounts: list of floats (raw amounts for variance calc)

        Example:
        [{
            "merchant": "netflix_subscription",
            "avg_amount": 15.99,
            "count": 24,
            "dates": ["2023-01-07", "2023-02-07", ...],
            "amounts": [15.99, 15.99, ...]
        }, ...]
    """
    if not transactions:
        return []

    groups = group_by_merchant(transactions)
    recurring = []

    for merchant, txns in groups.items():
        if len(txns) < 3:
            continue

        # Sort by date
        sorted_txns = sorted(txns, key=lambda t: t["date"])
        dates = [t["date"] for t in sorted_txns]

        # Check if gaps between dates are roughly 7 days
        is_weekly, _, _ = _is_roughly_periodic(dates, period_days=7,
                                               tolerance_days=tolerance_days)
        if not is_weekly:
            continue

        # Compute average amount
        amounts = [t["amount"] for t in sorted_txns]
        avg_amount = sum(amounts) / len(amounts)

        recurring.append({
            "merchant": merchant,
            "avg_amount": round(avg_amount, 2),
            "count": len(txns),
            "dates": dates,
            "amounts": amounts
        })

    return recurring


def find_monthly_recurring(transactions, tolerance_days=5):
    """
    Find transactions that recur on a roughly monthly basis.

    Same approach as find_weekly_recurring but with period_days=30
    and a wider tolerance (5 days) to account for month length variations.

    A transaction is considered "monthly recurring" if:
    1. The merchant has at least 2 transactions
    2. The gaps between consecutive transactions are approximately
       30 days (within tolerance_days)

    Note: Uses 30 days as the period rather than calendar month boundaries
    to simplify comparison. This means 28-35 day gaps are accepted.

    Args:
        transactions: List of transaction dicts.
        tolerance_days: Max deviation from 30-day period (default 5 days).

    Returns:
        List of recurring groups (same format as find_weekly_recurring).
    """
    if not transactions:
        return []

    groups = group_by_merchant(transactions)
    recurring = []

    for merchant, txns in groups.items():
        if len(txns) < 2:
            continue

        sorted_txns = sorted(txns, key=lambda t: t["date"])
        dates = [t["date"] for t in sorted_txns]

        is_monthly, _, _ = _is_roughly_periodic(dates, period_days=30,
                                                 tolerance_days=tolerance_days)
        if not is_monthly:
            continue

        amounts = [t["amount"] for t in sorted_txns]
        avg_amount = sum(amounts) / len(amounts)

        recurring.append({
            "merchant": merchant,
            "avg_amount": round(avg_amount, 2),
            "count": len(txns),
            "dates": dates,
            "amounts": amounts
        })

    return recurring