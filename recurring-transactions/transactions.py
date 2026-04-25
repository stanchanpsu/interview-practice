def load_transactions(filepath):
    raise NotImplementedError()


def group_by_merchant(transactions):
    raise NotImplementedError()


def find_weekly_recurring(transactions, tolerance_days=3):
    raise NotImplementedError()


def find_monthly_recurring(transactions, tolerance_days=3):
    raise NotImplementedError()