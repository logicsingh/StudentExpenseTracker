"""SQLite storage and validation for Student Expense Tracker."""
from __future__ import annotations

import csv
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "student_expenses.db"
CATEGORIES = ("Food", "Transport", "Education", "Shopping", "Bills", "Health", "Entertainment", "Other")


def connect(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database(db_path: str | Path = DB_PATH, seed_demo: bool = False) -> None:
    with connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        if seed_demo and count == 0:
            today = date.today()
            samples = [
                ((today.replace(day=1)).isoformat(), "Education", "Semester notes and printing", 180.00),
                (today.isoformat(), "Food", "Lunch at campus", 120.00),
                (today.isoformat(), "Transport", "Auto / local travel", 85.00),
                (today.isoformat(), "Bills", "Mobile recharge", 299.00),
                (today.isoformat(), "Shopping", "Notebook and stationery", 95.00),
            ]
            conn.executemany(
                "INSERT INTO expenses (expense_date, category, description, amount) VALUES (?, ?, ?, ?)",
                samples,
            )


def validate_expense(expense_date: str, category: str, description: str, amount: str | float) -> tuple[str, str, str, float]:
    try:
        parsed_date = datetime.strptime(expense_date.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        raise ValueError("Date must use YYYY-MM-DD format, for example 2026-10-23.")
    if parsed_date.isoformat() != expense_date.strip():
        raise ValueError("Please enter a valid date in YYYY-MM-DD format.")
    category = str(category).strip()
    if category not in CATEGORIES:
        raise ValueError("Please select a valid expense category.")
    description = str(description).strip()
    if not description:
        raise ValueError("Description cannot be empty.")
    if len(description) > 120:
        raise ValueError("Description must be 120 characters or fewer.")
    try:
        numeric_amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a valid number.")
    if numeric_amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if numeric_amount > 10_000_000:
        raise ValueError("Amount is too large. Please check the value.")
    return parsed_date.isoformat(), category, description, round(numeric_amount, 2)


def add_expense(expense_date: str, category: str, description: str, amount: str | float, db_path: str | Path = DB_PATH) -> int:
    values = validate_expense(expense_date, category, description, amount)
    with connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO expenses (expense_date, category, description, amount) VALUES (?, ?, ?, ?)", values
        )
        return int(cursor.lastrowid)


def list_expenses(search: str = "", db_path: str | Path = DB_PATH) -> list[sqlite3.Row]:
    query = "SELECT id, expense_date, category, description, amount FROM expenses"
    params: list[object] = []
    if search.strip():
        needle = f"%{search.strip()}%"
        query += " WHERE category LIKE ? OR description LIKE ? OR expense_date LIKE ?"
        params.extend((needle, needle, needle))
    query += " ORDER BY expense_date DESC, id DESC"
    with connect(db_path) as conn:
        return list(conn.execute(query, params).fetchall())


def delete_expense(expense_id: int, db_path: str | Path = DB_PATH) -> bool:
    with connect(db_path) as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (int(expense_id),))
        return cursor.rowcount > 0


def get_summary(db_path: str | Path = DB_PATH) -> dict[str, object]:
    month = date.today().strftime("%Y-%m")
    with connect(db_path) as conn:
        total = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses").fetchone()[0]
        count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
        month_total = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE substr(expense_date, 1, 7) = ?", (month,)
        ).fetchone()[0]
        categories = conn.execute(
            "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC"
        ).fetchall()
    return {"total": float(total), "count": int(count), "month_total": float(month_total),
            "categories": [(row["category"], float(row["total"])) for row in categories]}


def export_csv(destination: str | Path, db_path: str | Path = DB_PATH) -> int:
    rows = list_expenses(db_path=db_path)
    with open(destination, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(("ID", "Date", "Category", "Description", "Amount (INR)"))
        writer.writerows((row["id"], row["expense_date"], row["category"], row["description"], f'{row["amount"]:.2f}') for row in rows)
    return len(rows)
