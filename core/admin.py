from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Config, Gallery, Photo


@admin.register(Config)
class ConfigAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Основные', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('name', 'logo')
        }),
        ('Контент', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('gallery', 'page')
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('seo_title', 'seo_description'),
        }),
    )


class PhotoInlines(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image_tag', 'image', 'caption')
    readonly_fields = ('image_tag',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = (PhotoInlines,)


config = Config.get_solo()

admin.site.site_header = config.name
admin.site.site_title = config.name
