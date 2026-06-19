#!/usr/bin/env python3
# GUI calculator built with tkinter
# supports keyboard input too

import tkinter as tk

BUTTONS = [
    ["C",  "+/-", "%", "÷"],
    ["7",  "8",   "9", "×"],
    ["4",  "5",   "6", "−"],
    ["1",  "2",   "3", "+"],
    ["0",  ".",   "⌫", "="],
]

BG          = "#0d0d0d"
DISPLAY_BG  = "#0d0d0d"
DISPLAY_FG  = "#00ff88"
BTN_BG      = "#1a1a1a"
BTN_FG      = "#00ff88"
BTN_BORDER  = "#00ff88"
OP_BG       = "#003322"
OP_FG       = "#00ff88"
EQ_BG       = "#00ff88"
EQ_FG       = "#0d0d0d"
CLEAR_BG    = "#1a0000"
CLEAR_FG    = "#ff4444"

SPECIAL_BG = {"=": EQ_BG,  "÷": OP_BG, "×": OP_BG, "−": OP_BG, "+": OP_BG, "C": CLEAR_BG}
SPECIAL_FG = {"=": EQ_FG,  "÷": OP_FG, "×": OP_FG, "−": OP_FG, "+": OP_FG, "C": CLEAR_FG}


class Calculator:
    def __init__(self, root):
        self.root      = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.expr      = ""
        self.just_eval = False

        # header label
        tk.Label(root, text="[ CALC ]", font=("Courier", 11),
                 bg=BG, fg="#005533").pack(anchor="w", padx=12, pady=(8, 0))

        self.display_var = tk.StringVar(value="0")
        tk.Entry(root, textvariable=self.display_var, font=("Courier", 36, "bold"),
                 justify="right", bd=0, bg=DISPLAY_BG, fg=DISPLAY_FG,
                 readonlybackground=DISPLAY_BG, state="readonly",
                 insertbackground=DISPLAY_FG).pack(fill="x", padx=12, pady=(2, 8))

        tk.Frame(root, bg="#00ff88", height=1).pack(fill="x", padx=12, pady=(0, 8))

        frame = tk.Frame(root, bg=BG)
        frame.pack(padx=10, pady=(0, 10))
        for r, row in enumerate(BUTTONS):
            for c, label in enumerate(row):
                bg = SPECIAL_BG.get(label, BTN_BG)
                fg = SPECIAL_FG.get(label, BTN_FG)
                tk.Button(frame, text=label, font=("Courier", 18, "bold"), width=4, height=2,
                          bg=bg, fg=fg, activebackground="#003322", activeforeground="#00ff88",
                          relief="flat", bd=0,
                          command=lambda l=label: self.press(l)).grid(row=r, column=c, padx=2, pady=2)

        root.bind("<Key>", self.on_key)

    def press(self, key):
        if key in "0123456789":
            if self.just_eval:
                self.expr = ""; self.just_eval = False
            self.expr = ("" if self.expr == "0" else self.expr) + key

        elif key == ".":
            if self.just_eval:
                self.expr = "0"; self.just_eval = False
            last = self.expr.replace("+","÷").replace("÷"," ").replace("×"," ").replace("−"," ").split()[-1] if self.expr else ""
            if "." not in last:
                self.expr += ("0" if not self.expr else "") + "."

        elif key in ("+", "−", "×", "÷"):
            self.just_eval = False
            if self.expr and self.expr[-1] in "+−×÷":
                self.expr = self.expr[:-1]
            self.expr += key

        elif key == "=":
            if not self.expr:
                return
            try:
                result = eval(self.expr.replace("×","*").replace("÷","/").replace("−","-"))
                result = int(result) if result == int(result) else round(result, 10)
                self.expr = str(result)
            except ZeroDivisionError:
                self.expr = "Error"
            except Exception:
                self.expr = "Error"
            self.just_eval = True

        elif key == "C":
            self.expr = ""; self.just_eval = False
        elif key == "⌫":
            self.expr = self.expr[:-1]
        elif key == "+/-":
            try:
                v = -float(self.expr)
                self.expr = str(int(v) if v == int(v) else v)
            except Exception: pass
        elif key == "%":
            try:
                v = float(self.expr) / 100
                self.expr = str(int(v) if v == int(v) else v)
            except Exception: pass

        self.display_var.set(self.expr if self.expr else "0")

    def on_key(self, event):
        m = {"*": "×", "/": "÷", "-": "−", "\r": "=", "\x08": "⌫"}
        k = m.get(event.char, event.char)
        if k in "0123456789.+−×÷=⌫C":
            self.press(k)


def main():
    root = tk.Tk()
    Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
