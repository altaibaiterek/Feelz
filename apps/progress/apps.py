from django.utils.translation import gettext_lazy as _

from django.apps import AppConfig


class ProgressConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.progress"
    verbose_name = _('Прогресс студентов')
