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
    CDEKRecipient, CDEKPhone, CDEKPackage, CDEKItem, CDEKEncoder, CDEKMoney, CDEKTariff, CDEKService

client = CDEKClient('epT5FMOa7IwjjlwTc1gUjO1GZDH1M1rE', 'cYxOu9iAMZYQ1suEqfEvsHld4YQzjY0X', test=True)

# regions = client.get_regions(country_codes=['RU'], size=5, page=0)
# pprint.pprint(regions)

# cities = client.get_cities(country_codes=['RU'], size=5, page=0, payment_limit=0)
# pprint.pprint(cities)

# deliverypoints = client.get_deliverypoints(country_code='RU', dptype=DeliveryPointType.ALL)
# pprint.pprint(deliverypoints)

request = RegisterOrderRequest(
    # number = 1,
    tariff_code = CDEKTariff.STOCK_STOCK.value,
    shipment_point = 'PPK2',
    delivery_point = 'NSK33',
    # # date_invoice = datetime.datetime.now(),
    # shipper_name = 'ООО Рога и копыта',
    # shipper_address = 'Петропавловск-Камчатский, ул. Бохняка, 18',
    sender = CDEKSender(
        # company = 'ООО Рога и копыта',
        name = 'Иван Петров',
        # email = 'test@test.ru',
        phones = [CDEKPhone(number='79991010333')],
    ),
    recipient = CDEKRecipient(
        # company = 'ИП Сидоров',
        name = 'СИДОРОВ А.В.',
        email = 'sidorov@test.ru',
        phones = [CDEKPhone(number='799955550000')],
    ),
    services = [CDEKService(code='DELIV_WEEKEND')],
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
                payment=CDEKMoney(value=100),
                url='https://myshop.ru/product/1',
            )
        ]
    )]
)

order_uuid = client.register_order(request)
pprint.pprint(order_uuid)

# pprint.pprint(client.order_info(order_uuid))

# pprint.pprint(client.delete_order(order_uuid))

# print_uuid = client.print_request([order_uuid])
# print(print_uuid)

# print_info = client.print_info(print_uuid)
# pprint.pprint(print_info)
# print(client.get_print_status(print_info))
# print(client.get_print_url(print_info))


barcode_uuid = client.barcode_request([order_uuid])
print(barcode_uuid)

barcode_info = client.barcode_info(barcode_uuid)
pprint.pprint(barcode_info)
print(client.get_barcode_status(barcode_info))
print(client.get_barcode_url(barcode_info))

