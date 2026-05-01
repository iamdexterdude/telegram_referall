"""
config.py — Central configuration loaded from .env
"""
import os
from dataclasses import dataclass, field
from typing import List

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable '{name}' is not set.")
    return value


@dataclass(frozen=True)
class Config:
    bot_token: str = field(default_factory=lambda: _require("BOT_TOKEN"))
    bot_username: str = field(default_factory=lambda: _require("BOT_USERNAME"))
    channel_id: str = field(default_factory=lambda: _require("CHANNEL_ID"))
    database_url: str = field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL", "sqlite+aiosqlite:///./referral_bot.db"
        )
    )
    leaderboard_limit: int = field(
        default_factory=lambda: int(os.getenv("LEADERBOARD_LIMIT", "10"))
    )
    admin_ids: List[int] = field(
        default_factory=lambda: [
            int(x.strip())
            for x in os.getenv("ADMIN_IDS", "").split(",")
            if x.strip().isdigit()
        ]
    )
    welcome_image_url: str = field(
        default_factory=lambda: os.getenv("WELCOME_IMAGE_URL", "")
    )


# Reward milestone definitions: (referral_count, badge_emoji, badge_name)
MILESTONES = [
    (5,  "🥉", "Bronze"),
    (15, "🥈", "Silver"),
    (30, "🥇", "Gold"),
    (50, "💎", "Diamond"),
]


def get_badge(referral_count: int) -> str:
    """Return the highest earned badge for a given referral count."""
    badge = ""
    for threshold, emoji, name in MILESTONES:
        if referral_count >= threshold:
            badge = f"{emoji} {name}"
    return badge


def next_milestone(referral_count: int):
    """Return (needed, emoji, name) for the next milestone, or None if maxed."""
    for threshold, emoji, name in MILESTONES:
        if referral_count < threshold:
            return threshold - referral_count, emoji, name
    return None


config = Config()
