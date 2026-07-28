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
"""

import tkinter as tk
from tkinter import ttk

from beta_function_scratch import beta_via_integration, BetaFunctionError


class BetaFunctionApp:
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

        # this one shows error messages in red if something went wrong
        self.error_label = ttk.Label(
            main_frame, text="", font=("Helvetica", 10), foreground="red", wraplength=360
        )
        self.error_label.grid(row=5, column=0, columnspan=2, pady=5)

        # so pressing Enter also triggers Calculate, not just clicking the button
        root.bind("<Return>", lambda event: self.on_calculate())

    def on_calculate(self):
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
                text=f"Error: Please enter a valid number for x instead of '{x_raw}', "
                     f"and enter a valid number for y instead of '{y_raw}'."
            )
            return
        if not x_is_valid:
            self.error_label.config(text=f"Please enter a valid number for x instead of '{x_raw}'.")
            return
        if not y_is_valid:
            self.error_label.config(text=f"Please enter a valid number for y instead of '{y_raw}'.")
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
    root = tk.Tk()
    app = BetaFunctionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()