from django.core.management.base import BaseCommand

import asyncio

from apps.bot.config import start_bot


class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **kwargs):
        asyncio.run(start_bot())
