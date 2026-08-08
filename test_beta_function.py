"""
SOEN 6011 - Deliverable 3, Problem 8
Unit tests for the Beta function B(x, y).

Uses Python's built-in unittest framework (also called PyUnit).

Run with:
    python3 -m unittest test_beta_function.py -v

These tests are based on everything I actually found while testing
this project by hand earlier: known correct values, symmetry,
the underflow case, each type of invalid input, and the precision
limitation for x,y < 1 that I found and documented as a known issue
rather than hiding it.
"""

import math
import unittest

from beta_function_scratch import (
    beta_via_integration,
    real_power,
    my_ln,
    my_exp,
    NonPositiveValueError,
    UndefinedOperationError,
    UnsupportedDomainError,
)


def true_beta(x, y):
    """Reference value using Python's own math.gamma, for comparison."""
    return math.gamma(x) * math.gamma(y) / math.gamma(x + y)


class TestKnownValues(unittest.TestCase):
    """Check the function against values I know are correct by hand."""

    def test_beta_2_3(self):
        """B(2,3) = 1/12 exactly."""
        result = beta_via_integration(2.0, 3.0)
        self.assertAlmostEqual(result, 1 / 12, places=6)

    def test_beta_1_1(self):
        """B(1,1) = 1 exactly."""
        result = beta_via_integration(1.0, 1.0)
        self.assertAlmostEqual(result, 1.0, places=3)

    def test_beta_5_5(self):
        """B(5,5) should match the Gamma-function reference value."""
        result = beta_via_integration(5.0, 5.0)
        self.assertAlmostEqual(result, true_beta(5.0, 5.0), places=6)


class TestSymmetry(unittest.TestCase):
    """B(x, y) should always equal B(y, x)."""

    def test_symmetry_2_3(self):
        """B(2,3) should equal B(3,2)."""
        self.assertAlmostEqual(
            beta_via_integration(2.0, 3.0),
            beta_via_integration(3.0, 2.0),
            places=6,
        )

    def test_symmetry_7_2(self):
        """B(7,2) should equal B(2,7)."""
        self.assertAlmostEqual(
            beta_via_integration(7.0, 2.0),
            beta_via_integration(2.0, 7.0),
            places=6,
        )


class TestUnderflowCase(unittest.TestCase):
    """Large x, y should give a tiny but correct (non-zero) result."""

    def test_beta_10_50_is_tiny_not_zero(self):
        """B(10,50) should be a real tiny positive number, not zero."""
        result = beta_via_integration(10.0, 50.0)
        self.assertGreater(result, 0.0)
        self.assertLess(result, 1e-9)

    def test_beta_10_50_matches_reference(self):
        """B(10,50) should be close to the Gamma-function reference."""
        result = beta_via_integration(10.0, 50.0)
        expected = true_beta(10.0, 50.0)
        # compare relative error since the numbers are so small that
        # assertAlmostEqual's default absolute tolerance doesn't work well
        relative_error = abs(result - expected) / expected
        self.assertLess(relative_error, 1e-4)


class TestKnownPrecisionLimitation(unittest.TestCase):
    """
    Documents the real limitation I found: for x,y < 1, the integrand
    has a singularity at the interval edges that Simpson's Rule
    under-resolves, so accuracy drops well below the 6-digit target.
    This test doesn't hide that - it confirms the limitation exists
    and stays within a known bound, so a future fix would be caught
    by this test if it accidentally got worse.
    """

    def test_beta_half_half_has_known_error(self):
        """B(0.5,0.5) should be close to pi, but only within ~4% today."""
        result = beta_via_integration(0.5, 0.5)
        expected = math.pi  # true value of B(0.5, 0.5)
        relative_error = abs(result - expected) / expected
        # currently around 4%, well above the 6-digit target - this
        # assertion documents that fact instead of pretending it's fine
        self.assertLess(relative_error, 0.05)
        self.assertGreater(relative_error, 0.01)


class TestInvalidInput(unittest.TestCase):
    """Each exception type should fire for the right kind of bad input."""

    def test_negative_x_raises(self):
        """Negative x should raise NonPositiveValueError."""
        with self.assertRaises(NonPositiveValueError):
            beta_via_integration(-1.0, 3.0)

    def test_negative_y_raises(self):
        """Negative y should raise NonPositiveValueError."""
        with self.assertRaises(NonPositiveValueError):
            beta_via_integration(2.0, -1.0)

    def test_both_negative_raises(self):
        """Both x and y negative should still raise one clear error."""
        with self.assertRaises(NonPositiveValueError):
            beta_via_integration(-1.0, -1.0)

    def test_zero_x_raises(self):
        """x = 0 is not strictly positive, should raise an error."""
        with self.assertRaises(NonPositiveValueError):
            beta_via_integration(0.0, 3.0)

    def test_error_message_names_the_right_variable(self):
        """When only x is bad, the message should name x, not y."""
        # this checks the specific-message behavior I added earlier,
        # not just that *an* error was raised
        try:
            beta_via_integration(-1.0, 3.0)
            self.fail("Expected NonPositiveValueError was not raised")
        except NonPositiveValueError as e:
            self.assertIn("x", str(e))
            self.assertNotIn("y must", str(e))

    def test_ln_of_zero_raises(self):
        """ln(0) has no real answer, should raise our custom error."""
        with self.assertRaises(UndefinedOperationError):
            my_ln(0.0)

    def test_ln_of_negative_raises(self):
        """ln of a negative number should also raise our custom error."""
        with self.assertRaises(UndefinedOperationError):
            my_ln(-5.0)

    def test_negative_base_raises(self):
        """real_power doesn't support negative bases by design."""
        with self.assertRaises(UnsupportedDomainError):
            real_power(-2.0, 3.0)


class TestSubordinateFunctions(unittest.TestCase):
    """Test my_exp, my_ln, and real_power directly, not just through
    the full Beta function - these are the from-scratch building
    blocks, so it's worth confirming each one works on its own."""

    def test_my_exp_matches_builtin(self):
        """my_exp should match Python's math.exp closely."""
        self.assertAlmostEqual(my_exp(1.0), math.exp(1.0), places=6)
        self.assertAlmostEqual(my_exp(-2.5), math.exp(-2.5), places=6)

    def test_my_ln_matches_builtin(self):
        """my_ln should match Python's math.log closely."""
        self.assertAlmostEqual(my_ln(2.0), math.log(2.0), places=6)
        self.assertAlmostEqual(my_ln(0.1), math.log(0.1), places=6)

    def test_real_power_matches_builtin(self):
        """real_power should match Python's ** operator closely."""
        self.assertAlmostEqual(real_power(2.0, 10.0), 2.0 ** 10.0, places=4)
        self.assertAlmostEqual(real_power(0.5, 2.5), 0.5 ** 2.5, places=6)


if __name__ == "__main__":
    unittest.main()