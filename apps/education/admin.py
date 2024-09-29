from django.contrib import admin

from apps.bot.admin import BaseAdmin

from .models import Lesson, Task, Attendance


@admin.register(Lesson)
class LessonAdmin(BaseAdmin):
    list_display = ('topic', 'student_group', 'body')
    list_filter = ('student_group',)
    search_fields = ('topic', 'body', 'student_group__name')
    ordering = ('student_group', 'topic')
    fields = ('topic', 'student_group', 'body')
    list_per_page = 20


@admin.register(Task)
class TaskAdmin(BaseAdmin):
    list_display = ('lesson', 'body')
    search_fields = ('lesson__topic', 'body')
    list_filter = ('lesson',)
    ordering = ('lesson',)
    fields = ('lesson', 'body')
    list_per_page = 20


@admin.register(Attendance)
class AttendanceAdmin(BaseAdmin):
    list_display = ('lesson', 'student_group')
    search_fields = ('lesson__topic', 'student_group__name')
    list_filter = ('lesson', 'student_group')
    ordering = ('lesson', 'student_group')
    fields = ('lesson', 'student_group')
    list_per_page = 20
