"""Main entry point for MathApp application."""
from utils import add, multiply, format_result

def main():
    print("=== MathApp Application v1.0 ===")
    a, b = 10, 5
    print(f"Addition: {format_result(a, b, '+', add(a, b))}")
    print(f"Multiplication: {format_result(a, b, '*', multiply(a, b))}")

if __name__ == "__main__":
    main()
