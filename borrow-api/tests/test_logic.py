from datetime import date

import pytest

from logic import compute_due_date, is_overdue, validate_borrow


def test_due_date_is_three_days_after_borrowing():
    assert compute_due_date(date(2026, 10, 1)) == date(2026, 10, 4)


def test_due_date_crosses_month_end():
    assert compute_due_date(date(2026, 10, 30)) == date(2026, 11, 2)


def test_zero_day_loan_is_not_allowed():
    with pytest.raises(ValueError):
        compute_due_date(date(2026, 10, 1), days=0)


def test_is_overdue():
    assert is_overdue(date(2026, 10, 4), today=date(2026, 10, 5)) is True
    assert is_overdue(date(2026, 10, 4), today=date(2026, 10, 4)) is False


def test_validate_borrow():
    assert validate_borrow({"borrower_name": "Juan", "item_id": 1}) == []
    assert "borrower_name is required" in validate_borrow({"item_id": 1})
    assert "item_id must be a positive integer" in validate_borrow({"borrower_name": "Juan", "item_id": "1"})
