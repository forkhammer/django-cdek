from django.contrib import admin

from djcdek.cdek.models import *


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code')
    search_fields = ('title', 'code')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country', 'code', 'kladr_region_code', 'fias_region_guid')
    list_filter = ('country',)
    search_fields = ('title', )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'region', 'postal_codes', 'timezone')
    list_filter = ('region', )
    search_fields = ('title', 'code', 'postal_codes')


@admin.register(DeliveryPoint)
class DeliveryPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'city', 'type', 'postal_code', 'phones', 'email')
    list_filter = ('type', 'take_only', 'is_dressing_room', 'have_cashless', 'have_cash', 'allowed_cod', 'city')
    search_fields = ('title', 'code', 'postal_code', 'phones', 'email')
