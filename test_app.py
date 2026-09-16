"""Unit tests for MathApp utilities."""
import unittest
from utils import add, multiply, subtract, format_result

class TestMathUtils(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 2), 3)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-2, 3), -6)

    def test_format_result(self):
        self.assertEqual(format_result(2, 3, "+", 5), "2 + 3 = 5")

if __name__ == "__main__":
    unittest.main()

    def test_average(self):
        from stats import average
        self.assertEqual(average([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(average([]), 0.0)
