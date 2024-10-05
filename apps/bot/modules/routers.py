from aiogram import Dispatcher

from .main.handlers import main_router

dp = Dispatcher()

dp.include_router(main_router)
# dp.include_router(progress_router)
