<div align="center">

# 💸 Expense Logger

**A clean, layered command-line tool for tracking personal spending.**

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#installation)
[![Status](https://img.shields.io/badge/status-active-success.svg)](#roadmap)

</div>

---

Expenses are logged with an amount, category, description, and date, then queried through simple subcommands for listing and summarizing spend by month or category — no dependencies, no config, just Python's standard library.

```console
$ python -m expenses add 12.50 food "burrito"
added: 2026-07-03  food         $   12.50  burrito

$ python -m expenses summary --month 2026-07
total: $16.25
  coffee       $    3.75
  food         $   12.50
```

## Table of contents

- [Why this project](#why-this-project)
- [Project structure](#project-structure)
- [Design decisions worth noting](#design-decisions-worth-noting)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)

## Why this project

This repo is intentionally small, but it's built the way a larger production codebase would be: each module has one job, state is never shared implicitly, and the CLI layer knows nothing about how data is stored or how expenses are represented internally. That separation is what makes it easy to test, extend, or swap pieces out (e.g. replacing JSON storage with a database) without touching the rest of the code.

## Project structure

```text
Expense-Logger/
├── expenses/                 # The installable package — all application logic lives here
│   ├── __init__.py           # Marks this directory as a package
│   ├── __main__.py           # Entry point for `python -m expenses`; delegates to cli.main()
│   ├── cli.py                # Command-line interface: argument parsing and subcommands
│   ├── models.py             # The Expense data model
│   └── storage.py            # Persistence layer: reading/writing expenses to disk
├── expenses.json              # Runtime data file — created and updated by the app, not hand-edited
└── README.md
```

| File | Responsibility |
|---|---|
| `models.py` | The domain model. Defines the `Expense` class: a single spending record with an amount, category, description, and date. Implements comparison (`__lt__`) so expenses sort chronologically, equality (`__eq__`) for testing and deduplication, and `to_dict()` / `from_dict()` for converting to and from the JSON representation on disk. This is the only place that knows what an "expense" actually is. |
| `storage.py` | Persistence. Reads and writes `expenses.json` through a small set of pure functions (`load_expenses`, `save_expenses`, `add_expense`) plus query helpers (`in_month`, `total`, `by_category`) that operate on lists of `Expense` objects without caring where they came from. File and parsing failures are caught and re-raised as one `StorageError`, so callers never need to guess between `OSError`, `json.JSONDecodeError`, or `KeyError`. |
| `cli.py` | The interface. Builds the `argparse` command structure (`add`, `list`, `summary`) and wires each subcommand to a handler. The only file that talks to `stdin`/`stdout`/`stderr` — it formats output and turns a `StorageError` into a clean message and a non-zero exit code instead of a stack trace. |
| `__main__.py` | Calls `cli.main()`, which is what makes `python -m expenses ...` work as an entry point. |

## Design decisions worth noting

- **Layered architecture.** Model, storage, and CLI are fully decoupled — `models.py` has no knowledge of files, and `storage.py` has no knowledge of `argparse`. Any layer can be tested or replaced independently.
- **Single custom exception at the boundary.** All storage failures collapse into `StorageError`, giving the CLI one predictable thing to catch instead of a matrix of built-in exceptions.
- **Generators for querying.** `in_month()` yields matching expenses lazily rather than building an intermediate list, keeping the query path memory-efficient as the dataset grows.
- **Dunder methods over ad hoc helpers.** `Expense` implements `__lt__`, `__eq__`, `__repr__`, and `__str__` so it behaves naturally with Python's built-in `sorted()` and printing, instead of requiring a bespoke comparator function elsewhere.

## Installation

Requires Python 3.9+. No third-party dependencies.

```bash
git clone git@github.com:danielajones424/Expense-Logger.git
cd Expense-Logger
```

## Usage

```bash
# Record an expense: amount, category, and an optional description
python -m expenses add 12.50 food "burrito"

# List all expenses, oldest first
python -m expenses list

# List expenses for a specific month (YYYY-MM)
python -m expenses list --month 2026-07

# Show total spend and a per-category breakdown
python -m expenses summary

# Same, scoped to one month
python -m expenses summary --month 2026-07
```

Data is stored in `expenses.json` in the current directory, created automatically on first use.

## Roadmap

- [ ] Unit tests for `models.py` and `storage.py` (both are pure and easy to test in isolation)
- [ ] Packaging via `pyproject.toml` so the CLI can be installed with `pip install -e .`
- [ ] Category validation and configurable budgets with over-budget warnings
- [ ] CSV/Excel export for spend history
- [ ] Support for multiple named ledgers instead of a single `expenses.json`
