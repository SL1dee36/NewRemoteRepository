"""Unit tests for MathApp utilities."""
import unittest
from utils import add, multiply, format_result

class TestMathUtils(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-2, 3), -6)

    def test_format_result(self):
        self.assertEqual(format_result(2, 3, "+", 5), "2 + 3 = 5")

if __name__ == "__main__":
    unittest.main()
