from django.utils.translation import gettext_lazy as _

from django.contrib import admin

from django.contrib.auth.models import User, Group


admin.site.unregister(User)
admin.site.unregister(Group)


class BaseAdmin(admin.ModelAdmin):
    """
    Базовый класс для всех моделей в админке.
    Поля 'created_at' и 'updated_at' скрыты во вкладке 'Системная информация'.
    """
    
    readonly_fields = ('created_at', 'updated_at')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if not any(fs[0] == _('Системная информация') for fs in fieldsets):
            fieldsets = list(fieldsets)
            fieldsets.append((_('Системная информация'), {
                'classes': ('collapse',),
                'fields': ('created_at', 'updated_at'),
            }))
        
        return fieldsets
