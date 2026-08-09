"""
Beta function B(x, y) - built from scratch

For this part of the project we are not allowed to use the ** operator
or any math library for the actual calculation. So everything here is
done using just +, -, *, /, loops and if-statements. The only thing
python's own math stuff would normally give us for free (like x**y or
math.exp) had to be rebuilt manually below.

Basic idea / order I built things in:
    1. my_exp(z)        -> my own version of e^z
    2. my_ln(y)          -> my own version of ln(y)
    3. real_power(b, p)  -> b^p, using exp and ln together (b^p = e^(p*ln(b)))
    4. f(t, x, y)        -> the actual formula we're integrating
    5. beta_via_integration -> runs Simpson's Rule using all of the above

Which requirement each part is for (from Problem 2):
    REQ-001, REQ-002 : take in x and y, give back B(x,y)
    REQ-003          : x and y both have to be positive, or reject it
    REQ-004          : answer needs to be accurate to 6 sig figs
    REQ-007, REQ-008 : no external libraries / no built-in ** operator
    REQ-009          : error messages should actually be helpful,
                        so I made a few different exception types
                        instead of just one generic error

My custom exceptions (basically just different "types" of error so the
message can be more specific about what actually went wrong):

    BetaFunctionError            <- the "parent" one, catches all 3 below
        NonPositiveValueError    <- x or y was 0 or negative
        UndefinedOperationError  <- something like ln(0) which has no answer
        UnsupportedDomainError   <- negative base into real_power (don't need
                                    this for the Beta function itself, but
                                    added it so real_power() doesn't just
                                    silently give a wrong number)
"""

__version__ = "1.2.1"
class BetaFunctionError(Exception):
    """Parent class for all my custom errors.

    Catching this catches everything below too.
    """


class NonPositiveValueError(BetaFunctionError):
    """x or y was <= 0. This is what REQ-003 is about."""


class UndefinedOperationError(BetaFunctionError):
    """For math operations that don't have an answer.

    For example, ln(0) or ln of a negative number.
    """


class UnsupportedDomainError(BetaFunctionError):
    """For inputs my real_power function isn't built to handle.

    For example, a negative base.
    """


# ---------------------------------------------------------------------
# my_exp: my own version of e^z
# ---------------------------------------------------------------------
def my_exp(z):
    """
    Computes e^z using a Taylor series.

    Problem: if z is a big number, the Taylor series needs a LOT of terms
    to be accurate, and it starts giving wrong answers.

    Fix (this is called "range reduction"): keep cutting z in half until
    it's small (between -1 and 1). The Taylor series works great on small
    numbers. Then just square the result back up the same number of times
    we halved it, since e^z = (e^(z/2))^2, and that still equals e^z.
    """
    times_halved = 0
    small_z = z
    while small_z > 1 or small_z < -1:
        small_z = small_z / 2
        times_halved += 1

    # Taylor series: e^x = 1 + x + x^2/2! + x^3/3! + ...
    # building each term from the last one instead of recalculating
    # factorials every time, it's faster this way
    term = 1.0
    answer = 1.0
    for n in range(1, 30):
        term = term * small_z / n
        answer = answer + term

    # undo the halving from before
    for _ in range(times_halved):
        answer = answer * answer

    return answer


# ---------------------------------------------------------------------
# my_ln: my own version of ln(y)
# ---------------------------------------------------------------------
def my_ln(y):
    """
    Computes ln(y) for y > 0.

    Using this formula: ln(y) = 2*(u + u^3/3 + u^5/5 + ...)
    where u = (y-1)/(y+1)
    This only converges quickly when y is close to 1, so same idea as
    my_exp -- first shrink y down toward 1 by dividing/multiplying by 2
    a bunch of times, keep track of how many times, then add that back
    at the end using ln(2).
    """
    if y <= 0:
        raise UndefinedOperationError(
            "Cannot take ln of a non-positive number."
        )

    def ln_series(v):
        u = (v - 1) / (v + 1)
        u_power = u
        u_squared = u * u
        total = 0.0
        for n in range(1, 60, 2):  # odd numbers: 1, 3, 5, 7...
            total += u_power / n
            u_power *= u_squared
        return 2 * total

    ln2 = ln_series(2.0)  # need this constant for the range reduction below

    times_scaled = 0
    scaled_y = y
    while scaled_y >= 2.0:
        scaled_y = scaled_y / 2.0
        times_scaled += 1
    while scaled_y < 0.5:
        scaled_y = scaled_y * 2.0
        times_scaled -= 1

    return ln_series(scaled_y) + times_scaled * ln2


