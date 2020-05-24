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
