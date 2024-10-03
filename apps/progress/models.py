from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils.translation import gettext_lazy as _

from django.db import models

from apps.bot.models import Base

from apps.account.models import Student

from apps.education.models import Task, Attendance


class StudentTask(Base):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_('Задание'),
        help_text=_('Задание, которое выполняет студент')
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name=_('Студент'),
        help_text=_('Студент, выполняющий задание')
    )
    passed = models.BooleanField(
        default=False,
        verbose_name=_('Сдал'),
        help_text=_('Статус сдачи задания')
    )
    mark = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name=_('Отметка'),
        help_text=_('Отметка за задание'),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f'{self.task} ({self.student})'

    class Meta:
        ordering = ['student', 'task']
        verbose_name = _('Задание студента')
        verbose_name_plural = _('Задания студентов')


class StudentAttendance(Base):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name=_('Студент'),
        help_text=_('Студент, чья посещаемость фиксируется')
    )
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        verbose_name=_('Занятие'),
        help_text=_('Занятие, которое фиксируется')
    )
    skipped = models.BooleanField(
        default=False,
        verbose_name=_('Был'),
        help_text=_('Статус пропуска занятия')
    )
    late = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('Опоздание'),
        help_text=_('Опоздание в минутах')
    )

    def __str__(self):
        late = f'| опоздание на {self.late} минут'
        return f'{self.student} ({self.skipped}){late if self.late > 0 else ""}'

    class Meta:
        ordering = ['student', 'attendance']
        verbose_name = _('Пропуск студента')
        verbose_name_plural = _('Пропуски студентов')
