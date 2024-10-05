from django.utils.translation import gettext_lazy as _

from django.db import models

from apps.account.models import StudentGroup

from apps.bot.models import Base


class Lesson(Base):
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Группа'),
        help_text=_('Группа, которая проводит занятие')
    )
    topic = models.CharField(
        max_length=255,
        verbose_name=_('Тема'),
        help_text=_('Тема занятия')
    )
    body = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание'),
        help_text=_('Описание занятия')
    )

    def __str__(self):
        return f'{self.topic} - {self.student_group}'

    class Meta:
        ordering = ['student_group']
        verbose_name = _('Занятие')
        verbose_name_plural = _('Занятия')


class Task(Base):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Занятие'),
        help_text=_('Занятие, к которому относится задание')
    )
    body = models.TextField(
        verbose_name=_('Задание'),
        help_text=_('Описание задания')
    )

    def __str__(self):
        return f'{self.lesson}: {self.body}'

    class Meta:
        ordering = ['lesson', 'body']
        verbose_name = _('Задание')
        verbose_name_plural = _('Задания')


class Attendance(Base):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Занятие'),
        help_text=_('Занятие, для которого фиксируется посещаемость')
    )
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Группа'),
        help_text=_('Группа, чья посещаемость фиксируется')
    )

    def __str__(self):
        return f'{self.lesson} - {self.student_group}'

    class Meta:
        ordering = ['student_group', 'lesson']
        verbose_name = _('Отчёт посещаемости')
        verbose_name_plural = _('Отчёты посещаемости')
