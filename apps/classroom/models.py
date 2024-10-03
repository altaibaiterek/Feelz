from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils.translation import gettext_lazy as _

from django.db import models

from apps.bot.models import Base


class DayOfWeek(Base):
    DAYS_OF_WEEK = [
        (1, _('Понедельник')),
        (2, _('Вторник')),
        (3, _('Среда')),
        (4, _('Четверг')),
        (5, _('Пятница')),
        (6, _('Суббота')),
        (7, _('Воскресенье')),
    ]
    
    id = models.PositiveSmallIntegerField(
        choices=DAYS_OF_WEEK, 
        primary_key=True,
        unique=True,
        default=1,
        verbose_name=_('День'),
        help_text=_('День недели'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(7)
                    ]
        )

    def __str__(self):
        return f'{dict(self.DAYS_OF_WEEK)[self.id]}'
    
    class Meta:
        ordering = ['id']
        verbose_name = _('День недели')
        verbose_name_plural = _('Дни недели')


class ClassRoom(Base):
    name = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name=_("Название"),
        help_text=_('Название кабинета')
        )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание'),
        help_text=_('Описание кабинета'),
        )
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Кабинет')
        verbose_name_plural = _('Кабинеты')


class ClassSchedule(Base):
    name = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name=_("Название"),
        help_text=_('Название расписания')
        )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание'),
        help_text=_('Описание расписания'),
        ) 
    days = models.ManyToManyField(
        DayOfWeek,
        related_name='schedules',
        blank=True,
        verbose_name=_("Дни"),
        help_text=_("Дни недели"),
        )
    
    def __str__(self):
        return f'{self.name} ({self.days})'
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Расписание')
        verbose_name_plural = _('Расписания')
    
    
class ClassTime(Base):
    name = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name=_("Название"),
        help_text=_('Название временного отрезка')
        )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание'),
        help_text=_('Описание временного отрезка'),
        )
    start_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_('Начало'),
        help_text=_('Начало занятия'),
    )
    end_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_('Конец'),
        help_text=_('Конец занятия'),
    )

    def __str__(self):
        return f'{self.name} ({self.start_time}:{self.end_time})'
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Время занятия')
        verbose_name_plural = _('Время занятий')

