from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Config


@admin.register(Config)
class ConfigAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Основные', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('name', 'logo')
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('seo_title', 'seo_description'),
        }),
    )


config = Config.get_solo()

admin.site.site_header = config.name
admin.site.site_title = config.name
