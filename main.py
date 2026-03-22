"""
main.py — Точка входа. Запускает игру «Кто хочет стать миллионером?»
Требует: Python 3.10+, tkinter (входит в стандартную библиотеку).
"""
import tkinter as tk
import sys, os, json

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

from settings.config import DIFFICULTIES, AUTHORS, LANG_FILE
from settings.storage import load_balance, fmt_money
from settings.lang import LANGUAGES, t
from game.engine import GameSession
from answers.answers import AnswerButtons

BG       = "#06060f"
BG2      = "#0c0c22"
CARD     = "#0e1640"
GOLD     = "#f5c518"
GOLD_DIM = "#c9a100"
BLUE     = "#1a4fff"
TEXT     = "#e8eeff"
TEXT_DIM = "#7090b0"
GREEN    = "#22c55e"
RED      = "#ef4444"
PURPLE   = "#a78bfa"

def load_lang():
    try:
        with open(LANG_FILE) as f:
            return json.load(f).get("lang", "ru")
    except Exception:
        return "ru"

def save_lang(lang):
    os.makedirs(os.path.dirname(LANG_FILE), exist_ok=True)
    with open(LANG_FILE, "w") as f:
        json.dump({"lang": lang}, f)

def styled_btn(parent, text, command, color=GOLD, width=22, font_size=13):
    btn = tk.Button(
        parent, text=text, command=command,
        font=("Segoe UI", font_size, "bold"),
        fg=BG, bg=color, activebackground=GOLD_DIM,
        activeforeground=BG, relief="flat", bd=0,
        cursor="hand2", width=width, pady=10,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=GOLD_DIM))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

