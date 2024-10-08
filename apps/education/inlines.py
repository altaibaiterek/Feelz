from django.contrib import admin

from apps.education.models import Attendance, Task

from apps.progress.models import StudentAttendance, StudentTask

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class StudentAttendanceInline(admin.TabularInline):
    model = StudentAttendance
    extra = 0
    fields = ('student', 'lesson_info', 'skipped', 'late')
    readonly_fields = ('student', 'lesson_info')
    can_delete = False

    def lesson_info(self, obj):
        if obj.attendance and obj.attendance.lesson:
            return format_html(
                "{} ({})",
                obj.attendance.lesson.topic,
                obj.attendance.lesson.created_at.strftime('%d.%m.%Y')
            )
        return _("Нет информации о занятии")

    lesson_info.short_description = _('Занятие')


class StudentTaskInline(admin.TabularInline):
    model = StudentTask
    extra = 0
    fields = ('student', 'task_info', 'passed', 'mark')
    readonly_fields = ('student', 'task_info')
    can_delete = False

    def task_info(self, obj):
        if obj.task and obj.task.lesson:
            return format_html(
                "{} ({})",
                obj.task.lesson.topic,
                obj.task.lesson.created_at.strftime('%d.%m.%Y')
            )
        return _("Нет информации о занятии")

    task_info.short_description = _('Занятие')


class TaskInline(admin.StackedInline):
    model = Task
    extra = 0
    fields = ('body',)


class AttendanceInline(admin.StackedInline):
    model = Attendance
    extra = 0
    fields = ('student_group',)
