"""
main.py — Точка входа. Запускает игру «Кто хочет стать миллионером?»
Требует: Python 3.10+, tkinter (входит в стандартную библиотеку).
"""
import tkinter as tk
from tkinter import font as tkfont
import sys, os

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.dirname(__file__))

from settings.config import DIFFICULTIES, AUTHORS
from settings.storage import load_balance, fmt_money
from game.engine import GameSession
from answers.answers import AnswerButtons

# ═══════════════════════════════════════════════════════════════
#  ЦВЕТОВАЯ ПАЛИТРА
# ═══════════════════════════════════════════════════════════════
BG        = "#06060f"
BG2       = "#0c0c22"
CARD      = "#0e1640"
GOLD      = "#f5c518"
GOLD_DIM  = "#c9a100"
BLUE      = "#1a4fff"
TEXT      = "#e8eeff"
TEXT_DIM  = "#7090b0"
GREEN     = "#22c55e"
RED       = "#ef4444"
PURPLE    = "#a78bfa"

# ═══════════════════════════════════════════════════════════════
#  ВСПОМОГАТЕЛЬНЫЕ ВИДЖЕТЫ
# ═══════════════════════════════════════════════════════════════

def styled_btn(parent, text, command, color=GOLD, width=22, font_size=13):
    """Кнопка в стиле игры."""
    btn = tk.Button(
        parent, text=text, command=command,
        font=("Rajdhani", font_size, "bold"),
        fg=BG, bg=color, activebackground=GOLD_DIM,
        activeforeground=BG, relief="flat", bd=0,
        cursor="hand2", width=width, pady=10,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=GOLD_DIM))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def label(parent, text, size=12, color=TEXT, bold=False, font_family="Rajdhani"):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=(font_family, size, weight),
                    fg=color, bg=BG, wraplength=600, justify="center")


def sep(parent):
    f = tk.Frame(parent, bg=GOLD, height=1)
    f.pack(fill="x", padx=40, pady=8)
    return f


