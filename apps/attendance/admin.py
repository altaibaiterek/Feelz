from django.contrib import admin

from apps.bot.admin import BaseAdmin

from .models import StudentTask, StudentAttendance


@admin.register(StudentTask)
class StudentTaskAdmin(BaseAdmin):
    list_display = ('student', 'task', 'body')
    list_filter = ('student', 'task')
    search_fields = ('student__first_name', 'student__last_name', 'task__body')
    ordering = ('student', 'task')
    fields = ('student', 'task', 'body')
    list_per_page = 20


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(BaseAdmin):
    list_display = ('student', 'attendance', 'skipped', 'late')
    list_filter = ('student', 'attendance', 'skipped')
    search_fields = ('student__first_name', 'student__last_name', 'attendance__topic')
    ordering = ('student', 'attendance')
    fields = ('student', 'attendance', 'skipped', 'late')
    list_per_page = 20
