"""
SOEN 6011 - Deliverable 2, Problem 5
Beta function B(x, y) - GUI version using Tkinter

This file is just the interface -- two text boxes, a button, and a
label to show the result or an error. All the actual math lives in
beta_function_scratch.py, this file just calls it.

I kept it split into two files on purpose: this way the math can be
tested completely on its own (see the unit tests later on) without
needing the GUI to even open.

Which requirement each part is for:
    REQ-003, REQ-009 : bad input gets caught and shown as a clear
                        message instead of crashing the program
    REQ-010          : just run "python3 beta_function_gui.py",
                        no IDE needed
    REQ-011          : shows the input values next to the answer,
                        so you can double check what you typed

Accessibility notes:
    - x field gets keyboard focus automatically on launch, so you
      can start typing without clicking first
    - error text uses a darker red (#A32D2D, 6.2:1 contrast) instead
      of pure red (3.5:1), to pass WCAG AA's 4.5:1 minimum
    - error messages never rely on color alone - they always start
      with the word "Error:"
    - known limitation: vanilla Tkinter doesn't have a reliable,
      cross-platform way to programmatically link a label to its
      entry field for screen readers (no ARIA equivalent exists in
      Tkinter), so screen-reader users would hear "edit text" rather
      than "x, must be greater than 0" - documented honestly here
      rather than left unmentioned
"""

__version__ = "1.2.1"

import tkinter as tk
from tkinter import ttk

from beta_function_scratch import beta_via_integration, BetaFunctionError


class BetaFunctionApp:
    # pylint: disable=too-few-public-methods
    # This class only needs one public method (on_calculate) - it's
    # a thin GUI wrapper, not meant to have a larger public interface.
    """Tkinter GUI wrapper around the from-scratch Beta function."""

    def __init__(self, root):
        self.root = root
        self.root.title("Beta Function B(x, y) Calculator")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        main_frame = ttk.Frame(root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")

        title_label = ttk.Label(
            main_frame,
            text="Beta Function B(x, y)",
            font=("Helvetica", 16, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # box for x
        ttk.Label(main_frame, text="x (must be > 0):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.x_entry = ttk.Entry(main_frame, width=15)
        self.x_entry.grid(row=1, column=1, pady=5)

        # box for y
        ttk.Label(main_frame, text="y (must be > 0):").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.y_entry = ttk.Entry(main_frame, width=15)
        self.y_entry.grid(row=2, column=1, pady=5)

        # calculate button, runs on_calculate when clicked
        calculate_button = ttk.Button(
            main_frame, text="Calculate", command=self.on_calculate
        )
        calculate_button.grid(row=3, column=0, columnspan=2, pady=15)

        # this label shows the answer once it's calculated
        self.result_label = ttk.Label(
            main_frame, text="", font=("Helvetica", 11), foreground="black"
        )
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        # this one shows error messages in a dark red if something
        # went wrong. Using a darker red than pure "red" here since
        # pure red only has a 3.5:1 contrast ratio against the default
        # background (fails WCAG AA, which needs 4.5:1) - this dark
        # red (#A32D2D) gives 6.2:1, which passes.
        self.error_label = ttk.Label(
            main_frame, text="", font=("Helvetica", 10),
            foreground="#A32D2D", wraplength=360
        )
        self.error_label.grid(row=5, column=0, columnspan=2, pady=5)

        # so pressing Enter also triggers Calculate, not just
        # clicking the button
        root.bind("<Return>", lambda event: self.on_calculate())

        # accessibility: put the cursor in the x field right away,
        # so keyboard-only users don't have to click first
        self.x_entry.focus()

    def on_calculate(self):
        """Read x and y from the entry fields, validate them, and
        show either the computed B(x, y) or an error message."""
        # clear out whatever was shown from last time first
        self.result_label.config(text="")
        self.error_label.config(text="")

        x_raw = self.x_entry.get()
        y_raw = self.y_entry.get()

        # try converting both to numbers before deciding what error to
        # show -- this way if BOTH boxes are bad, the message mentions
        # both instead of only complaining about x and hiding the fact
        # y is also wrong
        x_is_valid = True
        y_is_valid = True

        try:
            x = float(x_raw)
        except ValueError:
            x_is_valid = False

        try:
            y = float(y_raw)
        except ValueError:
            y_is_valid = False

        if not x_is_valid and not y_is_valid:
            self.error_label.config(
                text=f"Error: '{x_raw}' is not a valid number for x, "
                     f"and '{y_raw}' is not a valid number for y."
            )
            return
        if not x_is_valid:
            self.error_label.config(
                text=f"Error: '{x_raw}' is not a valid number for x."
            )
            return
        if not y_is_valid:
            self.error_label.config(
                text=f"Error: '{y_raw}' is not a valid number for y."
            )
            return

        # now that x and y are valid numbers, actually run the calculation
        try:
            result = beta_via_integration(x, y)
        except BetaFunctionError as e:
            # catching the parent class here catches NonPositiveValueError,
            # UndefinedOperationError, and UnsupportedDomainError all at
            # once, don't need a separate except for each one
            self.error_label.config(text=f"Error: {e}")
            return

        # if the answer is really tiny, showing 6 decimal places would
        # just print 0.000000 which looks wrong, so switch to scientific
        # notation in that case instead
        if abs(result) < 1e-6:
            result_text = f"B({x}, {y}) = {result:.6e}"
        else:
            result_text = f"B({x}, {y}) = {result:.6f}"

        self.result_label.config(text=result_text)


def main():
    """Launch the Beta function calculator GUI."""
    root = tk.Tk()
    BetaFunctionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
