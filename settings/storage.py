import json, os
from settings.config import SAVE_FILE

def load_balance() -> int:
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE) as f:
                return int(json.load(f).get("balance", 0))
        except Exception:
            pass
    return 0

def save_balance(amount: int):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump({"balance": amount}, f)

def add_balance(amount: int) -> int:
    new = load_balance() + amount
    save_balance(new)
    return new

def reset_balance():
    save_balance(0)

def fmt_money(amount: int) -> str:
    """$1,000,000"""
    return f"${amount:,}".replace(",", " ")
