"""Math utility functions - Enterprise High Precision Edition (Merged Person 1 & Person 3)."""


def add(a: float, b: float) -> float:
    """Returns the sum of two numbers with rounding and float conversion."""
    return round(float(a + b), 4)


def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b


def format_result(a: float, b: float, op: str, res: float) -> str:
    """Formats calculation result for display."""
    return f"{a} {op} {b} = {res}"


def subtract(a: float, b: float) -> float:
    """Returns the difference of two numbers."""
    return a - b
