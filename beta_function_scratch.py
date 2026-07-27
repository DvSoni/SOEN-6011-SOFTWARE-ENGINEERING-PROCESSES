"""
SOEN 6011 - Deliverable 2, Problem 5
Beta function B(x, y) - FROM SCRATCH implementation

Everything below is built using only: +, -, *, /, comparisons, and
loops. No use of the ** operator and no math/library imports for the
core computation (only allowed for input/output/UI, per the
assignment's "from scratch" rule).

Chain of dependencies:
    my_exp(z)        -> e^z via Taylor series + repeated squaring
    my_ln(y)         -> ln(y) via fast-converging series + range reduction
    real_power(b, p) -> b^p = exp(p * ln(b)), for any real exponent
    f(t, x, y)       -> the Beta function's integrand
    beta_via_integration(x, y) -> Simpson's Rule using the above

Traceability to requirements (Problem 2 / updated in Problem 7):
    REQ-001, REQ-002 : accept x, y and compute B(x, y)
    REQ-003           : reject x <= 0 or y <= 0
    REQ-004           : minimum 6 significant digits of precision
    REQ-007, REQ-008  : no external libraries, no built-in exponent operator
"""


class InvalidInputError(Exception):
    """Custom exception raised when x or y is not a valid positive real number."""
    pass


# ---------------------------------------------------------------------
# Building block 1: e^z from scratch
# ---------------------------------------------------------------------
def my_exp(z):
    """
    Computes e^z using a Taylor series with range reduction.

    Idea: e^z = (e^(z / 2^m))^(2^m)
      1. Keep halving z until it's small (|z| < 1)
      2. Compute e^(small number) with a Taylor series (converges fast)
      3. Square the result m times to undo the halving
    """
    m = 0
    reduced_z = z
    while reduced_z > 1 or reduced_z < -1:
        reduced_z = reduced_z / 2
        m += 1

    term = 1.0
    total = 1.0
    for n in range(1, 30):
        term = term * reduced_z / n
        total = total + term

    for _ in range(m):
        total = total * total

    return total


# ---------------------------------------------------------------------
# Building block 2: ln(y) from scratch
# ---------------------------------------------------------------------
def my_ln(y):
    """
    Computes ln(y) for y > 0 using:
        ln(y) = 2*(u + u^3/3 + u^5/5 + ...),   u = (y-1)/(y+1)
    Range-reduces y into [0.5, 2) first (dividing/multiplying by 2),
    since the series converges quickly only near y = 1.
    """
    if y <= 0:
        raise InvalidInputError("Cannot take ln of a non-positive number.")

    def ln_series(v):
        u = (v - 1) / (v + 1)
        u_power = u
        u_squared = u * u
        total = 0.0
        for n in range(1, 60, 2):  # 1, 3, 5, 7, ...
            total += u_power / n
            u_power *= u_squared
        return 2 * total

    ln2 = ln_series(2.0)

    k = 0
    reduced_y = y
    while reduced_y >= 2.0:
        reduced_y = reduced_y / 2.0
        k += 1
    while reduced_y < 0.5:
        reduced_y = reduced_y * 2.0
        k -= 1

    return ln_series(reduced_y) + k * ln2


# ---------------------------------------------------------------------
# Building block 3: real_power(base, exponent) from scratch
# ---------------------------------------------------------------------
def real_power(base, exponent):
    """
    Computes base^exponent for base > 0 and any real exponent, using
    base^exponent = exp(exponent * ln(base)).
    """
    if base == 0:
        if exponent > 0:
            return 0.0
        raise InvalidInputError("0 raised to a non-positive power is undefined.")
    if base < 0:
        raise InvalidInputError("Negative base is not supported (not needed for this function's domain).")

    return my_exp(exponent * my_ln(base))


# ---------------------------------------------------------------------
# Beta function itself
# ---------------------------------------------------------------------
def f(t, x, y):
    """Integrand: t^(x-1) * (1-t)^(y-1), computed with real_power."""
    return real_power(t, x - 1) * real_power(1 - t, y - 1)


def beta_via_integration(x, y, n=1000):
    """
    Approximates B(x, y) using Simpson's Rule with n subintervals.
    Small offsets (a, b) avoid the singularities at t=0 and t=1.

    Raises InvalidInputError if x or y is not strictly positive.
    """
    if x <= 0 or y <= 0:
        raise InvalidInputError("Both x and y must be strictly positive.")

    a = 0.00001
    b = 0.99999
    h = (b - a) / n

    total = f(a, x, y) + f(b, x, y)

    for i in range(1, n):
        t = a + i * h
        if i % 2 == 1:
            total += 4 * f(t, x, y)
        else:
            total += 2 * f(t, x, y)

    return (h / 3) * total


if __name__ == "__main__":
    # quick self-checks against known exact values
    # B(2,3) = 1/12 = 0.08333333...
    print("B(2, 3)  =", beta_via_integration(2.0, 3.0), " expected ~0.0833333")
    # B(10,50) is a known tiny value ~1.5916380e-12
    print("B(10,50) =", beta_via_integration(10.0, 50.0), " expected ~1.5916380e-12")

    try:
        beta_via_integration(-1.0, 3.0)
    except InvalidInputError as e:
        print("Correctly caught error:", e)
