import locale
import logging

from decouple import config
from aiogram import Bot

from aiogram.methods import DeleteWebhook
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from apps.bot.modules.routers import dp


locale.setlocale(
    locale.LC_TIME, 'ru_RU.UTF-8'
)


bot = Bot(
        token=config("BOT_TOKEN"),
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN
        )
    )


async def start_bot() -> None:
    logging.basicConfig(level=logging.INFO)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)
