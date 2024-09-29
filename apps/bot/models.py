from django.utils.translation import gettext_lazy as _

from django.db import models


class Base(models.Model):
    """
    Базовый абстрактный класс, содержащий общие поля и настройки для всех моделей.
    Поля включают время создания и обновления записей.

    Атрибуты:
        created_at (DateTimeField): Дата и время создания записи.
        updated_at (DateTimeField): Дата и время последнего обновления записи.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Дата и время создания"),
        verbose_name=_("Дата создания"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("Дата и время последнего обновления"),
        verbose_name=_("Дата последнего обновления"),
    )

    def __str__(self):
        return f'{self.__class__.__name__} (ID: {self.id})'

    class Meta:
        abstract = True
        ordering = ("-created_at",)