# ═══════════════════════════════════════════════════════════════
#  ГЛАВНОЕ ОКНО
# ═══════════════════════════════════════════════════════════════

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Кто хочет стать миллионером?")
        self.configure(bg=BG)
        self.geometry("900x650")
        self.minsize(800, 580)
        self.resizable(True, True)

        # Текущая сессия
        self.session: GameSession | None = None
        self._answer_btns: AnswerButtons | None = None

        # Текущий активный фрейм
        self._frame: tk.Frame | None = None

        self.show_menu()

    # ──────────────────────────────────────────────────────────
    #  УТИЛИТЫ НАВИГАЦИИ
    # ──────────────────────────────────────────────────────────
    def _switch(self, new_frame: tk.Frame):
        if self._frame:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

    # ══════════════════════════════════════════════════════════
    #  ЭКРАН 1: ГЛАВНОЕ МЕНЮ
    # ══════════════════════════════════════════════════════════
    def show_menu(self):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        # Фоновое изображение (место для пользователя)
        # Если хочешь добавить фон — раскомментируй и укажи путь:
        # from PIL import Image, ImageTk
        # img = ImageTk.PhotoImage(Image.open("background/bg.jpg").resize((900,650)))
        # tk.Label(f, image=img, bg=BG).place(relx=0, rely=0, relwidth=1, relheight=1)
        # f.image = img   # не дать сборщику мусора удалить

        # Декоративная рамка
        outer = tk.Frame(f, bg=GOLD, bd=0)
        outer.place(relx=0.5, rely=0.5, anchor="center", width=520, height=420)
        inner = tk.Frame(outer, bg=BG, padx=2, pady=2)
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        # Заголовок
        tk.Label(inner, text="КТО ХОЧЕТ СТАТЬ", font=("Rajdhani", 16, "bold"),
                 fg=GOLD_DIM, bg=BG).pack(pady=(30, 0))
        tk.Label(inner, text="МИЛЛИОНЕРОМ?", font=("Rajdhani", 26, "bold"),
                 fg=GOLD, bg=BG).pack(pady=(0, 4))

        # Баланс
        bal = load_balance()
        tk.Label(inner, text=f"Ваш баланс: {fmt_money(bal)}",
                 font=("Courier New", 13, "bold"), fg=GREEN, bg=BG).pack(pady=4)

        sep(inner)

        # Кнопки
        btn_frame = tk.Frame(inner, bg=BG)
        btn_frame.pack(pady=18)

        styled_btn(btn_frame, "▶   НАЧАТЬ", self.show_difficulty, width=24).pack(pady=8)
        styled_btn(btn_frame, "✦   АВТОРЫ", self.show_authors,
                   color="#4488ff", width=24).pack(pady=8)
        styled_btn(btn_frame, "✕   ВЫЙТИ", self.quit,
                   color="#555", width=24).pack(pady=8)

    # ══════════════════════════════════════════════════════════
    #  ЭКРАН 2: ВЫБОР СЛОЖНОСТИ
    # ══════════════════════════════════════════════════════════
    def show_difficulty(self):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        bal = load_balance()

        tk.Label(f, text="ВЫБОР СЛОЖНОСТИ", font=("Rajdhani", 22, "bold"),
                 fg=GOLD, bg=BG).pack(pady=(40, 4))
        tk.Label(f, text=f"Ваш баланс: {fmt_money(bal)}",
                 font=("Courier New", 12, "bold"), fg=GREEN, bg=BG).pack(pady=(0, 16))
        sep(f)

        cards_frame = tk.Frame(f, bg=BG)
        cards_frame.pack(pady=10)

        diff_order = ["easy", "medium", "hard", "infinite"]
        for diff in diff_order:
            cfg = DIFFICULTIES[diff]
            locked = bal < cfg["unlock"]
            self._diff_card(cards_frame, diff, cfg, locked)

        sep(f)
        styled_btn(f, "◀  НАЗАД", self.show_menu, color="#444", width=18).pack(pady=12)

    def _diff_card(self, parent, diff, cfg, locked):
        color = cfg["color"]
        bg_c  = "#1a1a3a" if not locked else "#111"
        fg_c  = color if not locked else "#444"

        card = tk.Frame(parent, bg=bg_c, bd=0, highlightbackground=color if not locked else "#333",
                        highlightthickness=2, padx=16, pady=10)
        card.pack(fill="x", padx=40, pady=5)

        row = tk.Frame(card, bg=bg_c)
        row.pack(fill="x")

        # Название
        tk.Label(row, text=cfg["name"], font=("Rajdhani", 14, "bold"),
                 fg=fg_c, bg=bg_c, width=20, anchor="w").pack(side="left")

        info = f"{cfg['questions'] or '∞'} вопр.  |  "
        if diff != "infinite":
            info += f"+{fmt_money(cfg['reward'])} за вопрос  |  ❤ × {cfg['lives']}"
        else:
            info += f"смешанные вопросы  |  ❤ × {cfg['lives']}"

        tk.Label(row, text=info, font=("Rajdhani", 10),
                 fg=TEXT_DIM if not locked else "#333", bg=bg_c).pack(side="left", padx=8)

        if locked:
            need = fmt_money(cfg["unlock"])
            tk.Label(row, text=f"🔒 Требуется {need}", font=("Rajdhani", 10, "bold"),
                     fg=RED, bg=bg_c).pack(side="right", padx=6)
        else:
            btn = tk.Button(row, text="ИГРАТЬ →",
                            font=("Rajdhani", 10, "bold"),
                            fg=BG, bg=color, activebackground=GOLD_DIM,
                            relief="flat", bd=0, cursor="hand2", padx=10, pady=4,
                            command=lambda d=diff: self.start_game(d))
            btn.pack(side="right", padx=6)

    # ══════════════════════════════════════════════════════════
    #  ЭКРАН 3: ИГРА
    # ══════════════════════════════════════════════════════════
    def start_game(self, difficulty: str):
        self.session = GameSession(difficulty)
        self._show_game_screen()

    def _show_game_screen(self):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        cfg = DIFFICULTIES[self.session.difficulty]

        # ── HUD (верхняя полоса) ────────────────────────────
        hud = tk.Frame(f, bg=BG2, pady=8)
        hud.pack(fill="x")

        self._lbl_balance = tk.Label(hud, text="", font=("Courier New", 14, "bold"),
                                     fg=GOLD, bg=BG2)
        self._lbl_balance.pack(side="left", padx=20)

        self._lbl_lives = tk.Label(hud, text="", font=("Rajdhani", 14, "bold"),
                                   fg=RED, bg=BG2)
        self._lbl_lives.pack(side="right", padx=20)

        self._lbl_progress = tk.Label(hud, text="", font=("Rajdhani", 11),
                                      fg=TEXT_DIM, bg=BG2)
        self._lbl_progress.pack(side="right", padx=20)

        # ── Вопрос ─────────────────────────────────────────
        q_frame = tk.Frame(f, bg=CARD, bd=0,
                           highlightbackground=GOLD_DIM, highlightthickness=1)
        q_frame.pack(fill="x", padx=30, pady=(18, 8))

        self._lbl_qnum = tk.Label(q_frame, text="", font=("Rajdhani", 10),
                                  fg=GOLD_DIM, bg=CARD, anchor="w")
        self._lbl_qnum.pack(fill="x", padx=16, pady=(10, 0))

        self._lbl_question = tk.Label(q_frame, text="", font=("Rajdhani", 15, "bold"),
                                      fg=TEXT, bg=CARD, wraplength=820,
                                      justify="center", pady=10)
        self._lbl_question.pack(fill="x", padx=16, pady=(4, 14))

        # ── Ответы ─────────────────────────────────────────
        a_frame = tk.Frame(f, bg=BG)
        a_frame.pack(fill="both", expand=True, padx=30, pady=4)
        self._answer_btns = AnswerButtons(a_frame)

        # ── Нижняя панель ──────────────────────────────────
        bot = tk.Frame(f, bg=BG2, pady=8)
        bot.pack(fill="x", side="bottom")

        styled_btn(bot, "💰  ВЫЙТИ И СОХРАНИТЬ",
                   self._exit_save, color="#226622", width=26,
                   font_size=11).pack(side="left", padx=20)

        self._lbl_reward_flash = tk.Label(bot, text="", font=("Courier New", 13, "bold"),
                                          fg=GREEN, bg=BG2)
        self._lbl_reward_flash.pack(side="right", padx=20)

        self._update_hud()
        self._load_question()

    def _update_hud(self):
        s = self.session
        self._lbl_balance.config(text=f"💵  {fmt_money(load_balance())}")
        hearts = "❤ " * s.lives + "♡ " * max(0, DIFFICULTIES[s.difficulty]["lives"] - s.lives)
        self._lbl_lives.config(text=hearts.strip())
        total = s.total_questions or "∞"
        self._lbl_progress.config(text=f"Вопрос  {s.index + 1} / {total}")

    def _load_question(self):
        s = self.session
        q = s.current_question
        if q is None:
            self._victory()
            return
        total = s.total_questions or "∞"
        self._lbl_qnum.config(text=f"Вопрос {s.index + 1} из {total}")
        self._lbl_question.config(text=q["q"])
        self._answer_btns.load(q["a"], q["correct"], self._on_answer)
        self._lbl_reward_flash.config(text="")

    def _on_answer(self, correct: bool):
        result = self.session.answer(correct)
        status = result["status"]

        if status == "correct":
            reward = result["reward"]
            self._lbl_reward_flash.config(text=f"+{fmt_money(reward)} ✔", fg=GREEN)
            self._update_hud()
            self.after(1600, self._load_question)

        elif status == "wrong_continue":
            self._lbl_reward_flash.config(text=f"Неверно! Жизней: {self.session.lives}", fg=RED)
            self._update_hud()
            self.after(1600, self._load_question)

        elif status == "game_over":
            self.after(800, lambda: self._game_over(result["lost"]))

        elif status == "victory":
            self.after(800, lambda: self._victory(result))

    def _exit_save(self):
        bal = self.session.exit_save()
        self.show_menu()

    # ══════════════════════════════════════════════════════════
    #  ЭКРАН 4: GAME OVER
    # ══════════════════════════════════════════════════════════
    def _game_over(self, lost: int):
        f = tk.Frame(self, bg="black")
        self._switch(f)

        # Чёрный экран с надписью
        tk.Label(f, text="", bg="black").pack(expand=True)
        tk.Label(f, text="GAME OVER", font=("Rajdhani", 52, "bold"),
                 fg=RED, bg="black").pack()
        tk.Label(f, text=f"Вы потеряли {fmt_money(lost)}",
                 font=("Rajdhani", 16), fg=TEXT_DIM, bg="black").pack(pady=12)
        tk.Label(f, text="", bg="black").pack(expand=True)

        btn_f = tk.Frame(f, bg="black")
        btn_f.pack(pady=20)
        styled_btn(btn_f, "НАЧАТЬ ЗАНОВО", self.show_menu, color=RED, width=20).pack(pady=8)
        styled_btn(btn_f, "ВЫЙТИ",         self.quit,      color="#444", width=20).pack(pady=8)

    # ══════════════════════════════════════════════════════════
    #  ЭКРАН 5: ПОБЕДА
    # ══════════════════════════════════════════════════════════
    def _victory(self, result: dict | None = None):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        tk.Label(f, text="", bg=BG).pack(expand=True)
        tk.Label(f, text="🏆  ПОЗДРАВЛЯЕМ!", font=("Rajdhani", 36, "bold"),
                 fg=GOLD, bg=BG).pack()

        if result:
            tk.Label(f, text=f"Вы заработали за сессию: {fmt_money(result.get('session', 0))}",
                     font=("Rajdhani", 15), fg=GREEN, bg=BG).pack(pady=6)

        bal = load_balance()
        tk.Label(f, text=f"Ваш общий баланс: {fmt_money(bal)}",
                 font=("Courier New", 18, "bold"), fg=GOLD, bg=BG).pack(pady=10)
        tk.Label(f, text="", bg=BG).pack(expand=True)

        btn_f = tk.Frame(f, bg=BG)
        btn_f.pack(pady=20)
        styled_btn(btn_f, "▶  ИГРАТЬ ЕЩЁ", self.show_difficulty, width=22).pack(pady=8)
        styled_btn(btn_f, "◀  ГЛАВНОЕ МЕНЮ", self.show_menu, color="#4488ff", width=22).pack(pady=8)

    # ══════════════════════════════════════════════════════════
    #  ЭКРАН 6: АВТОРЫ
    # ══════════════════════════════════════════════════════════
    def show_authors(self):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        tk.Label(f, text="", bg=BG).pack(expand=True)
        tk.Label(f, text="✦  АВТОРЫ  ✦", font=("Rajdhani", 26, "bold"),
                 fg=GOLD, bg=BG).pack(pady=(0, 16))
        sep(f)

        for name, role in AUTHORS:
            row = tk.Frame(f, bg=CARD, highlightbackground=GOLD_DIM,
                           highlightthickness=1)
            row.pack(fill="x", padx=120, pady=5)
            tk.Label(row, text=name, font=("Rajdhani", 14, "bold"),
                     fg=TEXT, bg=CARD, width=26, anchor="w",
                     padx=16, pady=10).pack(side="left")
            tk.Label(row, text=role, font=("Rajdhani", 12),
                     fg=TEXT_DIM, bg=CARD, padx=16).pack(side="right")

        tk.Label(f, text="", bg=BG).pack(expand=True)
        sep(f)
        styled_btn(f, "◀  НАЗАД", self.show_menu, color="#444", width=18).pack(pady=16)


# ═══════════════════════════════════════════════════════════════
#  ЗАПУСК
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
