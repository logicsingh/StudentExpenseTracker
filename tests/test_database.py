"""Unit tests for the Student Expense Tracker database layer."""
import csv
import tempfile
import unittest
from pathlib import Path

import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_expenses.db"
        database.initialize_database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_expense(self):
        expense_id = database.add_expense(
            "2026-11-13", "Food", "Lunch", "125.50", self.db_path
        )
        rows = database.list_expenses(db_path=self.db_path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], expense_id)
        self.assertEqual(rows[0]["amount"], 125.5)

    def test_search_expenses(self):
        database.add_expense("2026-11-13", "Food", "Campus lunch", 100, self.db_path)
        database.add_expense("2026-11-12", "Transport", "Bus ticket", 30, self.db_path)
        self.assertEqual(len(database.list_expenses("lunch", self.db_path)), 1)

    def test_delete_expense(self):
        expense_id = database.add_expense(
            "2026-11-13", "Food", "Lunch", 100, self.db_path
        )
        self.assertTrue(database.delete_expense(expense_id, self.db_path))
        self.assertFalse(database.delete_expense(expense_id, self.db_path))
        self.assertEqual(database.list_expenses(db_path=self.db_path), [])

    def test_validation_rejects_invalid_amount(self):
        with self.assertRaises(ValueError):
            database.add_expense(
                "2026-11-13", "Food", "Lunch", 0, self.db_path
            )

    def test_validation_rejects_invalid_category(self):
        with self.assertRaises(ValueError):
            database.add_expense(
                "2026-11-13", "Unknown", "Lunch", 100, self.db_path
            )

    def test_summary(self):
        database.add_expense("2026-11-13", "Food", "Lunch", 100, self.db_path)
        database.add_expense("2026-11-12", "Transport", "Bus", 50, self.db_path)
        summary = database.get_summary(self.db_path)
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["total"], 150.0)

    def test_export_csv(self):
        database.add_expense("2026-11-13", "Food", "Lunch", 100, self.db_path)
        output = Path(self.temp_dir.name) / "expenses.csv"
        self.assertEqual(database.export_csv(output, self.db_path), 1)
        with output.open(encoding="utf-8-sig", newline="") as file:
            rows = list(csv.reader(file))
        self.assertEqual(rows[0][0], "ID")
        self.assertEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()
