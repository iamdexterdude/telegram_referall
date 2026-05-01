"""
main.py — Application entry point for Referral Bot v2.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.database import init_db
from bot.handlers import main_router
from bot.middlewares import BanCheckMiddleware, DbSessionMiddleware
from config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Initialising database …")
    await init_db()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware order matters: DB first, then ban check
    dp.update.middleware(DbSessionMiddleware())
    dp.update.middleware(BanCheckMiddleware())

    dp.include_router(main_router)

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot is running → @%s", config.bot_username)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
