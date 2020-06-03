from django.db import models
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

    def __str__(self):
        return f"Настройки {self.name}"

    class Meta:
        verbose_name = "Настройки"


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
