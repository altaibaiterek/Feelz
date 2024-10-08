from django.contrib import admin

from apps.bot.admin import BaseAdmin
from apps.education.inlines import StudentAttendanceInline, StudentTaskInline

from .models import Student, StudentGroup

from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

@admin.register(Student)
class StudentAdmin(BaseAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'student_groups_links')
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('last_name', 'phone_number')
    fields = ('first_name', 'last_name', 'phone_number', 'student_groups_links')  # Добавляем поле в форму
    readonly_fields = ('student_groups_links', 'created_at', 'updated_at')  # Поле только для чтения в окне редактирования
    list_per_page = 20

    def student_groups_links(self, obj):
        # Проверяем, что объект существует (иначе будет ошибка при создании нового студента)
        if obj.pk:
            # Получаем все группы студента
            groups = obj.student_groups.all()
            # Формируем ссылки на каждую группу
            links = [
                format_html('<a href="{}">{}</a>', reverse('admin:account_studentgroup_change', args=[group.id]), group.name)
                for group in groups
            ]
            # Возвращаем группы в виде ссылок, разделенных запятой
            return format_html(', '.join(links))
        return '-'

    student_groups_links.short_description = _('Группы студента')

    inlines = [StudentTaskInline, StudentAttendanceInline]


@admin.register(StudentGroup)
class StudentGroupAdmin(BaseAdmin):
    list_display = ('name', 'classroom', 'class_schedule', 'class_time')
    search_fields = ('name', 'description')
    list_filter = ('classroom', 'class_schedule', 'class_time')
    ordering = ('name',)
    fields = ('name', 'description', 'classroom', 'class_schedule', 'class_time', 'students')
    list_per_page = 20
    filter_horizontal = ('students',)
