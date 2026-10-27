# Student Expense Tracker

A beginner-friendly MCA Semester 1 Python mini project. It records personal/student expenses, stores them in SQLite, searches records, shows spending summaries, and exports data to CSV.

## Features
- Desktop GUI built with Python's standard `tkinter` library
- SQLite database created automatically on first run
- Starts with an empty database so only your own entries appear
- Add, search, view and delete expense records
- All-time spending, current-month spending and record count
- Export all records to a CSV file
- Input validation and error messages
- Automated unit tests for the database/business logic

## Requirements
- Python 3.10 or newer recommended
- No pip packages or internet connection required
- On Windows, install Python from python.org and enable **Add Python to PATH**. Tkinter is normally included with the Windows installer.

## Run on Windows
1. Extract the ZIP folder.
2. Open the extracted `StudentExpenseTracker` folder.
3. Double-click `run_windows.bat`.
4. The app opens. The database file `student_expenses.db` is created in the same folder.

Alternative: open Command Prompt in this folder and run `python app.py`.

## Run on macOS/Linux
From this folder, run `python3 app.py`. If your Python installation does not include Tkinter, install the operating system's Tkinter package.

## Run tests
Open a terminal in this folder and run:

```bash
python -m unittest discover -s tests -v
```

## Data and privacy
Records are saved locally in `student_expenses.db`; they are not sent anywhere. The application starts with an empty database. Add your own records before the demonstration. To reset the app completely, close it and delete `student_expenses.db`; the next launch creates a fresh, empty database.

## Project files
- `app.py` — Tkinter user interface
- `database.py` — SQLite operations, validation, summary calculations and CSV export
- `tests/test_database.py` — automated tests
- `PROJECT_REPORT.md` — project report draft
- `FLOWCHART.mmd` — Mermaid flowchart source
- `run_windows.bat` — Windows launcher

## Limitations
This is a local, single-user educational project, not a financial product. It does not connect to bank accounts, make payments, or provide financial advice.
