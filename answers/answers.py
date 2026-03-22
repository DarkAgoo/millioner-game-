"""
Модуль ответов — создаёт 4 кнопки A/B/C/D и обрабатывает выбор.
"""
import tkinter as tk

LABELS = ["A", "B", "C", "D"]

# Цвета ответов
CLR_DEFAULT  = "#0e1a4a"
CLR_BORDER   = "#1a3a8a"
CLR_HOVER    = "#1a2a6a"
CLR_SELECTED = "#2255cc"
CLR_CORRECT  = "#166534"
CLR_WRONG    = "#7f1d1d"
CLR_TEXT     = "#e8eeff"
CLR_LABEL    = "#f5c518"


class AnswerButtons:
    def __init__(self, parent: tk.Frame):
        self.parent = parent
        self.buttons: list[tk.Button] = []
        self.locked = False
        self._build()

    def _build(self):
        for w in self.parent.winfo_children():
            w.destroy()
        self.buttons = []

        grid = tk.Frame(self.parent, bg="#06060f")
        grid.pack(fill="both", expand=True, padx=10, pady=5)
        grid.columnconfigure((0, 1), weight=1)
        grid.rowconfigure((0, 1), weight=1)

        for i in range(4):
            row, col = divmod(i, 2)
            btn = tk.Button(
                grid,
                text="",
                font=("Rajdhani", 13, "bold"),
                fg=CLR_TEXT,
                bg=CLR_DEFAULT,
                activebackground=CLR_HOVER,
                activeforeground="white",
                relief="flat",
                bd=0,
                cursor="hand2",
                wraplength=320,
                justify="left",
                padx=14,
                pady=12,
                highlightbackground=CLR_BORDER,
                highlightthickness=2,
            )
            btn.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
            # hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CLR_HOVER) if not self.locked else None)
            btn.bind("<Leave>", lambda e, b=btn, idx=i: self._reset_hover(b, idx))
            self.buttons.append(btn)

    def _reset_hover(self, btn: tk.Button, idx: int):
        if not self.locked:
            btn.config(bg=CLR_DEFAULT)

    def load(self, answers: list[str], correct: int, on_answer):
        self.locked = False
        for i, (btn, text) in enumerate(zip(self.buttons, answers)):
            btn.config(
                text=f"  {LABELS[i]}.  {text}",
                bg=CLR_DEFAULT,
                state="normal",
            )
            btn.config(command=lambda idx=i: self._select(idx, correct, on_answer))

    def _select(self, chosen: int, correct: int, on_answer):
        if self.locked:
            return
        self.locked = True

        # Подсвечиваем выбранный
        self.buttons[chosen].config(bg=CLR_SELECTED)

        # Через 500ms показываем правильный/неправильный
        self.parent.after(500, lambda: self._reveal(chosen, correct, on_answer))

    def _reveal(self, chosen: int, correct: int, on_answer):
        self.buttons[correct].config(bg=CLR_CORRECT)
        if chosen != correct:
            self.buttons[chosen].config(bg=CLR_WRONG)
        # Через 1.2s вызываем callback
        self.parent.after(1200, lambda: on_answer(chosen == correct))
