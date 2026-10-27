# Pocket Ledger: MySQL Expense Tracker

## Project overview

Pocket Ledger is a simple web application for recording and managing personal expenses. It provides a browser-based interface built with Flask and stores each record in a MySQL table. MySQL Workbench is used to create the schema, execute verification queries, and inspect the records. The project demonstrates direct application-to-MySQL connectivity and the required database operations.

## Data and database design

The database is named `expense_tracker_db`. Its `expenses` table contains:

| Column | Type | Purpose |
|---|---|---|
| `expense_id` | `INT AUTO_INCREMENT` | Primary key for each expense |
| `title` | `VARCHAR(100)` | Short description |
| `category` | `VARCHAR(50)` | Expense category |
| `amount` | `DECIMAL(10,2)` | Positive expense amount in rupees |
| `expense_date` | `DATE` | Date the money was spent |
| `created_at` | `TIMESTAMP` | Record creation time |

`expense_id` is the primary key. The amount constraint prevents zero or negative expenses. The setup script is `database/expense_tracker.sql`; it creates the database and table and inserts three sample expenses.

## Application functions

- Add an expense with a description, category, amount, and date (SQL `INSERT`).
- Display saved expenses and the overall total (SQL `SELECT`).
- Filter the displayed records by category (parameterized `SELECT`).
- Edit an existing expense (SQL `UPDATE`).
- Delete an expense after confirmation (SQL `DELETE`).
- Reject missing fields, overlong text, invalid dates, and non-positive amounts with a visible message.

The application uses Python, Flask, and `mysql-connector-python`. MySQL connection settings are read from environment variables so credentials remain outside the source files. Values in SQL statements are parameterized through the connector.

## Setup and demonstration

1. Start MySQL Server and connect to it in MySQL Workbench.
2. Open and execute `database/expense_tracker.sql`. Verify the sample records with `SELECT * FROM expenses;`.
3. Install Python dependencies with `python -m pip install -r requirements.txt`.
4. Set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` to match the Workbench server connection; then run `python app.py`.
5. Open `http://127.0.0.1:5000`. Add a record and verify it in Workbench. Edit the record, verify the changed value, delete it, then verify it is absent.

## Screenshot checklist for submission

Capture these screenshots after running the application with your local MySQL Server:

1. The Pocket Ledger page showing the form and records.
2. MySQL Workbench showing the `expense_tracker_db.expenses` schema and sample or newly added rows.
3. A record after an application edit, with the matching row in Workbench.
4. A successful deletion shown by the refreshed application list or a Workbench query.

Screenshots are intentionally left to capture from the student's own running MySQL Workbench session, so they show actual local database persistence.
