from django.contrib import admin

from apps.bot.admin import BaseAdmin

from .models import Student, StudentGroup


@admin.register(Student)
class StudentAdmin(BaseAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('last_name', 'phone_number')
    fields = ('first_name', 'last_name', 'phone_number')
    list_per_page = 20


@admin.register(StudentGroup)
class StudentGroupAdmin(BaseAdmin):
    list_display = ('name', 'classroom', 'class_schedule', 'class_time')
    search_fields = ('name', 'description')
    list_filter = ('classroom', 'class_schedule', 'class_time')
    ordering = ('name',)
    fields = ('name', 'description', 'classroom', 'class_schedule', 'class_time', 'students')
    list_per_page = 20
