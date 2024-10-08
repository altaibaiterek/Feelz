from django.contrib import admin

from apps.bot.admin import BaseAdmin

from apps.education.inlines import AttendanceInline, StudentAttendanceInline, StudentTaskInline, TaskInline

from .models import Lesson, Task, Attendance


@admin.register(Lesson)
class LessonAdmin(BaseAdmin):
    list_display = ('topic', 'created_at_date', 'body', 'student_group')
    list_filter = ('student_group',)
    search_fields = ('topic', 'body', 'student_group__name')
    ordering = ('student_group', 'topic')
    fields = ('topic', 'student_group', 'body')
    inlines = [TaskInline, ]
    list_per_page = 20

    def created_at_date(self, obj):
        return obj.created_at.strftime('%d.%m.%Y')

    created_at_date.short_description = 'Дата'


@admin.register(Attendance)
class AttendanceAdmin(BaseAdmin):
    list_display = ('lesson', 'lesson_date', 'student_group')
    search_fields = ('lesson__topic', 'student_group__name')
    list_filter = ('lesson', 'student_group')
    ordering = ('lesson', 'student_group')
    fields = ('lesson', 'student_group')
    inlines = [StudentAttendanceInline]
    list_per_page = 20

    def lesson_date(self, obj):
        return obj.lesson.created_at.strftime('%d.%m.%Y')

    lesson_date.short_description = 'Дата занятия'
