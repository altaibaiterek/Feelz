from django.utils.translation import gettext_lazy as _

from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account"
    verbose_name = _('Студенты и группы')
