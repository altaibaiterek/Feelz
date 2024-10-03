from django.utils.translation import gettext_lazy as _

from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bot"
    verbose_name = _('Управление ботом')
