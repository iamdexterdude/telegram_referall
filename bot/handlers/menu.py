"""
bot/handlers/menu.py — Main menu: referral link, stats, leaderboard, help, QR.
"""
from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.keyboards import (
    leaderboard_keyboard,
    main_menu_keyboard,
    referral_link_keyboard,
    stats_keyboard,
)
from bot.locales.translations import t
from bot.services.qr_service import generate_qr_bytes
from bot.services.user_service import get_leaderboard, get_user, get_user_rank
from bot.utils.helpers import build_referral_link
from config import config, get_badge, next_milestone

logger = logging.getLogger(__name__)
router = Router(name="menu")

MEDALS = ["🥇", "🥈", "🥉"]


# ─────────────────────────────────────────────────────────────────────────────
#  Guard helper
# ─────────────────────────────────────────────────────────────────────────────

async def _get_registered_user(message: Message, session: AsyncSession):
    user = await get_user(session, message.from_user.id)
    if not user:
        await message.answer(t("en", "not_registered"), parse_mode="HTML")
    return user


# ─────────────────────────────────────────────────────────────────────────────
#  Referral Link
# ─────────────────────────────────────────────────────────────────────────────

@router.message(F.text.in_(["🔗 Referal havola", "🔗 Реф. ссылка", "🔗 Referral Link"]))
@router.message(Command("link"))
async def show_referral_link(message: Message, session: AsyncSession) -> None:
    user = await _get_registered_user(message, session)
    if not user:
        return
    lang = user.language
    link = build_referral_link(config.bot_username, user.referral_code)
    await message.answer(
        t(lang, "your_link", link=link),
        reply_markup=referral_link_keyboard(lang, link),
        parse_mode="HTML",
    )


# ─────────────────────────────────────────────────────────────────────────────
#  QR Code (inline button callback)
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "get_qr")
async def cb_get_qr(callback: CallbackQuery, session: AsyncSession) -> None:
    user = await get_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Not registered.", show_alert=True)
        return

    link = build_referral_link(config.bot_username, user.referral_code)
    qr_bytes = generate_qr_bytes(link)

    await callback.message.answer_photo(
        photo=BufferedInputFile(qr_bytes, filename="referral_qr.png"),
        caption=t(user.language, "qr_caption", link=link),
        parse_mode="HTML",
    )
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
#  My Stats
# ─────────────────────────────────────────────────────────────────────────────

async def _build_stats_text(session: AsyncSession, user) -> str:
    lang = user.language
    link = build_referral_link(config.bot_username, user.referral_code)
    rank = await get_user_rank(session, user.user_id)
    badge = get_badge(user.referral_count) or "—"
    nxt = next_milestone(user.referral_count)

    if nxt:
        needed, emoji, name = nxt
        milestone_text = t(lang, "milestone_next", needed=needed, emoji=emoji, name=name)
    else:
        milestone_text = t(lang, "milestone_max")

    return t(
        lang, "stats",
        full_name=user.full_name(),
        username=f"@{user.username}" if user.username else "—",
        count=user.referral_count,
        badge=badge,
        rank=rank,
        date=user.created_at.strftime("%Y-%m-%d"),
        milestone_text=milestone_text,
        link=link,
    )


@router.message(F.text.in_(["📊 Mening natijalarim", "📊 Моя статистика", "📊 My Stats"]))
@router.message(Command("stats"))
async def show_stats(message: Message, session: AsyncSession) -> None:
    user = await _get_registered_user(message, session)
    if not user:
        return
    text = await _build_stats_text(session, user)
    await message.answer(
        text,
        reply_markup=stats_keyboard(user.language),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "refresh_stats")
async def cb_refresh_stats(callback: CallbackQuery, session: AsyncSession) -> None:
    user = await get_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Not registered.", show_alert=True)
        return
    text = await _build_stats_text(session, user)
    try:
        await callback.message.edit_text(
            text,
            reply_markup=stats_keyboard(user.language),
            parse_mode="HTML",
        )
    except Exception:
        pass  # Message unchanged — no edit needed
    await callback.answer("✅ Refreshed!")


# ─────────────────────────────────────────────────────────────────────────────
#  Top Referrers
# ─────────────────────────────────────────────────────────────────────────────

async def _build_leaderboard_text(session: AsyncSession, lang: str) -> str:
    leaders = await get_leaderboard(session, limit=config.leaderboard_limit)
    if not leaders:
        return t(lang, "top_empty")

    lines = [t(lang, "top_title")]
    for idx, u in enumerate(leaders, start=1):
        pos = MEDALS[idx - 1] if idx <= 3 else f"{idx}."
        display = f"@{u.username} ({u.full_name()})" if u.username else u.full_name()
        badge = get_badge(u.referral_count)
        lines.append(t(lang, "top_row", pos=pos, display=display, count=u.referral_count, badge=badge))

    return "\n".join(lines)


@router.message(F.text.in_(["🏆 Top referallar", "🏆 Топ рефералов", "🏆 Top Referrers"]))
@router.message(Command("top"))
async def show_top(message: Message, session: AsyncSession) -> None:
    user = await _get_registered_user(message, session)
    if not user:
        return
    text = await _build_leaderboard_text(session, user.language)
    await message.answer(
        text,
        reply_markup=leaderboard_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "refresh_top")
async def cb_refresh_top(callback: CallbackQuery, session: AsyncSession) -> None:
    user = await get_user(session, callback.from_user.id)
    lang = user.language if user else "en"
    text = await _build_leaderboard_text(session, lang)
    try:
        await callback.message.edit_text(
            text,
            reply_markup=leaderboard_keyboard(),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer("✅ Refreshed!")


# ─────────────────────────────────────────────────────────────────────────────
#  Help
# ─────────────────────────────────────────────────────────────────────────────

@router.message(F.text.in_(["❓ Yordam", "❓ Помощь", "❓ Help"]))
@router.message(Command("help"))
async def show_help(message: Message, session: AsyncSession) -> None:
    user = await get_user(session, message.from_user.id)
    lang = user.language if user else "en"
    await message.answer(t(lang, "help"), parse_mode="HTML")
