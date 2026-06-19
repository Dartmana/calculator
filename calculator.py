#!/usr/bin/env python3
# calculator.py - a simple calculator with a retro terminal look
# built using tkinter which comes with python so no extra installs

import tkinter as tk

# colors
bg_color      = "#0d0d0d"
green         = "#00ff88"
dark_green    = "#003322"
red           = "#ff4444"
dark_red      = "#1a0000"
btn_color     = "#1a1a1a"


def get_btn_colors(label):
    # operators get a dark green background
    if label in ("+", "−", "×", "÷"):
        return dark_green, green
    # equals is inverted - green background black text
    elif label == "=":
        return green, bg_color
    # clear button is red
    elif label == "C":
        return dark_red, red
    # everything else is the default dark button
    else:
        return btn_color, green


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg=bg_color)

        self.expression = ""
        self.just_evaluated = False

        # top label just to make it look different
        tk.Label(root, text="CALC v1", font=("Courier", 10),
                 bg=bg_color, fg=dark_green).pack(anchor="w", padx=12, pady=(8, 0))

        # the display where numbers show up
        self.display = tk.StringVar()
        self.display.set("0")

        tk.Entry(root, textvariable=self.display, font=("Courier", 34, "bold"),
                 justify="right", state="readonly", bd=0,
                 bg=bg_color, fg=green,
                 readonlybackground=bg_color).pack(fill="x", padx=12, pady=(4, 6))

        # divider line
        tk.Frame(root, bg=green, height=1).pack(fill="x", padx=12, pady=(0, 8))

        # button grid
        button_layout = [
            ["C",  "+/-", "%", "÷"],
            ["7",  "8",   "9", "×"],
            ["4",  "5",   "6", "−"],
            ["1",  "2",   "3", "+"],
            ["0",  ".",   "⌫", "="],
        ]

        grid = tk.Frame(root, bg=bg_color)
        grid.pack(padx=10, pady=(0, 10))

        for row_num, row in enumerate(button_layout):
            for col_num, label in enumerate(row):
                bg, fg = get_btn_colors(label)

                btn = tk.Button(grid, text=label, font=("Courier", 18, "bold"),
                                width=4, height=2, bg=bg, fg=fg,
                                activebackground=dark_green, activeforeground=green,
                                relief="flat", bd=0)

                # have to do this so each button remembers its own label
                btn.config(command=lambda l=label: self.button_clicked(l))
                btn.grid(row=row_num, column=col_num, padx=2, pady=2)

        # keyboard support
        root.bind("<Key>", self.handle_keypress)

    def button_clicked(self, key):
        if key.isdigit():
            if self.just_evaluated:
                self.expression = ""
                self.just_evaluated = False
            if self.expression == "0":
                self.expression = key
            else:
                self.expression += key

        elif key == ".":
            if self.just_evaluated:
                self.expression = "0"
                self.just_evaluated = False
            if "." not in self.expression:
                if self.expression == "":
                    self.expression = "0"
                self.expression += "."

        elif key in ("+", "−", "×", "÷"):
            self.just_evaluated = False
            # replace operator if one was already typed
            if self.expression and self.expression[-1] in "+−×÷":
                self.expression = self.expression[:-1]
            self.expression += key

        elif key == "=":
            if self.expression == "":
                return
            try:
                # swap out the display symbols for real python operators
                to_eval = self.expression
                to_eval = to_eval.replace("×", "*")
                to_eval = to_eval.replace("÷", "/")
                to_eval = to_eval.replace("−", "-")
                result = eval(to_eval)
                # show as int if theres no decimal part
                if float(result) == int(result):
                    self.expression = str(int(result))
                else:
                    self.expression = str(round(result, 8))
            except ZeroDivisionError:
                self.expression = "cant divide by 0"
            except:
                self.expression = "Error"
            self.just_evaluated = True

        elif key == "C":
            self.expression = ""
            self.just_evaluated = False

        elif key == "⌫":
            self.expression = self.expression[:-1]

        elif key == "+/-":
            try:
                val = float(self.expression) * -1
                if float(val) == int(val):
                    self.expression = str(int(val))
                else:
                    self.expression = str(val)
            except:
                pass

        elif key == "%":
            try:
                val = float(self.expression) / 100
                if float(val) == int(val):
                    self.expression = str(int(val))
                else:
                    self.expression = str(val)
            except:
                pass

        # update the display
        if self.expression == "":
            self.display.set("0")
        else:
            self.display.set(self.expression)

    def handle_keypress(self, event):
        key = event.char

        if key == "*":
            self.button_clicked("×")
        elif key == "/":
            self.button_clicked("÷")
        elif key == "-":
            self.button_clicked("−")
        elif key in ("\r", "\n"):
            self.button_clicked("=")
        elif event.keysym == "BackSpace":
            self.button_clicked("⌫")
        elif key in "0123456789.+C%":
            self.button_clicked(key)


def main():
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
