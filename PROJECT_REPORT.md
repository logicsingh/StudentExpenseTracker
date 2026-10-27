# Student Expense Tracker — Mini Project Report

## 1. Title
**Student Expense Tracker Using Python and SQLite**

## 2. Abstract
The Student Expense Tracker is a desktop application developed using Python. It helps a student record daily expenses, classify them into categories, review spending totals and export records for later use. The application uses Tkinter for its graphical user interface and SQLite for persistent storage. It validates user input, supports searching and deleting records, and provides an export-to-CSV facility. The system is designed to be lightweight and runs locally without paid services or third-party Python packages.

## 3. Problem Statement
Students often make small daily purchases that are difficult to track from memory. Without organized records, it can be difficult to understand total spending or identify common expense categories. This project provides a simple digital record of expenses and calculates useful summaries automatically.

## 4. Objectives
- Develop a user-friendly Python desktop application.
- Store expense records persistently using SQLite.
- Demonstrate Python functions, modules, exception handling and database operations.
- Validate input to prevent invalid records.
- Display spending summaries and support searching.
- Export records to a CSV file for use in spreadsheet software.

## 5. Scope
The project is intended for one local user and educational demonstration. It supports expense entry, listing, search, deletion, summary calculations and CSV export. It does not include bank integration, cloud synchronization, multi-user authentication or payment processing.

## 6. Tools and Technologies
- **Python:** application logic and input validation.
- **Tkinter/ttk:** graphical user interface.
- **SQLite (`sqlite3`):** local relational database.
- **CSV module:** export of stored expense records.
- **unittest:** automated tests for core database operations.

All these modules are included in standard Python distributions, although Tkinter availability can depend on the operating-system package.

## 7. System Requirements
**Hardware:** Any modern computer capable of running Python; 4 GB RAM recommended for general comfort.

**Software:** Python 3.10 or newer recommended. No internet connection is required after Python is installed.

## 8. Functional Requirements
1. Add an expense with date, category, description and amount.
2. Reject invalid dates, blank descriptions, invalid categories and non-positive amounts.
3. View saved expense records in descending date order.
4. Search by date, category or description.
5. Delete a selected record after confirmation.
6. Display all-time and current-month totals and record count.
7. Export saved records to a CSV file.

## 9. Database Design
Table: `expenses`

| Field | Type | Purpose |
|---|---|---|
| id | INTEGER PRIMARY KEY | Unique record identifier |
| expense_date | TEXT | Date in YYYY-MM-DD format |
| category | TEXT | Expense category |
| description | TEXT | Short explanation of the expense |
| amount | REAL | Positive expense amount |
| created_at | TEXT | Record creation timestamp |

## 10. Module Description
- **User interface (`app.py`):** collects input, displays the table and summaries, and shows confirmation/error dialogs.
- **Data layer (`database.py`):** initializes the database, validates entries, adds/searches/deletes records, calculates summaries and exports CSV.
- **Tests (`tests/test_database.py`):** checks adding, validation, searching, deletion and summary calculations using a temporary database.

## 11. Algorithm
1. Start the application.
2. Create the database/table if it does not exist.
3. Create the database tables if they do not already exist. The application starts with no pre-filled expense records.
4. Display the dashboard and saved records.
5. When the user adds an expense, validate the fields.
6. If input is invalid, show an error; otherwise save the record.
7. Refresh totals and the record table.
8. Allow searching, deletion or CSV export as requested.
9. Close the application when the user exits.

## 12. Testing
The supplied automated tests cover:
- Inserting and listing a record.
- Rejecting zero or negative amounts.
- Rejecting unknown categories.
- Searching records by text.
- Deleting a record.
- Calculating totals and record counts.

Run tests with `python -m unittest discover -s tests -v`. Record the actual test output and add genuine screenshots from the running application before final submission.

## 13. Advantages
- Easy to install and operate.
- No paid API or internet dependency.
- Local database persists between launches.
- Clear separation between interface and data operations.
- CSV export supports further analysis.

## 14. Limitations and Future Enhancements
The current version is a single-user desktop app and does not sync across devices. Future work could add monthly budgets, category charts, password protection, recurring expense templates or optional cloud backup. These features are intentionally excluded from the basic release to keep it reliable and easy to explain.

## 15. Conclusion
The Student Expense Tracker demonstrates how Python can be used to build a practical desktop application. It combines GUI programming, input validation, SQLite database operations, summary calculations, file export and unit testing in a compact project suitable for an introductory postgraduate programming course.

## 16. Viva Preparation
**Q1. Why did you choose Python?**  Python has readable syntax and standard libraries that reduce setup requirements.

**Q2. What is SQLite?**  SQLite is a lightweight relational database engine that stores data in a local file.

**Q3. Why use parameterized SQL queries?**  They safely pass values separately from SQL commands and reduce SQL injection risk.

**Q4. What is exception handling?**  It allows the program to respond to runtime problems without abruptly failing during expected error cases.

**Q5. Why use functions in `database.py`?**  Functions separate responsibilities, reduce repeated code and make the logic easier to test.

**Q6. What is CSV?**  Comma-separated values is a simple text format that can be opened by spreadsheet programs.

**Q7. How is the monthly total calculated?**  The database query filters expense dates by the current year-month and sums the matching amounts.

**Q8. How do you test the application?**  Automated unit tests run core operations against a temporary database so real user records are not changed.
