from adminsortable.models import SortableMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer
from solo.models import SingletonModel
from tinymce import HTMLField
from uuslug import uuslug
from mptt.models import MPTTModel, TreeForeignKey


class SEOBase(models.Model):
    seo_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='SEO заголовок')
    seo_description = models.TextField(max_length=255, blank=True, null=True, verbose_name='SEO описание')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f"{self.seo_title}"

    class Meta:
        abstract = True


class Config(SingletonModel, SEOBase):
    name = models.CharField(max_length=255, default='Магазин', verbose_name='Название')
    logo = models.FileField(upload_to='site/logo', blank=True, null=True, verbose_name='Лого')
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    title = models.CharField(max_length=255, default='Добро пожаловать', verbose_name='Заголовок')
    content = HTMLField(blank=True, null=True, verbose_name='Контент')
    gallery = models.OneToOneField('Gallery', blank=True, null=True, related_name='gallery', on_delete=models.CASCADE,
                                   verbose_name='Галлерея')
    page = models.OneToOneField('Page', blank=True, null=True, related_name='page', on_delete=models.CASCADE,
                                verbose_name='Страница')
    shop_page = models.OneToOneField('Page', blank=True, null=True, related_name='shop', on_delete=models.CASCADE,
                                verbose_name='Страница магазина')
    footer_1 = HTMLField(blank=True, null=True, verbose_name='Подвал Виджет_1')
    footer_2 = HTMLField(blank=True, null=True, verbose_name='Подвал Виджет_2')
    footer_3 = HTMLField(blank=True, null=True, verbose_name='Подвал Виджет_3')
    footer_4 = HTMLField(blank=True, null=True, verbose_name='Подвал Виджет_4')

    def __str__(self):
        return f"Настройки {self.name}"

    class Meta:
        verbose_name = "Настройки"


class Page(SEOBase):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = HTMLField(blank=True, null=True, verbose_name='Контент')
    slug = models.CharField(max_length=255, blank=True, null=True, verbose_name='ЧПУ ссылка', db_index=True)

    def get_absolute_url(self):
        return reverse('core:page', args=[str(self.slug)])

    def get_title(self):
        return self.seo_title or self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuslug(self.title, instance=self)
        if not self.seo_title:
            self.seo_title = self.title
        if not self.seo_description:
            self.seo_description = self.title

        super(Page, self).save(*args, **kwargs)

    class Meta:
        ordering = ['create_at']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'


class Gallery(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Галлерея'
        verbose_name_plural = 'Галлерея'


class Photo(models.Model):
    gallery = models.ForeignKey('Gallery', related_name='photos', on_delete=models.CASCADE, verbose_name='Галлерея')
    image = models.ImageField(upload_to='gallery/photos', verbose_name='Изображение')
    caption = models.TextField(blank=True, null=True, verbose_name='Подпись')

    def __str__(self):
        return f'Фото #{self.pk}'

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

    def image_tag(self):
        return format_html('<img src="{}" width="100" height="100" />'.format(self.get_small_img()))

    image_tag.short_description = 'Миниатюра'

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class Block(models.Model):
    title = models.CharField(max_length=255, default='Добро пожаловать', verbose_name='Заголовок')
    content = HTMLField(blank=True, null=True, verbose_name='Контент')

    def __str__(self):
        return f'Блок #{self.title}'

    class Meta:
        verbose_name = 'Блок контент'
        verbose_name_plural = 'Блоки контента'


class Menu(models.Model):
    POSITON_CHOICES = (
        (None, 'Выберите позицию'),
        ('main', 'Главное меню'),
        ('mobile', 'Мобильное меню'),
        ('footer', 'Меню в подвале'),
    )
    name = models.CharField(max_length=200, verbose_name='Название меню')
    position = models.CharField(max_length=100, choices=POSITON_CHOICES, unique=True, db_index=True,
                                verbose_name='Позиция')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class MenuItem(MPTTModel):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE, verbose_name='Меню')
    name = models.CharField(max_length=200, verbose_name='Название')
    parent = TreeForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE,
                            verbose_name='Родитель')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Произвольная ссылка')
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE,
                                     verbose_name='Тип контента')
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name='ID обьекта')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.menu.name} -> {self.name}'

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_link(self):
        if self.content_object:
            return self.content_object.get_absolute_url()
        elif self.link:
            return self.link
        else:
            return '#'

    class Meta:
        ordering = ['name']
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
