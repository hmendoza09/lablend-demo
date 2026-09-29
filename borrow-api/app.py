"""borrow-api: records borrowing and returning of lab equipment."""
import os
from datetime import date

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import dict_row

from logic import compute_due_date, validate_borrow

app = Flask(__name__)


def get_conn():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "lablend"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row,
    )


@app.get("/health")
def health():
    return jsonify(status="ok", service="borrow-api")


@app.get("/")
def list_borrows():
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT b.id, b.item_id, i.name AS item_name, b.borrower_name,
                   b.borrow_date::text AS borrow_date, b.due_date::text AS due_date,
                   b.status
            FROM borrows b JOIN items i ON i.id = b.item_id
            ORDER BY b.id DESC
            """
        ).fetchall()
    return jsonify(rows)


@app.post("/")
def create_borrow():
    data = request.get_json(silent=True) or {}
    errors = validate_borrow(data)
    if errors:
        return jsonify(errors=errors), 400

    today = date.today()
    due = compute_due_date(today)

    with get_conn() as conn:
        item = conn.execute(
            "SELECT id, available FROM items WHERE id = %s FOR UPDATE", (data["item_id"],)
        ).fetchone()
        if item is None:
            return jsonify(error="item not found"), 404
        if not item["available"]:
            return jsonify(error="item is already borrowed"), 409

        row = conn.execute(
            """
            INSERT INTO borrows (item_id, borrower_name, borrow_date, due_date)
            VALUES (%s, %s, %s, %s)
            RETURNING id, item_id, borrower_name, borrow_date::text AS borrow_date,
                      due_date::text AS due_date, status
            """,
            (data["item_id"], data["borrower_name"].strip(), today, due),
        ).fetchone()
        conn.execute("UPDATE items SET available = FALSE WHERE id = %s", (data["item_id"],))
    return jsonify(row), 201


@app.patch("/<int:borrow_id>/return")
def return_item(borrow_id):
    with get_conn() as conn:
        row = conn.execute(
            """
            UPDATE borrows SET status = 'returned', returned_at = NOW()
            WHERE id = %s AND status = 'borrowed'
            RETURNING id, item_id, status
            """,
            (borrow_id,),
        ).fetchone()
        if row is None:
            return jsonify(error="borrow record not found or already returned"), 404
        conn.execute("UPDATE items SET available = TRUE WHERE id = %s", (row["item_id"],))
    return jsonify(row)
