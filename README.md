# Beta Function B(x, y) Calculator

**SOEN 6011 — Software Engineering Processes (Summer 2026)**
**Concordia University — Individual Project**

An implementation of the Beta function, B(x, y), built from first
principles as part of a scientific software engineering course project.

---

## What it does

Computes the value of the Beta function:

```
B(x, y) = Integral from 0 to 1 of  t^(x-1) * (1-t)^(y-1) dt
```

for any strictly positive real numbers x and y, using **Simpson's Rule**
numerical integration. Provides a simple graphical interface for entering
values and viewing the result.

---

## Project status

This repository currently reflects **Deliverable 2 (D2)**:
- Core math rebuilt entirely from scratch (no `**` operator, no `math`
  module, no external libraries)
- Graphical user interface (Tkinter)
- Custom exception hierarchy for error handling

Deliverable 1's original CLI version and requirements list are described
in the full project report (not included in this repo — LaTeX report is
submitted separately per course instructions).

---

## Files

| File | Description |
|---|---|
| `beta_function_scratch.py` | Core math logic: from-scratch `exp`, `ln`, and `power` functions, plus the Beta function itself and its custom exceptions |
| `beta_function_gui.py` | Tkinter GUI — entry fields for x and y, a Calculate button, and result/error display |

---

## How to run

Requires Python 3 (no external packages needed — everything uses only
the standard library).

```bash
python3 beta_function_gui.py
```

1. Enter a positive real number for **x**
2. Enter a positive real number for **y**
3. Click **Calculate** (or press Enter)
4. The result appears below, or a clear error message if the input is invalid

---

## How the calculation works

1. **`my_exp(z)`** — computes e^z using a Taylor series, with range
   reduction (repeated halving + squaring) so it stays accurate for
   large inputs.
2. **`my_ln(y)`** — computes ln(y) using a fast-converging series, with
   range reduction (scaling toward 1) for the same reason.
3. **`real_power(base, exponent)`** — computes base^exponent for any
   real exponent, using the identity `base^exponent = e^(exponent * ln(base))`,
   since Beta function inputs aren't limited to whole numbers.
4. **`beta_via_integration(x, y)`** — applies Simpson's Rule (1000
   subintervals) to numerically integrate the Beta function's integrand,
   using the from-scratch functions above.

All results have been verified against known exact values (e.g.,
B(2, 3) = 1/12) and cross-checked against Python's built-in `math`
library during development.

---

## Error handling

Invalid input is handled through a custom exception hierarchy rather
than a single generic error, so messages are specific to what went
wrong:

```
BetaFunctionError            (base class)
├── NonPositiveValueError    (x or y is zero or negative)
├── UndefinedOperationError  (e.g. ln of a non-positive number)
└── UnsupportedDomainError   (e.g. negative base passed internally)
```

The GUI also validates that x and y are entered as valid numbers before
attempting the calculation, and reports both fields together if both are
invalid at once.

---

## Known limitations

- Very large input values (x, y in the hundreds or more) may cause
  `B(x, y)` to underflow toward zero, since the true mathematical value
  becomes extremely small — this is expected numerical behavior, not a
  bug.
- This version accepts one (x, y) pair at a time; batch input is out of
  scope for this deliverable.

---

## Author

Dv Soni — SOEN 6011, Summer 2026