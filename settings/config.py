# ============================================================
#  НАСТРОЙКИ ИГРЫ
# ============================================================

DIFFICULTIES = {
    "easy": {
        "questions": 10,
        "reward": 500_000,
        "lives": 3,
        "unlock": 0,
        "color": "#4ade80",
        "diff_key": "diff_easy",
    },
    "medium": {
        "questions": 20,
        "reward": 1_000_000,
        "lives": 2,
        "unlock": 5_000_000,
        "color": "#facc15",
        "diff_key": "diff_medium",
    },
    "hard": {
        "questions": 30,
        "reward": 2_500_000,
        "lives": 1,
        "unlock": 15_000_000,
        "color": "#f87171",
        "diff_key": "diff_hard",
    },
    "infinite": {
        "questions": None,   # бесконечно
        "reward": None,      # зависит от сложности вопроса
        "lives": 2,
        "unlock": 0,
        "color": "#a78bfa",
        "diff_key": "diff_infinite",
    },
}

# Награда в бесконечном режиме берётся из сложности вопроса:
INFINITE_REWARDS = {
    "easy":   500_000,
    "medium": 1_000_000,
    "hard":   2_500_000,
}

AUTHORS = [
    ("Главный разработчик", "Архитектура и движок"),
    ("Дизайнер игры",       "Механики и UI"),
    ("Автор вопросов",      "Вопросы и ответы"),
]

SAVE_FILE = "settings/save.json"
LANG_FILE = "settings/lang_save.json"
