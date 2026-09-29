"""Pure functions (no database) so they are easy to unit test."""


def validate_item(data):
    """Return a list of error messages. An empty list means the item is valid."""
    errors = []
    name = str(data.get("name", "")).strip()
    category = str(data.get("category", "")).strip()

    if not name:
        errors.append("name is required")
    elif len(name) > 100:
        errors.append("name must be at most 100 characters")

    if not category:
        errors.append("category is required")
    elif len(category) > 50:
        errors.append("category must be at most 50 characters")

    return errors
