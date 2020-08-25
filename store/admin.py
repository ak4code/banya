from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.utils.html import format_html

from .models import Category, Product
from import_export import resources, fields, widgets
from import_export.admin import ImportExportActionModelAdmin
from adminsortable.admin import SortableAdmin


@admin.register(Category)
class CategoryAdmin(SortableAdmin):
    search_fields = ('name',)
    list_display = ('image_tag', 'name', 'is_active', 'create_at', 'update_at')
    readonly_fields = ['image_tag', ]
    list_display_links = ('image_tag', 'name')
    fieldsets = (
        (None, {
            'fields': ('name', 'image_tag', 'image', 'is_active')
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty',),
            'fields': ('seo_title', 'seo_description', 'slug',),
        }),
    )

    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.get_small_img()))

    image_tag.short_description = 'Миниатюра'


class CategoryWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if value:
            obj, created = self.get_queryset(value, row, *args, **kwargs).get_or_create(**{self.field: value})
            return obj
        else:
            return None


class ProductResource(resources.ModelResource):
    name = fields.Field(
        column_name='Название',
        attribute='name',
        widget=widgets.Widget())
    description = fields.Field(
        column_name='Описание',
        attribute='description',
        widget=widgets.Widget())
    price = fields.Field(
        column_name='Цена',
        attribute='price',
        widget=widgets.DecimalWidget())
    in_stock = fields.Field(
        column_name='В наличии',
        attribute='in_stock',
        default=0,
        widget=widgets.BooleanWidget())
    category = fields.Field(
        column_name='Категория',
        attribute='category',
        widget=CategoryWidget(Category, 'name'))
    features = fields.Field(
        column_name='Характеристики',
        attribute='features',
        widget=widgets.Widget())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'price', 'in_stock', 'features')
        export_order = ('id', 'category', 'name', 'price', 'in_stock', 'description', 'features')


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = ('image_tag', 'name', 'category', 'price', 'in_stock', 'create_at', 'update_at')
    list_display_links = ('image_tag', 'name')
    list_filter = ('category',)
    search_fields = ('name',)
    readonly_fields = ['image_tag', ]
    actions = ImportExportActionModelAdmin.actions + ['make_available', 'make_unavailable']
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description', 'price', 'in_stock', 'unit', 'quantity', 'image_tag', 'image',
                       'features')
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty',),
            'fields': ('seo_title', 'seo_description'),
        }),
    )

    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.get_small_img()))

    image_tag.short_description = 'Миниатюра'

    def make_available(self, request, queryset):
        updated = queryset.update(in_stock=True)
        self.message_user(request, ngettext(
            '%d товар помечен как "В наличии".',
            '%d товаров помечены как "В наличии".',
            updated,
        ) % updated, messages.SUCCESS)

    make_available.short_description = "Сделать выделенные товары 'В наличии'"

    def make_unavailable(self, request, queryset):
        updated = queryset.update(in_stock=False)
        self.message_user(request, ngettext(
            '%d товар помечен как "Под заказ".',
            '%d товаров помечены как "Под заказ".',
            updated,
        ) % updated, messages.SUCCESS)

    make_unavailable.short_description = "Сделать выделенные товары 'Под заказ'"
