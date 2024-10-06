from django.contrib import admin

from apps.education.models import Attendance, Task

from apps.progress.models import StudentAttendance, StudentTask


class StudentAttendanceInline(admin.TabularInline):
    model = StudentAttendance
    extra = 0
    fields = ('student', 'skipped', 'late')
    readonly_fields = ('student',)
    can_delete = False


class StudentTaskInline(admin.TabularInline):
    model = StudentTask
    extra = 0
    fields = ('student', 'passed', 'mark')
    readonly_fields = ('student',)
    can_delete = False


class TaskInline(admin.StackedInline):
    model = Task
    extra = 0
    fields = ('body',)


class AttendanceInline(admin.StackedInline):
    model = Attendance
    extra = 0
    fields = ('student_group',)
