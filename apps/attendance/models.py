from django.utils.translation import gettext_lazy as _

from django.db import models

from apps.bot.models import Base

from apps.account.models import Student

from apps.education.models import Lesson, Task, Attendance


class StudentTask(Base):
    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Задание'),
        help_text=_('Задание, которое выполняет студент')
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Студент'),
        help_text=_('Студент, выполняющий задание')
    )
    body = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Ответ'),
        help_text=_('Ответ студента на задание')
    )

    def __str__(self):
        return f'Задание {self.task} - Студент {self.student}'

    class Meta:
        ordering = ['student', 'task']
        verbose_name = _('Задание студента')
        verbose_name_plural = _('Задания студентов')


class StudentAttendance(Base):
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Студент'),
        help_text=_('Студент, чья посещаемость фиксируется')
    )
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Отчет посещаемости'),
        help_text=_('Отчет посещаемости, для которого фиксируется студент')
    )
    skipped = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        verbose_name=_('Пропущено'),
        help_text=_('Студент пропустил занятие')
    )
    late = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name=_('Опоздание'),
        help_text=_('Количество минут опоздания')
    )

    def __str__(self):
        return f'Посещаемость {self.student} на занятии {self.attendance}'

    class Meta:
        ordering = ['student', 'attendance']
        verbose_name = _('Посещаемость студента')
        verbose_name_plural = _('Посещаемость студентов')
