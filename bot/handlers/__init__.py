from aiogram import Router

from bot.handlers.start import router as start_router
from bot.handlers.menu import router as menu_router
from bot.handlers.admin import router as admin_router

main_router = Router(name="main")
main_router.include_routers(start_router, menu_router, admin_router)
