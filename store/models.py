from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer

from core.models import SEOBase
from uuslug import uuslug


class Category(SEOBase):
    name = models.CharField(max_length=255, default='Раздел', verbose_name='Название')
    slug = models.CharField(max_length=255, blank=True, null=True, verbose_name='ЧПУ ссылка', unique=True,
                            db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(SEOBase):
    name = models.CharField(max_length=255, default='Товар', verbose_name='Название')
    image = models.ImageField(upload_to='store/products', blank=True, null=True, verbose_name='Загрузка изображения')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE,
                                 verbose_name='Категория')
    price = models.DecimalField(decimal_places=2, max_digits=20, default=1, verbose_name='Цена')
    features = models.TextField(blank=True, null=True, verbose_name='Характеристики')
    in_stock = models.BooleanField(default=True, help_text='При снятой отметки будет отображатся "Под заказ"',
                                   verbose_name='В наличии')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product', (), {
            'category': self.category.slug,
            'pk': self.pk,
        })

    def get_medium_img(self):
        if self.image:
            return get_thumbnailer(self.image)['medium'].url
        else:
            return static('store/no-image.webp')

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (get_thumbnailer(self.image)['small'].url))
        else:
            return mark_safe('<img src="%s" width="50" height="50" />' % (static('store/no-image.webp')))

    image_tag.short_description = 'Изображение'

    class Meta:
        ordering = ['create_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
