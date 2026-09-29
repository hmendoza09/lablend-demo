"""Business rules for borrowing (pure functions, easy to unit test)."""
from datetime import date, timedelta

LOAN_DAYS = 3  # equipment must be returned within 3 days


def compute_due_date(borrow_date: date, days: int = LOAN_DAYS) -> date:
    """Due date = borrow date + loan period."""
    if days < 1:
        raise ValueError("loan period must be at least 1 day")
    return borrow_date + timedelta(days=days)


def is_overdue(due_date: date, today: date) -> bool:
    return today > due_date


def validate_borrow(data):
    """Return a list of error messages. An empty list means the request is valid."""
    errors = []
    if not str(data.get("borrower_name", "")).strip():
        errors.append("borrower_name is required")
    item_id = data.get("item_id")
    if not isinstance(item_id, int) or isinstance(item_id, bool) or item_id < 1:
        errors.append("item_id must be a positive integer")
    return errors
