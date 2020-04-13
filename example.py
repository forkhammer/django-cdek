import logging
import logging.config
import os
import pprint

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

from djcdek.client import CDEKClient, DeliveryPointType

client = CDEKClient('epT5FMOa7IwjjlwTc1gUjO1GZDH1M1rE', 'cYxOu9iAMZYQ1suEqfEvsHld4YQzjY0X', test=True)

# regions = client.get_regions(country_codes=['RU'], size=5, page=0)
# pprint.pprint(regions)

# cities = client.get_cities(country_codes=['RU'], size=5, page=0, payment_limit=0)
# pprint.pprint(cities)

deliverypoints = client.get_deliverypoints(country_code='RU', dptype=DeliveryPointType.ALL, have_cashless=False)
pprint.pprint(deliverypoints)