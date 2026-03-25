"""
Игровой движок — управляет состоянием сессии.
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from questions.questions import get_questions, get_infinite_questions
from settings.config import DIFFICULTIES, INFINITE_REWARDS
from settings.storage import load_balance, add_balance, reset_balance, fmt_money


def _shuffle(lst):
    out = list(lst)
    random.shuffle(out)
    return out


class GameSession:
    def __init__(self, difficulty: str, lang: str = "ru"):
        self.difficulty = difficulty
        self.lang = lang
        cfg = DIFFICULTIES[difficulty]
        self.lives = cfg["lives"]
        self.session_earned = 0
        self.index = 0

        if difficulty == "infinite":
            self._pool = _shuffle(get_infinite_questions(lang))
        else:
            self._pool = _shuffle(get_questions(lang, difficulty))

    @property
    def current_question(self):
        if self.difficulty == "infinite":
            while self.index >= len(self._pool):
                self._pool += _shuffle(get_infinite_questions(self.lang))
            return self._pool[self.index]
        if self.index >= len(self._pool):
            return None
        return self._pool[self.index]

    @property
    def total_questions(self):
        return DIFFICULTIES[self.difficulty]["questions"]

    @property
    def balance(self):
        return load_balance()

    def answer(self, correct: bool) -> dict:
        q = self.current_question

        if correct:
            reward = self._get_reward(q)
            self.session_earned += reward
            add_balance(reward)
            self.index += 1

            if self.total_questions and self.index >= self.total_questions:
                return {"status": "victory",
                        "reward": reward,
                        "session": self.session_earned,
                        "balance": load_balance()}
            return {"status": "correct", "reward": reward, "balance": load_balance()}
        else:
            self.lives -= 1
            self.index += 1
            if self.lives <= 0:
                lost = load_balance()
                reset_balance()
                return {"status": "game_over", "lost": lost}
            return {"status": "wrong_continue", "balance": load_balance()}

    def exit_save(self) -> int:
        return load_balance()

    def _get_reward(self, q) -> int:
        if self.difficulty == "infinite":
            return INFINITE_REWARDS[q.get("diff", "easy")]
        return DIFFICULTIES[self.difficulty]["reward"]