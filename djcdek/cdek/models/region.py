from django.db import models

from .country import Country


class Region(models.Model):
    """
    Регион доставки
    """
    title = models.CharField('Название', max_length=300)
    country = models.ForeignKey(Country, verbose_name='Страна', on_delete=models.CASCADE)
    code = models.CharField('Код региона', max_length=50, default=None, blank=True, null=True)
    kladr_region_code = models.CharField('Код КЛАДР региона', max_length=50, default=None, blank=True, null=True)
    fias_region_guid = models.CharField('Уникальный идентификатор ФИАС региона', max_length=50, default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return self.title

    def __repr__(self):
        return str(self.id)