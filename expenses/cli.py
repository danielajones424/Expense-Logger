import argparse
import sys

from expenses.models import Expense
from expenses.storage import (
    StorageError, add_expense, load_expenses,
    in_month, total, by_category,
)


def cmd_add(args):
    expense = Expense(args.amount, args.category, args.description or "")
    add_expense(expense)
    print(f"added: {expense}")


def cmd_list(args):
    expenses = load_expenses()
    if args.month:
        expenses = list(in_month(expenses, args.month))
    if not expenses:
        print("no expenses found")
        return
    for e in sorted(expenses):
        print(e)


def cmd_summary(args):
    expenses = load_expenses()
    if args.month:
        expenses = list(in_month(expenses, args.month))
    print(f"total: ${total(expenses):.2f}")
    for category, amount in sorted(by_category(expenses).items()):
        print(f"  {category:<12} ${amount:>8.2f}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="expenses", description="Track spending from the command line.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="record a new expense")
    p_add.add_argument("amount", type=float)
    p_add.add_argument("category")
    p_add.add_argument("description", nargs="?", default="")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="show expenses, oldest first")
    p_list.add_argument("--month", help="filter, e.g. 2026-07")
    p_list.set_defaults(func=cmd_list)

    p_sum = sub.add_parser("summary", help="totals overall and per category")
    p_sum.add_argument("--month", help="filter, e.g. 2026-07")
    p_sum.set_defaults(func=cmd_summary)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except StorageError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)