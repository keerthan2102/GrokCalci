"""Tests for GrokCalci calculator."""

import unittest

from calculator import calculate, format_result


class TestCalculate(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate("2 + 3"), 5)

    def test_subtraction(self):
        self.assertEqual(calculate("10 - 4"), 6)

    def test_multiplication(self):
        self.assertEqual(calculate("6 * 7"), 42)

    def test_division(self):
        self.assertEqual(calculate("15 / 3"), 5)

    def test_precedence(self):
        self.assertEqual(calculate("2 + 3 * 4"), 14)

    def test_parentheses(self):
        self.assertEqual(calculate("(2 + 3) * 4"), 20)

    def test_power(self):
        self.assertEqual(calculate("2 ** 8"), 256)
        self.assertEqual(calculate("2^8"), 256)

    def test_modulo(self):
        self.assertEqual(calculate("10 % 3"), 1)

    def test_floor_division(self):
        self.assertEqual(calculate("7 // 2"), 3)

    def test_unary_minus(self):
        self.assertEqual(calculate("-5 + 3"), -2)
        self.assertEqual(calculate("-(2 + 3)"), -5)

    def test_decimals(self):
        self.assertAlmostEqual(calculate("0.5 * 4"), 2.0)

    def test_unicode_ops(self):
        self.assertEqual(calculate("6 × 7"), 42)
        self.assertEqual(calculate("20 ÷ 4"), 5)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as ctx:
            calculate("1 / 0")
        self.assertIn("zero", str(ctx.exception).lower())

    def test_empty(self):
        with self.assertRaises(ValueError):
            calculate("")
        with self.assertRaises(ValueError):
            calculate("   ")

    def test_invalid(self):
        with self.assertRaises(ValueError):
            calculate("2 +")
        with self.assertRaises(ValueError):
            calculate("import os")
        with self.assertRaises(ValueError):
            calculate("__import__('os')")

    def test_format_result(self):
        self.assertEqual(format_result(5), "5")
        self.assertEqual(format_result(2.5), "2.5")


class TestMain(unittest.TestCase):
    def test_cli_expression(self):
        from calculator import main
        from io import StringIO
        import sys

        buf = StringIO()
        old = sys.stdout
        try:
            sys.stdout = buf
            code = main(["2 + 2"])
        finally:
            sys.stdout = old
        self.assertEqual(code, 0)
        self.assertEqual(buf.getvalue().strip(), "4")


if __name__ == "__main__":
    unittest.main()
