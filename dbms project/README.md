# Pocket Ledger — MySQL Expense Tracker

A small Flask application that records expenses in a real MySQL database. It demonstrates all four CRUD operations: **Create** (INSERT), **Read** (SELECT), **Update** (UPDATE), and **Delete** (DELETE). The database is created and inspected with MySQL Workbench; Workbench is the client UI, while the running MySQL Server stores the data.

## Project structure

```text
app.py                      Flask application and parameterized SQL
database/expense_tracker.sql Database and table setup for MySQL Workbench
templates/                  HTML interface
static/style.css            Responsive styling
requirements.txt            Python dependencies
REPORT.md                   Ready-to-submit project report
```

## 1. Create the database in MySQL Workbench

1. Start your local MySQL Server and open its connection in MySQL Workbench.
2. Open `database/expense_tracker.sql` in Workbench.
3. Execute the script (lightning bolt). It creates `expense_tracker_db`, the `expenses` table, and three sample records.
4. Refresh **Schemas**, expand `expense_tracker_db` → **Tables**, then inspect `expenses`. Run the final `SELECT` in the script to verify the rows.

The table stores `expense_id`, `title`, `category`, `amount`, `expense_date`, and `created_at`. The auto-incrementing primary key identifies each row; amount is a positive `DECIMAL(10,2)`.

## 2. Configure and start the application

Use Python 3.10 or newer. In a terminal opened in this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set the same connection details as the MySQL Workbench connection. On macOS/Linux:

```bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD='your MySQL server password'
export DB_NAME=expense_tracker_db
python app.py
```

On Windows PowerShell, use `$env:DB_HOST="127.0.0.1"` (and likewise for the other `DB_*` settings) before `python app.py`. Open <http://127.0.0.1:5000>. Use the MySQL **server account password** configured for the Workbench connection, not a separate Workbench password. Do not commit real credentials.

## 3. Demonstrate CRUD

- **INSERT:** Add an expense in the form. It appears in the list. In Workbench, run `SELECT * FROM expense_tracker_db.expenses;` to confirm the new row is persisted.
- **SELECT:** The page loads stored rows from MySQL. Use the category filter to query a subset.
- **UPDATE:** Choose **Edit**, change a field, then save. Confirm the changed row in Workbench.
- **DELETE:** Choose **Delete** and confirm. Confirm that row is gone in Workbench.
- **Invalid input:** Try a blank field or amount of zero; the form rejects it. Database errors include a troubleshooting page.

All SQL values use connector parameters (`%s`); inputs are not joined into SQL strings. The connection values come from environment variables so passwords are not in source code.

## Troubleshooting

- **Can't connect / access denied:** confirm MySQL Server is running, the Workbench connection works, and `DB_HOST`, `DB_PORT`, `DB_USER`, and `DB_PASSWORD` match that server account.
- **Unknown database:** execute the supplied SQL file in Workbench first and check that `DB_NAME=expense_tracker_db`.
- **Module not found:** activate `.venv` and run `python -m pip install -r requirements.txt` again.
