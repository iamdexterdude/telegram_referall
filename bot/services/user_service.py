"""
bot/services/user_service.py — User business logic.
"""
from __future__ import annotations

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User
from bot.utils.helpers import generate_referral_code


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_code(session: AsyncSession, code: str) -> User | None:
    result = await session.execute(select(User).where(User.referral_code == code))
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    *,
    user_id: int,
    username: str | None,
    first_name: str,
    last_name: str | None = None,
    phone_number: str | None = None,
    referred_by: int | None = None,
    language: str = "en",
) -> User:
    # Guard: if user already exists (FSM glitch), just return existing user
    existing = await get_user(session, user_id)
    if existing:
        return existing

    for _ in range(10):
        code = generate_referral_code()
        if not await get_user_by_code(session, code):
            break
    else:
        raise RuntimeError("Could not generate unique referral code.")

    user = User(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        referral_code=code,
        referral_count=0,
        referred_by=referred_by,
        language=language,
        is_banned=False,
        link_clicks=0,
    )
    session.add(user)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        # Another concurrent insert beat us — fetch and return that user
        existing = await get_user(session, user_id)
        if existing:
            return existing
        raise
    await session.refresh(user)
    return user


async def update_language(session: AsyncSession, user_id: int, language: str) -> None:
    await session.execute(
        update(User).where(User.user_id == user_id).values(language=language)
    )
    await session.commit()


async def increment_referral_count(session: AsyncSession, referrer_id: int) -> int:
    """Atomically increment and return new count."""
    await session.execute(
        update(User)
        .where(User.user_id == referrer_id)
        .values(referral_count=User.referral_count + 1)
    )
    await session.commit()
    result = await session.execute(
        select(User.referral_count).where(User.user_id == referrer_id)
    )
    return result.scalar_one()


async def get_user_rank(session: AsyncSession, user_id: int) -> int:
    """Return the 1-based rank of a user by referral_count."""
    result = await session.execute(
        select(func.count()).select_from(User).where(
            User.referral_count > select(User.referral_count)
            .where(User.user_id == user_id)
            .scalar_subquery()
        )
    )
    return (result.scalar() or 0) + 1


async def get_leaderboard(session: AsyncSession, limit: int = 10) -> list[User]:
    result = await session.execute(
        select(User)
        .where(User.referral_count > 0, User.is_banned == False)
        .order_by(User.referral_count.desc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(
        select(User).where(User.is_banned == False)
    )
    return list(result.scalars().all())


async def set_banned(session: AsyncSession, user_id: int, banned: bool) -> None:
    await session.execute(
        update(User).where(User.user_id == user_id).values(is_banned=banned)
    )
    await session.commit()


async def increment_link_clicks(session: AsyncSession, user_id: int) -> None:
    await session.execute(
        update(User)
        .where(User.user_id == user_id)
        .values(link_clicks=User.link_clicks + 1)
    )
    await session.commit()
