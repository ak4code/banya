from django.contrib import admin
from .models import Category, Product
from import_export import resources, fields, widgets
from import_export.admin import ImportExportActionModelAdmin
from adminsortable.admin import SortableAdmin


@admin.register(Category)
class CategoryAdmin(SortableAdmin):
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('SEO Настройки', {
            'classes': ('collapse',),
            'fields': ('slug', 'seo_title', 'seo_description'),
        }),
    )


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
        fields = ('id', 'name', 'category', 'description', 'price', 'features')
        export_order = ('id', 'category', 'name', 'price', 'description', 'features')


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = ('image_tag', 'name', 'category', 'price', 'create_at', 'update_at')
    list_display_links = ('image_tag', 'name')
    list_filter = ('category',)
    search_fields = ('name',)
    readonly_fields = ['image_tag']
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
