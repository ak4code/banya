from django.conf import settings
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


class Order(models.Model):
    SHIPPING_TYPE_CHOICES = (
        ('pickup', 'САМОВЫВОЗ'),
        ('shipping', 'ДОСТАВКА'),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders',
                                 verbose_name='Клиент')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    shipping_type = models.CharField(max_length=8, default='pickup', choices=SHIPPING_TYPE_CHOICES,
                                     verbose_name='Тип доставки')
    shipping_city = models.CharField(max_length=255, blank=True, null=True, verbose_name='Город доставки')
    shipping_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес доставки')

    def __str__(self):
        return f'Заказ №{self.pk} от {self.create_at.strftime("%d.%m.%Y %H:%M")}, клиент {self.customer.first_name}'

    def amount(self):
        return sum([i.amount() for i in self.items.all()])

    amount.short_description = 'Сумма заказа'

    class Meta:
        ordering = ['-create_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items', verbose_name='Товар')
    price = models.DecimalField(decimal_places=2, max_digits=20, default=1, verbose_name='Цена за единицу')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')

    def amount(self):
        return self.price * self.quantity

    amount.short_description = 'Сумма'

    def __str__(self):
        return f'{self.product.name} - {self.price} за {self.product.unit}'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
