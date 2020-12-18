# Generated by Django 2.2.10 on 2020-04-16 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdek', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Населенный пункт', 'verbose_name_plural': 'Населенные пункты'},
        ),
        migrations.AddField(
            model_name='region',
            name='code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Код региона'),
        ),
        migrations.AddField(
            model_name='region',
            name='fias_region_guid',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Уникальный идентификатор ФИАС региона'),
        ),
        migrations.AddField(
            model_name='region',
            name='kladr_region_code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Код КЛАДР региона'),
        ),
        migrations.AlterField(
            model_name='country',
            name='code',
            field=models.CharField(max_length=2, unique=True, verbose_name='Код страны'),
        ),
    ]