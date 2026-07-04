import json
from pathlib import Path

from expenses.models import Expense

DEFAULT_PATH = Path("expenses.json")


class StorageError(Exception):
    """Raised when the expense file cannot be read or written."""


def load_expenses(path=DEFAULT_PATH):
    path = Path(path)
    if not path.exists():
        return []
    try:
        with open(path) as f:
            raw = json.load(f)
        return [Expense.from_dict(d) for d in raw]
    except json.JSONDecodeError as err:
        raise StorageError(f"{path} is not valid JSON: {err}") from err
    except (KeyError, TypeError) as err:
        raise StorageError(f"{path} has unexpected structure: {err}") from err


def save_expenses(expenses, path=DEFAULT_PATH):
    try:
        with open(path, "w") as f:
            json.dump([e.to_dict() for e in expenses], f, indent=2)
    except OSError as err:
        raise StorageError(f"cannot write {path}: {err}") from err


def add_expense(expense, path=DEFAULT_PATH):
    expenses = load_expenses(path)
    expenses.append(expense)
    save_expenses(expenses, path)

def in_month(expenses, month):
    """Yield only the expenses falling in a month like '2026-07'."""
    for e in expenses:
        if e.is_in_month(month):
            yield e


def total(expenses):
    """Sum amounts without building any intermediate list."""
    return sum(e.amount for e in expenses)


def by_category(expenses):
    """Return {category: total} for the given expenses."""
    totals = {}
    for e in expenses:
        totals[e.category] = totals.get(e.category, 0) + e.amount
    return totals