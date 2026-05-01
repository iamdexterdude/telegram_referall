"""
bot/middlewares/ban_check.py — Silently blocks banned users from all interactions.
"""
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from bot.services.user_service import get_user


class BanCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session = data.get("session")
        if not session:
            return await handler(event, data)

        # Extract user from update
        user = None
        if isinstance(event, Update):
            if event.message:
                user = event.message.from_user
            elif event.callback_query:
                user = event.callback_query.from_user

        if user:
            db_user = await get_user(session, user.id)
            if db_user and db_user.is_banned:
                # Optionally notify the user once
                if isinstance(event, Update) and event.message:
                    from bot.locales.translations import t
                    await event.message.answer(t(db_user.language, "banned"))
                return  # Block further processing

        return await handler(event, data)
