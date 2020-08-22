from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Config, Gallery, Photo, Page, Block


@admin.register(Config)
class ConfigAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Основные', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('name', 'phone', 'email', 'address')
        }),
        ('Блок приветствия', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('title', 'content')
        }),
        ('Контент', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('gallery', 'page')
        }),
        ('Подвал', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('footer_1', 'footer_2', 'footer_3', 'footer_4',)
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


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'update_at')
    fieldsets = (
        ('Основные', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('title', 'content',)
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('seo_title', 'seo_description', 'slug'),
        }),
    )


@admin.register(Block)
class BlockADmin(admin.ModelAdmin):
    pass


admin.site.site_header = "Банщик"
admin.site.site_title = "Банщик"
