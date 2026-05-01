"""
bot/utils/helpers.py — Pure utility functions.
"""
import random
import secrets
import string

_CODE_ALPHABET = string.ascii_letters + string.digits
_CODE_LENGTH = 8


def generate_referral_code() -> str:
    return "".join(secrets.choice(_CODE_ALPHABET) for _ in range(_CODE_LENGTH))


def build_referral_link(bot_username: str, referral_code: str) -> str:
    return f"https://t.me/{bot_username}?start={referral_code}"


def generate_captcha() -> tuple[int, int, int]:
    """Return (a, b, answer) for a simple addition captcha."""
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    return a, b, a + b
