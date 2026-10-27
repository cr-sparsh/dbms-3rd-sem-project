-- Run this script in MySQL Workbench against your local MySQL Server.
CREATE DATABASE IF NOT EXISTS expense_tracker_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE expense_tracker_db;

CREATE TABLE IF NOT EXISTS expenses (
  expense_id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(100) NOT NULL,
  category VARCHAR(50) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  expense_date DATE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (expense_id),
  CONSTRAINT chk_expenses_amount_positive CHECK (amount > 0)
);

-- Sample rows make the first dashboard view useful. Remove this INSERT if you
-- want to demonstrate an initially empty table.
INSERT INTO expenses (title, category, amount, expense_date) VALUES
  ('Groceries', 'Food', 42.75, '2026-10-20'),
  ('Bus pass', 'Transport', 18.00, '2026-10-21'),
  ('Notebook', 'Study', 6.50, '2026-10-22');

-- Verify the schema and sample data in Workbench:
SELECT * FROM expenses ORDER BY expense_date DESC, expense_id DESC;