# ---------------------------------------------------------------------
# real_power: does base^exponent for any real exponent (not just whole numbers)
# ---------------------------------------------------------------------
def real_power(base, exponent):
    """
    Since x and y in our Beta function aren't always whole numbers, we
    can't just multiply base by itself a bunch of times. Instead we use
    the identity: base^exponent = e^(exponent * ln(base))
    which works for any real exponent.
    """
    if base == 0:
        if exponent > 0:
            return 0.0
        raise UndefinedOperationError(
            "0 raised to a non-positive power is undefined."
        )
    if base < 0:
        raise UnsupportedDomainError(
            "Negative base is not supported here "
            "(not needed for the Beta function anyway)."
        )

    return my_exp(exponent * my_ln(base))


# ---------------------------------------------------------------------
# The Beta function itself
# ---------------------------------------------------------------------
def f(t, x, y):
    """This is just the formula inside the integral: t^(x-1) * (1-t)^(y-1)."""
    return real_power(t, x - 1) * real_power(1 - t, y - 1)


def beta_via_integration(x, y, n=1000):
    """
    Estimates B(x, y) using Simpson's Rule (adds up thin slices under
    the curve of f(t, x, y) from t=0 to t=1).

    n = how many slices to use. More slices = more accurate but slower.
    1000 is way more than enough to get 6+ correct digits.

    a and b below aren't exactly 0 and 1 -- using 0 or 1 directly can
    cause a divide-by-zero type error in f() when x or y is less than 1,
    so we start/stop just barely inside the real range instead.
    """
    # check x and y separately so the error message can say exactly
    # which one is the problem (or both, if both are bad)
    if x <= 0 and y <= 0:
        raise NonPositiveValueError(
            f"Both x ({x}) and y ({y}) must be strictly positive."
        )
    if x <= 0:
        raise NonPositiveValueError(
            f"x must be strictly positive, but x = {x}."
        )
    if y <= 0:
        raise NonPositiveValueError(
            f"y must be strictly positive, but y = {y}."
        )

    a = 0.00001
    b = 0.99999
    h = (b - a) / n

    total = f(a, x, y) + f(b, x, y)

    for i in range(1, n):
        t = a + i * h
        if i % 2 == 1:
            total += 4 * f(t, x, y)   # odd positions get weight 4
        else:
            total += 2 * f(t, x, y)   # even positions get weight 2

    return (h / 3) * total


if __name__ == "__main__":
    # quick sanity checks -- comparing against values I know are correct
    # B(2,3) = 1/12 = 0.08333333...
    print("B(2, 3)  =", beta_via_integration(2.0, 3.0),
          " expected ~0.0833333")
    # B(10,50) is a known tiny value ~1.5916380e-12
    print("B(10,50) =", beta_via_integration(10.0, 50.0),
          " expected ~1.5916380e-12")

    try:
        beta_via_integration(-1.0, 3.0)
    except NonPositiveValueError as e:
        print("Correctly caught NonPositiveValueError:", e)

    try:
        real_power(-2.0, 3.0)
    except UnsupportedDomainError as e:
        print("Correctly caught UnsupportedDomainError:", e)

    try:
        my_ln(0.0)
    except UndefinedOperationError as e:
        print("Correctly caught UndefinedOperationError:", e)
