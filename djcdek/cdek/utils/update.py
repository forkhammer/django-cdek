import logging
from djcdek.cdek.models import *
from djcdek.cdek.client import CDEKDjangoClient


def update_regions():
    """
    Обновляет справочник регионов и стран из базы данных CDEK 
    """
    logger = logging.getLogger('cdek')

    logger.info('Update regions and countries')
    client = CDEKDjangoClient()
    page_size = 100 #размер страницы запроса
    current_page = 0
    while True:
        logger.info('Page %s' % current_page)
        response = client.get_regions(size=page_size, page=current_page)
        logger.info('Get %s elements' % len(response))
        for item in response:
            region = Region.objects.filter(title=item.get('region'), country__code=item.get('country_code')).first()
            if not region:
                country, result = Country.objects.get_or_create(title=item.get('country'), code=item.get('country_code'))
                region = Region.objects.create(
                    title=item.get('region'),
                    country=country,
                    kladr_region_code=item.get('kladr_region_code'),
                    fias_region_guid=item.get('fias_region_guid'),
                )
                logger.info('Create %s region' % region.title)
            region.code=item.get('region_code')
            region.kladr_region_code=item.get('kladr_region_code')
            region.fias_region_guid=item.get('fias_region_guid')
            region.save()
        
        current_page += 1

        if len(response) == 0:
            break


def update_cities():
    """
    Обновляет справочник населенных пунктов из базы данных CDEK 
    """
    logger = logging.getLogger('cdek')

    logger.info('Update city')
    client = CDEKDjangoClient()
    page_size = 1000 #размер страницы запроса
    current_page = 0
    while True:
        logger.info('Page %s' % current_page)
        response = client.get_cities(size=page_size, page=current_page)
        logger.info('Get %s elements' % len(response))
        for item in response:
            city = City.objects.filter(code=item.get('code')).first()
            if not city:
                region = Region.objects.filter(title=item.get('region'), country__code=item.get('country_code')).first()
                city = City.objects.create(
                    title=item.get('city'),
                    code=item.get('code'),
                    region=region,
                )
                logger.info('Create %s city' % city.title)
            city.fias_guid=item.get('fias_guid')
            city.kladr_code=item.get('kladr_code')
            city.postal_codes = ';'.join(item.get('postal_codes', [])) if item.get('postal_codes') else ''
            try:
                city.longitude =float(item.get('longitude'))
                city.latitude =float(item.get('latitude'))
            except (ValueError, TypeError):
                pass
            city.timezone = item.get('time_zone')
            try:
                city.payment_limit = float(item.get('payment_limit'))
            except (ValueError, TypeError):
                pass
            city.save()
        
        current_page += 1

        if len(response) == 0:
            break


def update_pvz():
    """
    Обновляет справочник ПВЗ из базы данных CDEK 
    """
    logger = logging.getLogger('cdek')

    logger.info('Update delivery points')
    client = CDEKDjangoClient()
    response = client.get_deliverypoints()
    logger.info('Get %s elements' % len(response))
    for item in response:
        dp = DeliveryPoint.objects.filter(code=item.get('code')).first()
        if not dp:
            dp = DeliveryPoint.objects.create(
                title=item.get('name'),
                code=item.get('code'),
            )
            logger.info('Create %s deliverypoint' % dp.title)
        
        dp.city = City.objects.filter(code=item.get('location').get('city_code')).first()
        dp.postal_сode=item.get('location').get('postal_сode')
        dp.address=item.get('location').get('address')
        dp.address_full=item.get('location').get('address_full')
        dp.address_comment=item.get('address_comment')
        dp.nearest_station=item.get('nearest_station')
        try:
            dp.longitude = float(item.get('location').get('longitude'))
            dp.latitude = float(item.get('location').get('latitude'))
        except (ValueError, TypeError, AttributeError):
            pass
        dp.work_time=item.get('work_time')
        dp.email=item.get('email')
        dp.phones=', '.join([p['number'] for p in item.get('phones', [])]) if item.get('phones') else ''
        dp.note=item.get('note')
        dp.type=item.get('type')
        dp.owner_сode=item.get('owner_сode')
        dp.take_only = bool(item.get('take_only')) if item.get('take_only') is not None else False 
        dp.is_dressing_room = bool(item.get('is_dressing_room')) if item.get('is_dressing_room') is not None else False
        dp.have_cashless = bool(item.get('have_cashless')) if item.get('have_cashless') is not None else False
        dp.have_cash = bool(item.get('have_cash')) if item.get('have_cash') is not None else False
        dp.allowed_cod = bool(item.get('allowed_cod')) if item.get('allowed_cod') is not None else False
        dp.site=item.get('site')
        dp.save()
        


