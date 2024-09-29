from django.utils.translation import gettext_lazy as _

from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.attendance"
    verbose_name = _('Посещаемость')
