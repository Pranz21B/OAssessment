# How To Run This Repository

**Prerequisites:** Python 3.8+ (Tasks 1 & 3), SQLite (Task 2) — [download here](https://www.sqlite.org/download.html)

First, clone or download this repository.

## Task 1: Validation Calculations
Double-click 'validation_calculations.py'
A window will open showing the results.
Alternatively you can run the script from cmd.

## Task 2: SQL Investigation
Load the database distribution_qa (1).db into sqlite.
From the task2 folder, run each sql query against the database and view the results

## Task 3: Automated Regression Tests
Windows: double-click run_tests.bat in the task3 folder.
Or manually:
    pip install pytest
    cd task3/tests
    python -m pytest -v