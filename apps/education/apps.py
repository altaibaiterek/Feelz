from django.utils.translation import gettext_lazy as _

from django.apps import AppConfig


class EducationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.education"
    verbose_name = _('Успеваемость')
