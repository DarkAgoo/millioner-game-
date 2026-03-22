"""
База вопросов по языкам.
Структура: QUESTIONS[язык][сложность][список вопросов]

Языки: uk, ru, en, fr, de
Сложности: easy (10), medium (20), hard (30)

correct: индекс правильного ответа (0=A, 1=B, 2=C, 3=D)
"""

def _default(label, count):
    """Генерирует placeholder-вопросы для заданной метки и количества."""
    return [
        {"q": f"Default Text — {label} {i}?",
         "a": ["Default A", "Default B", "Default C", "Default D"],
         "correct": (i - 1) % 4}
        for i in range(1, count + 1)
    ]

QUESTIONS = {

    # ── УКРАИНСКИЙ ───────────────────────────────────────────
    "uk": {
        "easy":   _default("Легке питання", 10),
        "medium": _default("Середнє питання", 20),
        "hard":   _default("Важке питання", 30),
    },

    # ── РУССКИЙ ──────────────────────────────────────────────
    "ru": {
        "easy":   _default("Лёгкий вопрос", 10),
        "medium": _default("Средний вопрос", 20),
        "hard":   _default("Сложный вопрос", 30),
    },

    # ── ENGLISH ──────────────────────────────────────────────
    "en": {
        "easy":   _default("Easy question", 10),
        "medium": _default("Medium question", 20),
        "hard":   _default("Hard question", 30),
    },

    # ── FRANÇAIS ─────────────────────────────────────────────
    "fr": {
        "easy":   _default("Question facile", 10),
        "medium": _default("Question moyenne", 20),
        "hard":   _default("Question difficile", 30),
    },

    # ── DEUTSCH ──────────────────────────────────────────────
    "de": {
        "easy":   _default("Leichte Frage", 10),
        "medium": _default("Mittlere Frage", 20),
        "hard":   _default("Schwere Frage", 30),
    },
}


def get_questions(lang: str, difficulty: str) -> list:
    """Возвращает вопросы для нужного языка и сложности.
    Если язык не найден — возвращает русские вопросы."""
    lang_q = QUESTIONS.get(lang, QUESTIONS["ru"])
    return list(lang_q.get(difficulty, []))
