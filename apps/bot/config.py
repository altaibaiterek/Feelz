import locale
import logging

from decouple import config
from aiogram import Bot, Dispatcher

from aiogram.methods import DeleteWebhook
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from apps.bot.handlers import main_router, group_router, lesson_router, attendance_router, education_router


locale.setlocale(
    locale.LC_TIME, 'ru_RU.UTF-8'
)


dp = Dispatcher()
bot = Bot(
        token=config("BOT_TOKEN"),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )


dp.include_router(main_router)
dp.include_router(group_router)
dp.include_router(lesson_router)
dp.include_router(attendance_router)
dp.include_router(education_router)


async def start_bot() -> None:
    logging.basicConfig(level=logging.INFO)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)
