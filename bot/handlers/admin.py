"""
bot/handlers/admin.py — Admin commands: panel, broadcast, ban/unban, CSV export.
"""
from __future__ import annotations

import csv
import io
import logging
from datetime import datetime, timezone, timedelta

from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Referral, User
from bot.locales.translations import t
from bot.services.user_service import get_all_users, get_user, set_banned
from config import config

logger = logging.getLogger(__name__)
router = Router(name="admin")


def _is_admin(user_id: int) -> bool:
    return user_id in config.admin_ids


def _require_admin(func_):
    """Decorator: silently ignore non-admins."""
    import functools
    @functools.wraps(func_)
    async def wrapper(message: Message, *args, **kwargs):
        if not _is_admin(message.from_user.id):
            await message.answer(t("en", "not_admin"))
            return
        return await func_(message, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
#  /admin — dashboard
# ─────────────────────────────────────────────────────────────────────────────

@router.message(Command("admin"))
@_require_admin
async def cmd_admin(message: Message, session: AsyncSession, **_) -> None:
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    total_users = (await session.execute(select(func.count()).select_from(User))).scalar()
    total_referrals = (await session.execute(select(func.count()).select_from(Referral))).scalar()
    today_users = (
        await session.execute(
            select(func.count()).select_from(User).where(User.created_at >= today)
        )
    ).scalar()
    today_refs = (
        await session.execute(
            select(func.count()).select_from(Referral).where(Referral.created_at >= today)
        )
    ).scalar()

    await message.answer(
        t("en", "admin_panel",
          users=total_users,
          referrals=total_referrals,
          today_users=today_users,
          today_refs=today_refs),
        parse_mode="HTML",
    )


# ─────────────────────────────────────────────────────────────────────────────
#  /broadcast
# ─────────────────────────────────────────────────────────────────────────────

@router.message(Command("broadcast"))
@_require_admin
async def cmd_broadcast(message: Message, session: AsyncSession, **_) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(t("en", "broadcast_usage"))
        return

    text = parts[1]
    users = await get_all_users(session)
    sent = 0

    for user in users:
        try:
            await message.bot.send_message(
                chat_id=user.user_id,
                text=text,
                parse_mode="HTML",
            )
            sent += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            pass  # User blocked bot or deleted account

    await message.answer(t("en", "broadcast_done", count=sent))


# ─────────────────────────────────────────────────────────────────────────────
#  /ban and /unban
# ─────────────────────────────────────────────────────────────────────────────

@router.message(Command("ban"))
@_require_admin
async def cmd_ban(message: Message, session: AsyncSession, **_) -> None:
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer(t("en", "ban_usage"))
        return
    uid = int(parts[1])
    await set_banned(session, uid, True)
    await message.answer(t("en", "ban_done", user_id=uid))


@router.message(Command("unban"))
@_require_admin
async def cmd_unban(message: Message, session: AsyncSession, **_) -> None:
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer(t("en", "ban_usage"))
        return
    uid = int(parts[1])
    await set_banned(session, uid, False)
    await message.answer(t("en", "unban_done", user_id=uid))


# ─────────────────────────────────────────────────────────────────────────────
#  CSV exports
# ─────────────────────────────────────────────────────────────────────────────

@router.message(Command("export_users"))
@_require_admin
async def cmd_export_users(message: Message, session: AsyncSession, **_) -> None:
    result = await session.execute(select(User).order_by(User.created_at))
    users = result.scalars().all()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "id", "user_id", "username", "first_name", "last_name",
        "phone_number", "referral_code", "referral_count",
        "referred_by", "language", "is_banned", "link_clicks", "created_at"
    ])
    for u in users:
        writer.writerow([
            u.id, u.user_id, u.username, u.first_name, u.last_name,
            u.phone_number, u.referral_code, u.referral_count,
            u.referred_by, u.language, u.is_banned, u.link_clicks,
            u.created_at.isoformat(),
        ])

    filename = f"users_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
    await message.answer_document(
        BufferedInputFile(buf.getvalue().encode(), filename=filename),
        caption=f"📋 {len(users)} users exported.",
    )


@router.message(Command("export_referrals"))
@_require_admin
async def cmd_export_referrals(message: Message, session: AsyncSession, **_) -> None:
    result = await session.execute(select(Referral).order_by(Referral.created_at))
    referrals = result.scalars().all()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "referrer_id", "referred_user_id", "created_at"])
    for r in referrals:
        writer.writerow([r.id, r.referrer_id, r.referred_user_id, r.created_at.isoformat()])

    filename = f"referrals_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
    await message.answer_document(
        BufferedInputFile(buf.getvalue().encode(), filename=filename),
        caption=f"📋 {len(referrals)} referrals exported.",
    )
