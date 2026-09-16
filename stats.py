"""Statistical calculation helpers."""

def average(values: list) -> float:
    """Returns the arithmetic mean of a list of numbers."""
    if not values:
        return 0.0
    return sum(values) / len(values)
