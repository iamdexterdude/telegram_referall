"""
bot/keyboards/keyboards.py — All keyboards (inline + reply), language-aware.
"""
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.locales.translations import t

remove_keyboard = ReplyKeyboardRemove()


# ── Language selection ────────────────────────────────────────────────────────

def language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang:uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
    )
    return builder.as_markup()


# ── Main menu (reply keyboard) ────────────────────────────────────────────────

def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(lang, "btn_link")),
                KeyboardButton(text=t(lang, "btn_stats")),
            ],
            [
                KeyboardButton(text=t(lang, "btn_top")),
                KeyboardButton(text=t(lang, "btn_help")),
            ],
            [
                KeyboardButton(text=t(lang, "btn_language")),
            ],
        ],
        resize_keyboard=True,
    )


# ── Request phone number ──────────────────────────────────────────────────────

def request_contact_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(
            text=t(lang, "share_phone_btn"),
            request_contact=True,
        )]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# ── Channel join verification ─────────────────────────────────────────────────

def join_verify_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(lang, "verify_btn"))]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# ── Referral link inline actions ──────────────────────────────────────────────

def referral_link_keyboard(lang: str, link: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📤 Share", switch_inline_query=link),
        InlineKeyboardButton(text="📱 QR Code", callback_data="get_qr"),
    )
    return builder.as_markup()


# ── Stats inline refresh ──────────────────────────────────────────────────────

def stats_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Refresh", callback_data="refresh_stats"),
        InlineKeyboardButton(text="📱 My QR", callback_data="get_qr"),
    )
    return builder.as_markup()


# ── Leaderboard inline refresh ────────────────────────────────────────────────

def leaderboard_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Refresh", callback_data="refresh_top"),
    )
    return builder.as_markup()
