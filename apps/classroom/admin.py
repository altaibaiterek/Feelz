from django.contrib import admin

from apps.bot.admin import BaseAdmin

from .models import ClassRoom, ClassSchedule, ClassTime


@admin.register(ClassRoom)
class ClassRoomAdmin(BaseAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('name',)
    fields = ('name', 'description')
    list_per_page = 20


@admin.register(ClassSchedule)
class ClassScheduleAdmin(BaseAdmin):
    list_display = ('name', 'description', 'display_days')
    search_fields = ('name', 'description')
    list_filter = ('days',)
    ordering = ('name',)
    fields = ('name', 'description', 'days')
    list_per_page = 20

    def display_days(self, obj):
        return ", ".join([str(day) for day in obj.days.all()])
    display_days.short_description = 'Дни'


@admin.register(ClassTime)
class ClassTimeAdmin(BaseAdmin):
    list_display = ('name', 'start_time', 'end_time')
    search_fields = ('name',)
    list_filter = ('start_time', 'end_time')
    ordering = ('start_time',)
    fields = ('name', 'description', 'start_time', 'end_time')
    list_per_page = 20
