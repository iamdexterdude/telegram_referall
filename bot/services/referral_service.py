"""
bot/services/referral_service.py — Referral tracking, channel checks, notifications.
"""
from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Referral
from bot.services.user_service import get_user, increment_referral_count
from config import MILESTONES, get_badge, next_milestone
from bot.locales.translations import t

logger = logging.getLogger(__name__)


async def is_member_of_channel(bot: Bot, channel_id: str, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except (TelegramBadRequest, TelegramForbiddenError) as exc:
        logger.warning("Channel check failed for %s: %s", user_id, exc)
        return False


async def referral_already_exists(session: AsyncSession, referred_user_id: int) -> bool:
    result = await session.execute(
        select(Referral).where(Referral.referred_user_id == referred_user_id)
    )
    return result.scalar_one_or_none() is not None


async def confirm_referral(
    session: AsyncSession,
    bot: Bot,
    *,
    referrer_id: int,
    referred_user_id: int,
    referred_name: str,
) -> bool:
    """
    Insert referral row, increment counter, send real-time notification to referrer.
    Returns True on success, False if duplicate.
    """
    if referrer_id == referred_user_id:
        return False

    referral = Referral(referrer_id=referrer_id, referred_user_id=referred_user_id)
    session.add(referral)
    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        return False

    # Atomically increment and get new total
    new_total = await increment_referral_count(session, referrer_id)
    await session.commit()

    # ── Send real-time notification to referrer ──────────────────────────
    referrer = await get_user(session, referrer_id)
    if referrer:
        lang = referrer.language
        badge = get_badge(new_total)
        prev_total = new_total - 1

        try:
            await bot.send_message(
                chat_id=referrer_id,
                text=t(lang, "notif_new_referral",
                       name=referred_name,
                       total=new_total,
                       badge=badge),
                parse_mode="HTML",
            )

            # ── Milestone notification ───────────────────────────────────
            for threshold, emoji, name in MILESTONES:
                if prev_total < threshold <= new_total:
                    await bot.send_message(
                        chat_id=referrer_id,
                        text=t(lang, "milestone_reached", emoji=emoji, name=name),
                        parse_mode="HTML",
                    )
                    break

        except (TelegramForbiddenError, TelegramBadRequest):
            pass  # User blocked the bot — silently ignore

    logger.info("Referral confirmed: %s → %s (total=%s)", referrer_id, referred_user_id, new_total)
    return True
