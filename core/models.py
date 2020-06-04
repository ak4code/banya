from django.templatetags.static import static
from django.db import models
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer
from solo.models import SingletonModel


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
    gallery = models.OneToOneField('Gallery', blank=True, null=True, related_name='gallery', on_delete=models.CASCADE,
                                   verbose_name='Галлерея')
    page = models.OneToOneField('Page', blank=True, null=True, related_name='page', on_delete=models.CASCADE,
                                verbose_name='Страница')

    def __str__(self):
        return f"Главная {self.name}"

    class Meta:
        verbose_name = "Главная"


class Page(SEOBase):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(blank=True, null=True, verbose_name='Контент')

    def get_title(self):
        return self.seo_title or self.title

    def save(self, *args, **kwargs):
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
