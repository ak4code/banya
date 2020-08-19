from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer
from adminsortable.models import SortableMixin
from core.models import SEOBase
from uuslug import uuslug


class Category(SEOBase, SortableMixin):
    name = models.CharField(max_length=255, default='Раздел', verbose_name='Название')
    slug = models.CharField(max_length=255, blank=True, null=True, verbose_name='ЧПУ ссылка', unique=True,
                            db_index=True)
    position = models.PositiveIntegerField(default=0, editable=False, db_index=True, verbose_name='Порядок')
    image = models.ImageField(upload_to='store/category', blank=True, null=True, verbose_name='Загрузка изображения')
    is_active = models.BooleanField(default=True, verbose_name='Активно', help_text='Отображение на сайте вкл/выкл')

    def __str__(self):
        return self.name

    def get_title(self):
        return self.seo_title or self.name

    def get_absolute_url(self):
        return reverse('store:category', args=[str(self.slug)])

    def get_medium_img(self):
        if self.image:
            return get_thumbnailer(self.image)['medium'].url
        else:
            return static('store/no-image.webp')

    def get_small_img(self):
        if self.image:
            return get_thumbnailer(self.image)['small'].url
        else:
            return static('store/no-image.webp')

    get_small_img.short_description = 'Миниатюра'

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['position']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(SEOBase):
    name = models.CharField(max_length=255, default='Товар', verbose_name='Название')
    image = models.ImageField(upload_to='store/products', blank=True, null=True, verbose_name='Загрузка изображения')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE,
                                 verbose_name='Категория')
    price = models.DecimalField(decimal_places=2, max_digits=20, default=1, verbose_name='Цена')
    unit = models.CharField(default='шт.', max_length=100, verbose_name='Единица измерения')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество на складе')
    features = models.TextField(blank=True, null=True, verbose_name='Характеристики')
    in_stock = models.BooleanField(default=True, help_text='При снятой отметки будет отображатся "Под заказ"',
                                   verbose_name='В наличии')

    def __str__(self):
        return self.name

    def get_title(self):
        return self.seo_title or self.name

    def get_absolute_url(self):
        return reverse('store:product', kwargs={
            'category': self.category.slug,
            'pk': self.pk,
        })

    def get_full_img(self):
        if self.image:
            return get_thumbnailer(self.image).url
        else:
            return static('store/no-image.webp')

    def get_medium_img(self):
        if self.image:
            return get_thumbnailer(self.image)['medium'].url
        else:
            return static('store/no-image.webp')

    def get_small_img(self):
        if self.image:
            return get_thumbnailer(self.image)['small'].url
        else:
            return static('store/no-image.webp')

    def save(self, *args, **kwargs):
        if not self.seo_title:
            self.seo_title = self.name
        if not self.seo_description:
            self.seo_description = self.name

        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['create_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
