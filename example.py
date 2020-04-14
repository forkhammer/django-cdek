import logging
import logging.config
import os
import pprint
import datetime
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


logConfig = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        'cdek': {
            'handler': ['console'],
            'level': 'DEBUG',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        }
    }
}
logging.config.dictConfig(logConfig)

from djcdek.client import CDEKClient, DeliveryPointType, RegisterOrderRequest, CDEKSender, \
    CDEKRecipient, CDEKPhone, CDEKPackage, CDEKItem, CDEKEncoder

client = CDEKClient('epT5FMOa7IwjjlwTc1gUjO1GZDH1M1rE', 'cYxOu9iAMZYQ1suEqfEvsHld4YQzjY0X', test=True)

# regions = client.get_regions(country_codes=['RU'], size=5, page=0)
# pprint.pprint(regions)

# cities = client.get_cities(country_codes=['RU'], size=5, page=0, payment_limit=0)
# pprint.pprint(cities)

# deliverypoints = client.get_deliverypoints(country_code='RU', dptype=DeliveryPointType.ALL)
# pprint.pprint(deliverypoints)

request = RegisterOrderRequest()
request.number = 1
request.shipment_point = 'PPK2'
request.delivery_point = 'NSK33'
request.date_invoice = datetime.datetime.now()
request.shipper_name = 'ООО Рога и копыта'
request.shipper_address = 'Петропавловск-Камчатский, ул. Бохняка, 18'
request.sender = CDEKSender(
    company = 'ООО Рога и копыта',
    name = 'Иван Петров',
    email = 'test@test.ru',
    phones = [CDEKPhone(number='+79991010333')],
)
request.recipient = CDEKRecipient(
    company = 'ИП Сидоров',
    name = 'СИДОРОВ А.В.',
    email = 'sidorov@test.ru',
    phones = [CDEKPhone(number='+799955550000')],
    packages = [CDEKPackage(
        number='1',
        weight=1000,
        length=10,
        width=10,
        height=10,
        items = [
            CDEKItem(
                name='Товар 1',
                ware_key='id1',
                cost=1000,
                weight=1000,
                amount=1,
                url='https://myshop.ru/product/1',
            )
        ]
    )]
)

response = client.register_order(request)
pprint.pprint(response)

