from django.contrib import admin

from apps.bot.admin import BaseAdmin

from .models import StudentTask, StudentAttendance


@admin.register(StudentTask)
class StudentTaskAdmin(BaseAdmin):
    list_display = ('student', 'task', 'passed', 'mark')
    list_filter = ('student', 'task', 'passed')
    search_fields = ('student__first_name', 'student__last_name')
    ordering = ('student', 'task')
    fields = ('student', 'task', 'passed', 'mark')
    list_per_page = 20


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(BaseAdmin):
    list_display = ('student', 'attendance', 'skipped', 'late')
    list_filter = ('student', 'attendance', 'skipped')
    search_fields = ('student__first_name', 'student__last_name', 'attendance__topic')
    ordering = ('student', 'attendance')
    fields = ('student', 'attendance', 'skipped', 'late')
    list_per_page = 20
