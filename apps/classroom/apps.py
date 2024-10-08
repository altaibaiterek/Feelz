from django.utils.translation import gettext_lazy as _

from django.apps import AppConfig


class ClassroomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.classroom"
    verbose_name = _('Организация расписания')

    def ready(self):
        import apps.classroom.signals
