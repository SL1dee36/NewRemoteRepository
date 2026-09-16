"""Main entry point for MathApp application with Person 2 logging."""
from utils import add, multiply, subtract, format_result
from logger import log_action

def main():
    log_action("Starting MathApp v1.2", level="INFO")
    print("=== MathApp Application v1.2 (Enhanced by Person 2) ===")
    a, b = 10, 5
    print(f"Addition: {format_result(a, b, '+', add(a, b))}")
    print(f"Subtraction: {format_result(a, b, '-', subtract(a, b))}")
    print(f"Multiplication: {format_result(a, b, '*', multiply(a, b))}")
    log_action("MathApp finished successfully", level="SUCCESS")

if __name__ == "__main__":
    main()
