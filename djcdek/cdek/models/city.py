from django.db import models

from .region import Region


class City(models.Model):
    """
    Населенный пункт доставки
    """
    title = models.CharField('Название', max_length=300)
    code = models.CharField('Код населенного пункта', max_length=100)
    fias_guid = models.CharField('Уникальный идентификатор ФИАС населенного пункта', max_length=100,
                    default=None, blank=True, null=True)
    kladr_code = models.CharField('Код КЛАДР населенного пункта', max_length=100,
                    default=None, blank=True, null=True)
    longitude = models.FloatField('Код населенного пункта', default=None, blank=True, null=True)
    latitude = models.FloatField('Код населенного пункта', default=None, blank=True, null=True)
    timezone = models.CharField('Временная зона', max_length=50, default=None, blank=True, null=True)
    payment_limit = models.IntegerField('Платежные ограничения', default=None, blank=True, null=True)
    postal_codes = models.TextField('Почтовые индексы (через ;)', default=None, blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name='Регион', default=None, blank=True, null=True, on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'

    def __str__(self):
        return self.title

    def __repr__(self):
        return str(self.id)
