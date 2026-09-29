from validation import validate_item


def test_valid_item_has_no_errors():
    assert validate_item({"name": "Oscilloscope", "category": "Measuring tool"}) == []


def test_missing_name_is_rejected():
    assert "name is required" in validate_item({"category": "Networking"})


def test_blank_category_is_rejected():
    assert "category is required" in validate_item({"name": "Router", "category": "   "})


def test_name_too_long_is_rejected():
    errors = validate_item({"name": "x" * 101, "category": "Networking"})
    assert "name must be at most 100 characters" in errors
