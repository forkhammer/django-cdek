from django.db import models

from .city import City
from djcdek.types import DeliveryPointType


class DeliveryPoint(models.Model):
    """
    Точка доставки
    """
    title = models.CharField('Название', max_length=300)
    code = models.CharField('Код', max_length=100)
    city = models.ForeignKey(City, verbose_name='Населенный пункт', default=None, blank=True, null=True, 
                    on_delete=models.CASCADE, related_name='deliverypoints')
    postal_code = models.CharField('Почтовый индекс', max_length=10, default=None, blank=True, null=True)
    longitude = models.FloatField('Код населенного пункта', default=None, blank=True, null=True)
    latitude = models.FloatField('Код населенного пункта', default=None, blank=True, null=True)
    address = models.CharField('Адрес', max_length=500, default='', blank=True, null=True)
    address_full = models.CharField('Полный адрес', max_length=500, default='', blank=True, null=True)
    address_comment = models.TextField('Описание местоположения', default='', blank=True, null=True)
    nearest_station = models.TextField('Ближайшая станция/остановка транспорта', default='', blank=True, null=True)
    phones = models.TextField('Список телефонов', default='', blank=True, null=True)
    email = models.EmailField(default=None, blank=True, null=True)
    note = models.TextField('Примечание по ПВЗ', default='', blank=True, null=True)
    work_time = models.TextField('Режим работы', default='', blank=True, null=True)
    type = models.CharField('Тип ПВЗ', max_length=10, choices=list(DeliveryPointType.to_dict().items()), default=DeliveryPointType.PVZ.value)
    owner_code = models.CharField('Принадлежность ПВЗ компании', max_length=10, default=None, blank=True, null=True)
    take_only = models.BooleanField('Является ли ПВЗ только пунктом выдачи или также осуществляет приём грузов', default=False, blank=True)
    is_dressing_room = models.BooleanField('Есть ли примерочная', default=False, blank=True)
    have_cashless = models.BooleanField('Есть безналичный расчет', default=False, blank=True)
    have_cash = models.BooleanField('Есть приём наличных', default=False, blank=True)
    allowed_cod = models.BooleanField('Разрешен наложенный платеж в ПВЗ', default=False, blank=True)
    site = models.CharField('Ссылка на страницу ПВЗ', max_length=300, default=None, blank=True, null=True)
    weight_min = models.FloatField('Минимальный вес (в кг.), принимаемый в ПВЗ (> WeightMin)', default=None, blank=True, null=True)
    weight_max = models.FloatField('Максимальный вес (в кг.), принимаемый в ПВЗ (<=WeightMax)', default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'ПВЗ'
        verbose_name_plural = 'ПВЗ'

    def __str__(self):
        return self.title

    def __repr__(self):
        return str(self.id)



