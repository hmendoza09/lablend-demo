"""items-api: manages lab equipment (list, view, add, edit)."""
import os

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import dict_row

from validation import validate_item

app = Flask(__name__)

COLUMNS = "id, name, category, available"


def get_conn():
    """Open a new database connection using settings from environment variables."""
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "lablend"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row,
    )


@app.get("/health")
def health():
    return jsonify(status="ok", service="items-api")


@app.get("/")
def list_items():
    with get_conn() as conn:
        rows = conn.execute(f"SELECT {COLUMNS} FROM items ORDER BY id").fetchall()
    return jsonify(rows)


@app.get("/<int:item_id>")
def get_item(item_id):
    with get_conn() as conn:
        row = conn.execute(
            f"SELECT {COLUMNS} FROM items WHERE id = %s", (item_id,)
        ).fetchone()
    if row is None:
        return jsonify(error="item not found"), 404
    return jsonify(row)


@app.post("/")
def create_item():
    data = request.get_json(silent=True) or {}
    errors = validate_item(data)
    if errors:
        return jsonify(errors=errors), 400
    with get_conn() as conn:
        row = conn.execute(
            f"INSERT INTO items (name, category) VALUES (%s, %s) RETURNING {COLUMNS}",
            (data["name"].strip(), data["category"].strip()),
        ).fetchone()
    return jsonify(row), 201


@app.put("/<int:item_id>")
def update_item(item_id):
    data = request.get_json(silent=True) or {}
    errors = validate_item(data)
    if errors:
        return jsonify(errors=errors), 400
    with get_conn() as conn:
        row = conn.execute(
            f"UPDATE items SET name = %s, category = %s WHERE id = %s RETURNING {COLUMNS}",
            (data["name"].strip(), data["category"].strip(), item_id),
        ).fetchone()
    if row is None:
        return jsonify(error="item not found"), 404
    return jsonify(row)
