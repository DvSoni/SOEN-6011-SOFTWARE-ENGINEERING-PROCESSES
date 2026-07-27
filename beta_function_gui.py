"""
SOEN 6011 - Deliverable 2, Problem 5
Beta function B(x, y) - Graphical User Interface (Tkinter)

This GUI is a thin wrapper around beta_function_scratch.py, which
contains the actual from-scratch math (no ** operator, no external
libraries). This file only handles displaying input fields, a
button, and showing the result or an error message.

Traceability to requirements:
    REQ-003, REQ-009 : invalid input is caught and shown as a clear,
                        plain-language error message in the GUI
                        (not a crash)
    REQ-010           : runs standalone via `python3 beta_function_gui.py`,
                        no IDE dependency
    REQ-011           : the GUI echoes the input values alongside
                        the computed result
"""

import tkinter as tk
from tkinter import ttk

from beta_function_scratch import beta_via_integration, InvalidInputError


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

        # --- x input ---
        ttk.Label(main_frame, text="x (must be > 0):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.x_entry = ttk.Entry(main_frame, width=15)
        self.x_entry.grid(row=1, column=1, pady=5)

        # --- y input ---
        ttk.Label(main_frame, text="y (must be > 0):").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.y_entry = ttk.Entry(main_frame, width=15)
        self.y_entry.grid(row=2, column=1, pady=5)

        # --- Calculate button ---
        calculate_button = ttk.Button(
            main_frame, text="Calculate", command=self.on_calculate
        )
        calculate_button.grid(row=3, column=0, columnspan=2, pady=15)

        # --- Result / error display ---
        self.result_label = ttk.Label(
            main_frame, text="", font=("Helvetica", 11), foreground="black"
        )
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        self.error_label = ttk.Label(
            main_frame, text="", font=("Helvetica", 10), foreground="red", wraplength=360
        )
        self.error_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Let Enter key trigger calculation too
        root.bind("<Return>", lambda event: self.on_calculate())

    def on_calculate(self):
        # clear previous messages
        self.result_label.config(text="")
        self.error_label.config(text="")

        x_raw = self.x_entry.get()
        y_raw = self.y_entry.get()

        try:
            x = float(x_raw)
        except ValueError:
            self.error_label.config(text=f"Error: '{x_raw}' is not a valid number for x.")
            return

        try:
            y = float(y_raw)
        except ValueError:
            self.error_label.config(text=f"Error: '{y_raw}' is not a valid number for y.")
            return

        try:
            result = beta_via_integration(x, y)
        except InvalidInputError as e:
            self.error_label.config(text=f"Error: {e}")
            return

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