def sep(parent):
    f = tk.Frame(parent, bg=GOLD, height=1)
    f.pack(fill="x", padx=40, pady=8)
    return f

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = load_lang()
        self.configure(bg=BG)
        self.geometry("900x660")
        self.minsize(800, 580)
        self.resizable(True, True)
        self._update_title()
        self.session = None
        self._answer_btns = None
        self._frame = None
        self.show_menu()

    def _T(self, key):
        return t(self.lang, key)

    def _update_title(self):
        self.title(f"{self._T('title_top')} {self._T('title_main')}")

    def _switch(self, new_frame):
        if self._frame:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

    # ── ГЛАВНОЕ МЕНЮ ──────────────────────────────────────────
    def show_menu(self):
        self._update_title()
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        outer = tk.Frame(f, bg=GOLD)
        outer.place(relx=0.5, rely=0.5, anchor="center", width=540, height=480)
        inner = tk.Frame(outer, bg=BG, padx=2, pady=2)
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(inner, text=self._T("title_top"), font=("Segoe UI", 15, "bold"),
                 fg=GOLD_DIM, bg=BG).pack(pady=(28, 0))
        tk.Label(inner, text=self._T("title_main"), font=("Segoe UI", 26, "bold"),
                 fg=GOLD, bg=BG).pack(pady=(0, 4))

        bal = load_balance()
        tk.Label(inner, text=f"{self._T('balance')}: {fmt_money(bal)}",
                 font=("Courier New", 13, "bold"), fg=GREEN, bg=BG).pack(pady=4)

        sep(inner)

        btn_frame = tk.Frame(inner, bg=BG)
        btn_frame.pack(pady=10)

        styled_btn(btn_frame, self._T("btn_start"),    self.show_difficulty, width=26).pack(pady=6)
        styled_btn(btn_frame, self._T("btn_authors"),  self.show_authors,    color="#4488ff", width=26).pack(pady=6)
        styled_btn(btn_frame, self._T("btn_language"), self.show_language,   color=PURPLE, width=26).pack(pady=6)
        styled_btn(btn_frame, self._T("btn_quit"),     self.quit,            color="#555", width=26).pack(pady=6)

    # ── ВЫБОР ЯЗЫКА ───────────────────────────────────────────
    def show_language(self):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        tk.Label(f, text="", bg=BG).pack(expand=True)
        tk.Label(f, text=self._T("choose_language"), font=("Segoe UI", 22, "bold"),
                 fg=GOLD, bg=BG).pack(pady=(0, 10))
        sep(f)

        cards = tk.Frame(f, bg=BG)
        cards.pack(pady=10)

        for code, name in LANGUAGES.items():
            is_active = (code == self.lang)
            bg_c   = "#1a2a6a" if is_active else "#111827"
            border = GOLD if is_active else "#334"
            row = tk.Frame(cards, bg=bg_c, highlightbackground=border, highlightthickness=2)
            row.pack(fill="x", padx=120, pady=5, ipady=4)

            tk.Label(row, text=name, font=("Segoe UI", 14, "bold"),
                     fg=GOLD if is_active else TEXT,
                     bg=bg_c, width=30, anchor="w", padx=16).pack(side="left")

            if is_active:
                tk.Label(row, text="✔", font=("Segoe UI", 14, "bold"),
                         fg=GREEN, bg=bg_c, padx=12).pack(side="right")
            else:
                def make_cmd(c=code):
                    def cmd():
                        self.lang = c
                        save_lang(c)
                        self.show_language()
                    return cmd
                tk.Button(row, text="✔", font=("Segoe UI", 11, "bold"),
                          fg=BG, bg=GOLD, activebackground=GOLD_DIM,
                          relief="flat", bd=0, cursor="hand2", padx=14, pady=4,
                          command=make_cmd()).pack(side="right", padx=10)

        tk.Label(f, text="", bg=BG).pack(expand=True)
        sep(f)
        styled_btn(f, self._T("btn_back"), self.show_menu, color="#444", width=18).pack(pady=14)

    # ── ВЫБОР СЛОЖНОСТИ ───────────────────────────────────────
    def show_difficulty(self):
        f = tk.Frame(self, bg=BG)
        self._switch(f)
        bal = load_balance()

        tk.Label(f, text=self._T("difficulty_title"), font=("Segoe UI", 22, "bold"),
                 fg=GOLD, bg=BG).pack(pady=(40, 4))
        tk.Label(f, text=f"{self._T('balance')}: {fmt_money(bal)}",
                 font=("Courier New", 12, "bold"), fg=GREEN, bg=BG).pack(pady=(0, 16))
        sep(f)

        cards_frame = tk.Frame(f, bg=BG)
        cards_frame.pack(pady=10)

        for diff in ["easy", "medium", "hard", "infinite"]:
            cfg = DIFFICULTIES[diff]
            locked = bal < cfg["unlock"]
            self._diff_card(cards_frame, diff, cfg, locked)

        sep(f)
        styled_btn(f, self._T("btn_back"), self.show_menu, color="#444", width=18).pack(pady=12)

    def _diff_card(self, parent, diff, cfg, locked):
        color = cfg["color"]
        bg_c  = "#1a1a3a" if not locked else "#111"
        fg_c  = color if not locked else "#444"
        name  = self._T(cfg["diff_key"])

        card = tk.Frame(parent, bg=bg_c,
                        highlightbackground=color if not locked else "#333",
                        highlightthickness=2, padx=16, pady=10)
        card.pack(fill="x", padx=40, pady=5)

        row = tk.Frame(card, bg=bg_c)
        row.pack(fill="x")

        tk.Label(row, text=name, font=("Segoe UI", 14, "bold"),
                 fg=fg_c, bg=bg_c, width=20, anchor="w").pack(side="left")

        q_lbl = self._T("questions_lbl")
        if diff != "infinite":
            info = f"{cfg['questions']} {q_lbl}  |  +{fmt_money(cfg['reward'])}  |  {self._T('hearts_lbl')} {cfg['lives']}"
        else:
            info = f"∞  |  {self._T('mixed')}  |  {self._T('hearts_lbl')} {cfg['lives']}"

        tk.Label(row, text=info, font=("Segoe UI", 10),
                 fg=TEXT_DIM if not locked else "#333", bg=bg_c).pack(side="left", padx=8)

        if locked:
            tk.Label(row, text=f"{self._T('locked')} {fmt_money(cfg['unlock'])}",
                     font=("Segoe UI", 10, "bold"), fg=RED, bg=bg_c).pack(side="right", padx=6)
        else:
            tk.Button(row, text=self._T("btn_play"),
                      font=("Segoe UI", 10, "bold"),
                      fg=BG, bg=color, activebackground=GOLD_DIM,
                      relief="flat", bd=0, cursor="hand2", padx=10, pady=4,
                      command=lambda d=diff: self.start_game(d)).pack(side="right", padx=6)

    # ── ИГРА ──────────────────────────────────────────────────
    def start_game(self, difficulty):
        self.session = GameSession(difficulty, lang=self.lang)
        self._show_game_screen()

    def _show_game_screen(self):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        hud = tk.Frame(f, bg=BG2, pady=8)
        hud.pack(fill="x")

        self._lbl_balance = tk.Label(hud, text="", font=("Courier New", 14, "bold"), fg=GOLD, bg=BG2)
        self._lbl_balance.pack(side="left", padx=20)

        self._lbl_lives = tk.Label(hud, text="", font=("Segoe UI", 14, "bold"), fg=RED, bg=BG2)
        self._lbl_lives.pack(side="right", padx=20)

        self._lbl_progress = tk.Label(hud, text="", font=("Segoe UI", 11), fg=TEXT_DIM, bg=BG2)
        self._lbl_progress.pack(side="right", padx=20)

        q_frame = tk.Frame(f, bg=CARD, highlightbackground=GOLD_DIM, highlightthickness=1)
        q_frame.pack(fill="x", padx=30, pady=(18, 8))

        self._lbl_qnum = tk.Label(q_frame, text="", font=("Segoe UI", 10), fg=GOLD_DIM, bg=CARD, anchor="w")
        self._lbl_qnum.pack(fill="x", padx=16, pady=(10, 0))

        self._lbl_question = tk.Label(q_frame, text="", font=("Segoe UI", 15, "bold"),
                                      fg=TEXT, bg=CARD, wraplength=820, justify="center", pady=10)
        self._lbl_question.pack(fill="x", padx=16, pady=(4, 14))

        a_frame = tk.Frame(f, bg=BG)
        a_frame.pack(fill="both", expand=True, padx=30, pady=4)
        self._answer_btns = AnswerButtons(a_frame)

        bot = tk.Frame(f, bg=BG2, pady=8)
        bot.pack(fill="x", side="bottom")

        styled_btn(bot, self._T("btn_exit_save"), self._exit_save,
                   color="#226622", width=28, font_size=11).pack(side="left", padx=20)

        self._lbl_reward_flash = tk.Label(bot, text="", font=("Courier New", 13, "bold"), fg=GREEN, bg=BG2)
        self._lbl_reward_flash.pack(side="right", padx=20)

        self._update_hud()
        self._load_question()

    def _update_hud(self):
        s = self.session
        self._lbl_balance.config(text=f"💵  {fmt_money(load_balance())}")
        hearts = "❤ " * s.lives + "♡ " * max(0, DIFFICULTIES[s.difficulty]["lives"] - s.lives)
        self._lbl_lives.config(text=hearts.strip())
        total = s.total_questions or "∞"
        self._lbl_progress.config(text=self._T("question_of").format(s.index + 1, total))

    def _load_question(self):
        s = self.session
        q = s.current_question
        if q is None:
            self._victory()
            return
        total = s.total_questions or "∞"
        self._lbl_qnum.config(text=self._T("question_of").format(s.index + 1, total))
        self._lbl_question.config(text=q["q"])
        self._answer_btns.load(q["a"], q["correct"], self._on_answer)
        self._lbl_reward_flash.config(text="")

    def _on_answer(self, correct):
        result = self.session.answer(correct)
        status = result["status"]

        if status == "correct":
            self._lbl_reward_flash.config(text=f"+{fmt_money(result['reward'])} ✔", fg=GREEN)
            self._update_hud()
            self.after(1600, self._load_question)

        elif status == "wrong_continue":
            self._lbl_reward_flash.config(
                text=self._T("wrong_lives").format(self.session.lives), fg=RED)
            self._update_hud()
            self.after(1600, self._load_question)

        elif status == "game_over":
            self.after(800, lambda: self._game_over(result["lost"]))

        elif status == "victory":
            self.after(800, lambda: self._victory(result))

    def _exit_save(self):
        self.session.exit_save()
        self.show_menu()

    # ── GAME OVER ─────────────────────────────────────────────
    def _game_over(self, lost):
        f = tk.Frame(self, bg="black")
        self._switch(f)

        tk.Label(f, text="", bg="black").pack(expand=True)
        tk.Label(f, text=self._T("game_over"), font=("Segoe UI", 52, "bold"), fg=RED, bg="black").pack()
        tk.Label(f, text=self._T("lost_text").format(fmt_money(lost)),
                 font=("Segoe UI", 16), fg=TEXT_DIM, bg="black").pack(pady=12)
        tk.Label(f, text="", bg="black").pack(expand=True)

        btn_f = tk.Frame(f, bg="black")
        btn_f.pack(pady=20)
        styled_btn(btn_f, self._T("btn_restart"), self.show_menu, color=RED,  width=22).pack(pady=8)
        styled_btn(btn_f, self._T("btn_exit"),    self.quit,      color="#444", width=22).pack(pady=8)

    # ── ПОБЕДА ────────────────────────────────────────────────
    def _victory(self, result=None):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        tk.Label(f, text="", bg=BG).pack(expand=True)
        tk.Label(f, text=self._T("victory_title"), font=("Segoe UI", 36, "bold"), fg=GOLD, bg=BG).pack()

        if result:
            tk.Label(f, text=self._T("session_earned").format(fmt_money(result.get("session", 0))),
                     font=("Segoe UI", 15), fg=GREEN, bg=BG).pack(pady=6)

        bal = load_balance()
        tk.Label(f, text=self._T("total_balance").format(fmt_money(bal)),
                 font=("Courier New", 18, "bold"), fg=GOLD, bg=BG).pack(pady=10)
        tk.Label(f, text="", bg=BG).pack(expand=True)

        btn_f = tk.Frame(f, bg=BG)
        btn_f.pack(pady=20)
        styled_btn(btn_f, self._T("btn_play_more"), self.show_difficulty, width=24).pack(pady=8)
        styled_btn(btn_f, self._T("btn_main_menu"), self.show_menu, color="#4488ff", width=24).pack(pady=8)

    # ── АВТОРЫ ────────────────────────────────────────────────
    def show_authors(self):
        f = tk.Frame(self, bg=BG)
        self._switch(f)

        tk.Label(f, text="", bg=BG).pack(expand=True)
        tk.Label(f, text=self._T("authors_title"), font=("Segoe UI", 26, "bold"),
                 fg=GOLD, bg=BG).pack(pady=(0, 16))
        sep(f)

        for name, role in AUTHORS:
            row = tk.Frame(f, bg=CARD, highlightbackground=GOLD_DIM, highlightthickness=1)
            row.pack(fill="x", padx=120, pady=5)
            tk.Label(row, text=name, font=("Segoe UI", 14, "bold"),
                     fg=TEXT, bg=CARD, width=26, anchor="w", padx=16, pady=10).pack(side="left")
            tk.Label(row, text=role, font=("Segoe UI", 12),
                     fg=TEXT_DIM, bg=CARD, padx=16).pack(side="right")

        tk.Label(f, text="", bg=BG).pack(expand=True)
        sep(f)
        styled_btn(f, self._T("btn_back"), self.show_menu, color="#444", width=18).pack(pady=16)


if __name__ == "__main__":
    app = App()
    app.mainloop()
