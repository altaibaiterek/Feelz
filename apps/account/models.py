from django.db import models

from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.bot.models import Base

from apps.classroom.models import ClassRoom, ClassSchedule, ClassTime


class Student(Base):
    first_name = models.CharField(
        max_length=255, 
        blank=True,
        null=True,
        verbose_name=_("Имя"),
        help_text=_('Имя студента')
        )
    last_name = models.CharField(
        max_length=255, 
        blank=True,
        null=True,
        verbose_name=_("Фамилия"),
        help_text=_('Фамилия студента')
        )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name=_("Телефон"),
        help_text=_("Номер телефона студента (Например: +996555333222).")
        )
    telegram_username = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_("Псевдоним в Телеграм"),
        help_text=_("Псевдоним студента в Телеграм.")
        )
    telegram_id = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        verbose_name=_("Телеграм идентификатор"),
        help_text=_("Уникальный идентификатор студента в Телеграм.")
        )
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} {self.phone}'
    
    class Meta:
        ordering = ['last_name']
        verbose_name = _('Студент')
        verbose_name_plural = _('Студенты')
    
    
class StudentGroup(Base):
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Название'),
        help_text=_('Название группы'),
        )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание'),
        help_text=_('Описание группы'),
        )
    students = models.ManyToManyField(
        Student,
        related_name='student_groups',
        blank=True,
        verbose_name=_("Студенты"),
        help_text=_("Студенты, относящиеся к группе."),
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Кабинет'),
        help_text=_('Кабинет, относящийся к группе'),
    )
    class_schedule = models.ForeignKey(
        ClassSchedule,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Расписание (дни недели)'),
        help_text=_('Расписание группы в днях недели'),
    )
    class_time = models.ForeignKey(
        ClassTime,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Время занятий'),
        help_text=_('Время занятий группы, проч'),
    )
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Группа студентов')
        verbose_name_plural = _('Группы студентов')
