from django.db import models


class Country(models.Model):
    """
    Страна доставки
    """
    title = models.CharField('Название', max_length=300)
    code = models.CharField('Код страны', max_length=2, unique=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.title

    def __repr__(self):
        return str(self.id)
    