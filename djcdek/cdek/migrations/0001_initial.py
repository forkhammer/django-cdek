# Generated by Django 2.2.10 on 2020-04-16 04:24

from django.db import migrations, models
import django.db.models.deletion
import djcdek.types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название')),
                ('code', models.CharField(max_length=100, verbose_name='Код населенного пункта')),
                ('fias_guid', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Уникальный идентификатор ФИАС населенного пункта')),
                ('kladr_code', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Код КЛАДР населенного пункта')),
                ('longitude', models.FloatField(blank=True, default=None, null=True, verbose_name='Код населенного пункта')),
                ('latitude', models.FloatField(blank=True, default=None, null=True, verbose_name='Код населенного пункта')),
                ('timezone', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Временная зона')),
                ('payment_limit', models.IntegerField(blank=True, default=None, null=True, verbose_name='Платежные ограничения')),
                ('postal_codes', models.TextField(blank=True, default=None, null=True, verbose_name='Почтовые индексы (через ;)')),
            ],
            options={
                'verbose_name': 'Насленный пункт',
                'verbose_name_plural': 'Населенные пункты',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название')),
                ('code', models.CharField(max_length=2, verbose_name='Код страны')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cdek.Country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='DeliveryPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Название')),
                ('code', models.CharField(max_length=100, verbose_name='Код')),
                ('postal_code', models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Почтовый индекс')),
                ('longitude', models.FloatField(blank=True, default=None, null=True, verbose_name='Код населенного пункта')),
                ('latitude', models.FloatField(blank=True, default=None, null=True, verbose_name='Код населенного пункта')),
                ('address', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Адрес')),
                ('address_full', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Полный адрес')),
                ('address_comment', models.TextField(blank=True, default='', null=True, verbose_name='Описание местоположения')),
                ('nearest_station', models.TextField(blank=True, default='', null=True, verbose_name='Ближайшая станция/остановка транспорта')),
                ('phones', models.TextField(blank=True, default='', null=True, verbose_name='Список телефонов')),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('note', models.TextField(blank=True, default='', null=True, verbose_name='Примечание по ПВЗ')),
                ('type', models.CharField(choices=[(djcdek.types.DeliveryPointType('PVZ'), 'Склад CDEK'), (djcdek.types.DeliveryPointType('POSTOMAT'), 'Постомат')], default='PVZ', max_length=10, verbose_name='Тип ПВЗ')),
                ('owner_сode', models.CharField(blank=True, default=None, max_length=10, null=True, verbose_name='Принадлежность ПВЗ компании')),
                ('take_only', models.BooleanField(blank=True, default=False, verbose_name='Является ли ПВЗ только пунктом выдачи или также осуществляет приём грузов')),
                ('is_dressing_room', models.BooleanField(blank=True, default=False, verbose_name='Есть ли примерочная')),
                ('have_cashless', models.BooleanField(blank=True, default=False, verbose_name='Есть безналичный расчет')),
                ('have_cash', models.BooleanField(blank=True, default=False, verbose_name='Есть приём наличных')),
                ('allowed_cod', models.BooleanField(blank=True, default=False, verbose_name='Разрешен наложенный платеж в ПВЗ')),
                ('site', models.CharField(blank=True, default=None, max_length=300, null=True, verbose_name='Ссылка на страницу ПВЗ')),
                ('weight_min', models.FloatField(blank=True, default=None, null=True, verbose_name='Минимальный вес (в кг.), принимаемый в ПВЗ (> WeightMin)')),
                ('weight_max', models.FloatField(blank=True, default=None, null=True, verbose_name='Максимальный вес (в кг.), принимаемый в ПВЗ (<=WeightMax)')),
                ('city', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cdek.City', verbose_name='Населенный пункт')),
            ],
            options={
                'verbose_name': 'ПВЗ',
                'verbose_name_plural': 'ПВЗ',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='cdek.Region', verbose_name='Регион'),
        ),
    ]
