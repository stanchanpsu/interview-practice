# Recurring Transactions

Real-world style interview problem involving transaction analysis, date grouping, and pattern detection.

## Context

You have a list of credit/debit card transactions spanning ~2 years. Each transaction has a date, merchant name, amount, and category. Your task is to identify transactions that occur on a "weekly recurring" basis - meaning they happen roughly once per 7-day window, with consistent amounts and the same merchant.

This tests grouping, date arithmetic, and the ability to define and measure "recurrence" in messy real-world data.

## Data Format

The data file `data/transactions.txt` contains one transaction per line in colon-delimited format:
```
date | merchant | amount | category
```

Example:
```
2023-01-03 | rent_payment | 1500.00 | housing
2023-01-07 | netflix_subscription | 15.99 | entertainment
2023-01-10 | coffee_shop | 6.50 | food
```

## Run Tests

```bash
# Test user implementation (should fail until implemented)
python3 tests/test_transactions.py

# Test solution
python3 tests/test_transactions.py --solution
```

See `solution/solution.py` for a reference implementation.

Requires Python 3 only (uses stdlib `unittest`). No extra dependencies.

## Implementation Guidance

### Core (MVP - 20-30 min)
These must pass for a basic solution:

1. **`load_transactions(filepath)`** - Parse the transaction file into a list of dicts
2. **`group_by_merchant(transactions)`** - Group all transactions by merchant name
3. **`find_weekly_recurring(transactions, tolerance_days=3)`** - Find transactions that recur roughly weekly. Returns a list of recurring groups, each containing (merchant, avg_amount, count, dates)

### Followups (if time permits)
These add full functionality for a complete solution:

1. **`find_monthly_recurring(transactions, tolerance_days=5)`** - Find transactions that recur roughly monthly (within tolerance window)
2. **Time complexity optimization** - Analyze and optimize the O(n*g) scan where n=transactions, g=unique merchants
3. **Merchant name normalization** - Handle slight name variations (e.g., "Netflix" vs "netflix" vs "Netflix Subscription")

## Usage Example

```python
transactions = load_transactions("data/transactions.txt")

recurring = find_weekly_recurring(transactions, tolerance_days=3)
# Returns: [
#     {
#         "merchant": "netflix_subscription",
#         "avg_amount": 15.99,
#         "count": 24,
#         "dates": ["2023-01-07", "2023-02-07", ...]
#     },
#     ...
# ]

# Monthly recurring (rent, gym, subscriptions)
monthly = find_monthly_recurring(transactions, tolerance_days=5)
```