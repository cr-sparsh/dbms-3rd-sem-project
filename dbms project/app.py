"""Simple MySQL-backed expense tracker for the DBMS mini project."""
import os
from datetime import date

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-for-local-use")


def get_connection():
    """Open a connection using credentials configured in environment variables."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "123"),
        database=os.getenv("DB_NAME", "expense_tracker_db"),
    )


def money_amount(raw):
    try:
        amount = float(raw)
        if amount <= 0 or not amount < float("inf"):
            raise ValueError
        return round(amount, 2)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number greater than zero.")


@app.route("/")
def index():
    category = request.args.get("category", "").strip()
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if category:
            cursor.execute(
                "SELECT * FROM expenses WHERE category = %s ORDER BY expense_date DESC, expense_id DESC",
                (category,),
            )
        else:
            cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC, expense_id DESC")
        expenses = cursor.fetchall()
        cursor.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses")
        total = cursor.fetchone()["total"]
        cursor.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
        categories = [row["category"] for row in cursor.fetchall()]
        return render_template("index.html", expenses=expenses, total=total,
                               categories=categories, selected_category=category,
                               today=date.today().isoformat())
    except Error as exc:
        return render_template("error.html", message=str(exc)), 500
    finally:
        if conn and conn.is_connected():
            conn.close()


@app.route("/add", methods=["POST"])
def add_expense():
    try:
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        spent_on = request.form.get("expense_date", "").strip()
        amount = money_amount(request.form.get("amount"))
        if not title or len(title) > 100:
            raise ValueError("Description is required and must be 100 characters or fewer.")
        if not category or len(category) > 50:
            raise ValueError("Category is required and must be 50 characters or fewer.")
        date.fromisoformat(spent_on)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (title, category, amount, expense_date) VALUES (%s, %s, %s, %s)",
            (title, category, amount, spent_on),
        )
        conn.commit()
        flash("Expense added to MySQL.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    except Error as exc:
        flash(f"Could not save expense: {exc}", "error")
    finally:
        if "conn" in locals() and conn.is_connected():
            conn.close()
    return redirect(url_for("index"))


@app.route("/update/<int:expense_id>", methods=["POST"])
def update_expense(expense_id):
    try:
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        spent_on = request.form.get("expense_date", "").strip()
        amount = money_amount(request.form.get("amount"))
        if not title or len(title) > 100 or not category or len(category) > 50:
            raise ValueError("Description and category are required and must fit the allowed length.")
        date.fromisoformat(spent_on)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE expenses SET title=%s, category=%s, amount=%s, expense_date=%s WHERE expense_id=%s",
            (title, category, amount, spent_on, expense_id),
        )
        conn.commit()
        flash("Expense updated in MySQL." if cursor.rowcount else "Expense was not found.",
              "success" if cursor.rowcount else "error")
    except ValueError as exc:
        flash(str(exc), "error")
    except Error as exc:
        flash(f"Could not update expense: {exc}", "error")
    finally:
        if "conn" in locals() and conn.is_connected():
            conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))
        conn.commit()
        flash("Expense deleted from MySQL." if cursor.rowcount else "Expense was not found.",
              "success" if cursor.rowcount else "error")
    except Error as exc:
        flash(f"Could not delete expense: {exc}", "error")
    finally:
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
