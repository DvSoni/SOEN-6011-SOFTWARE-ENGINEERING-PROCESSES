# Beta Function B(x, y) Calculator

**SOEN 6011 — Software Engineering Processes (Summer 2026)**
**Concordia University — Individual Project**
**Version:** 1.2.1

An implementation of the Beta function, B(x, y), built from first
principles as part of a scientific software engineering course project.

---

## What it does

Computes the value of the Beta function:

```
B(x, y) = Integral from 0 to 1 of  t^(x-1) * (1-t)^(y-1) dt
```

for strictly positive real numbers x and y, using **Simpson's Rule**
numerical integration, with all supporting math (exponentiation,
natural log) built entirely from scratch. Provides a Tkinter GUI for
entering values and viewing the result.

---

## Files

| File | Description |
|---|---|
| `beta_function_scratch.py` | Core math: from-scratch `exp`, `ln`, and `power` functions, the Beta function itself, and its custom exception hierarchy |
| `beta_function_gui.py` | Tkinter GUI — entry fields for x and y, a Calculate button, result/error display |
| `test_beta_function.py` | Unit tests (Python's `unittest`) covering known values, symmetry, exceptions, and a documented precision limitation |

---

## How to run

Requires Python 3. No external packages needed — everything uses only
the standard library.

**Run the calculator:**
```bash
python3 beta_function_gui.py
```
1. Enter a positive real number for **x**
2. Enter a positive real number for **y**
3. Click **Calculate** (or press Enter)
4. The result appears below, or a clear error message if input is invalid

**Run the tests:**
```bash
python3 -m unittest test_beta_function.py -v
```

---

## How the calculation works

1. **`my_exp(z)`** — computes e^z using a Taylor series, with range
   reduction (repeated halving + squaring) for accuracy on large inputs.
2. **`my_ln(y)`** — computes ln(y) using a fast-converging series, with
   range reduction (scaling toward 1).
3. **`real_power(base, exponent)`** — computes base^exponent for any
   real exponent, via `base^exponent = e^(exponent * ln(base))`, since
   Beta function inputs aren't limited to whole numbers.
4. **`beta_via_integration(x, y)`** — applies Simpson's Rule (1000
   subintervals) to numerically integrate the Beta function, using the
   from-scratch functions above.

Verified against known exact values (e.g., B(2,3) = 1/12) and
cross-checked against Python's built-in `math` library during
development.

---

## Error handling

Invalid input is handled through a custom exception hierarchy, not a
single generic error, so messages are specific to what went wrong:

```
BetaFunctionError            (base class)
├── NonPositiveValueError    (x or y is zero or negative)
├── UndefinedOperationError  (e.g. ln of a non-positive number)
└── UnsupportedDomainError   (e.g. negative base passed internally)
```

Positivity errors name the specific variable at fault (e.g. "x must be
strictly positive, but x = -1"). The GUI also validates that x and y
are entered as valid numbers before calculating, and reports both
fields together if both are invalid at once.

---

## Code quality

- **PEP-8 compliant** — verified with Flake8, zero warnings
- **Pylint score: 10.00/10**
- Debugged using Python's built-in `pdb`
- Semantic Versioning (MAJOR.MINOR.PATCH) — current version 1.2.1

---

## Accessibility

- Keyboard focus is set automatically on the x field at launch
- Error text uses a dark red (#A32D2D, 6.2:1 contrast ratio) instead
  of pure red (3.5:1), to meet WCAG AA's 4.5:1 minimum for text
- Errors never rely on color alone — every message starts with the
  word "Error:"
- **Known limitation:** vanilla Tkinter has no reliable, cross-platform
  way to programmatically link a label to its entry field for screen
  readers (no ARIA equivalent exists in Tkinter). Documented here
  rather than left unmentioned.

---

## Known limitations

- **Precision for x, y < 1:** the integrand has a singularity at the
  interval's edges (t=0, t=1) that Simpson's Rule under-resolves in
  this region. For x, y ≥ 1, error is under 0.01%. For x, y < 1 (e.g.
  B(0.5, 0.5)), error is around 4%, below the project's 6-digit
  precision target. This is covered by a dedicated test
  (`TestKnownPrecisionLimitation`) that documents the bound rather
  than hiding it. A future fix would use adaptive step sizing near
  the singularities.
- Very large inputs (x, y in the hundreds or more) cause B(x, y) to
  underflow toward zero, since the true mathematical value becomes
  extremely small — expected numerical behavior, not a bug.
- Accepts one (x, y) pair at a time; batch input is out of scope.

---

## Author

Divy Soni — SOEN 6011, Summer 2026
