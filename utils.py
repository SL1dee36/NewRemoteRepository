"""Math utility functions."""

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b

def format_result(a: float, b: float, op: str, res: float) -> str:
    """Formats calculation result for display."""
    return f"{a} {op} {b} = {res}"
