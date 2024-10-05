from aiogram import Dispatcher

from .main.handlers import main_router
from .progress.handlers import progress_router
from .managment.handlers import managment_router

dp = Dispatcher()

dp.include_router(main_router)
dp.include_router(progress_router)
dp.include_router(managment_router)


