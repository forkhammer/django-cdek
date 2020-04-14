import logging
import json
import enum
from typing import List, Dict, Optional, Union
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from datetime import datetime

API_URL = 'http://api.cdek.ru/v2/'
API_URL_TEST = 'http://api.edu.cdek.ru/v2/'
ACCESS_URL = 'oauth/token'

logger = logging.getLogger('cdek')


class CDEKException(Exception):
    def __init__(self, code:str=None, message:str=None, *args, **kwargs):
        super(CDEKException, self).__init__(*args, **kwargs)
        self.code = code
        self.message = message


class CDEKSerializable:

    @property
    def fields(self):
        return self.__dict__


class CDEKEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, CDEKSerializable):
            return json.dumps(o.fields, cls=CDEKEncoder)
        elif isinstance(o, datetime):
            return o.strftime('%Y-%m-%d')
        return super(CDEKEncoder, self).default(o)


class DeliveryPointType(enum.Enum):
    PVZ = 'PVZ'  
    """ склады СДЭК """

    POSTOMAT = 'POSTOMAT'
    """ Постоматы партнёра """

    ALL = 'ALL'
    """ Все ПВЗ """


class OrderRequestType(enum.Enum):
    """ Тип заказа """
    SHOP = 1
    """ 1 - интернет-магазин (только для договора типа "Договор с ИМ") """

    DELIVERY = 2
    """ 2 - "доставка" (для любого договора) """


class Tariff(enum.Enum):
    """ Тариф доставки """

    STOCK_STOCK = 136
    """ склад - склад """

    STOCK_HOME = 137
    """ склад  - дверь """

    HOME_STOCK = 138
    """ дверь - склад """

    HOME_HOME = 139
    """ дверь - дверь """


class CDEKMoney(CDEKSerializable):
    value: float = None
    """ Сумма """
    vat_sum: float = None
    """ Сумма НДС """
    vat_rate: int = None
    """ Ставка НДС (значение - 0, 10, 18, 20 и т.п. , null - нет НДС) """

    def __init__(self, value: float, vat_sum: float = None, vat_rate: int = None):
        self.value = value
        self.vat_sum = vat_sum
        self.vat_rate = vat_rate
    


class CDEKPhone(CDEKSerializable):
    number: str = None
    """ Номер телефона. Должен передаваться в международном формате: код страны (для России +7) и сам номер (10 и более цифр)"""
    additional: str = None
    """ Дополнительная информация (доп. номер) """

    def __init__(self, number: str, additional: str = None):
        self.number = number
        self.additional = additional


class CDEKSender(CDEKSerializable):
    """ Отправитель """

    company: str = None
    """ Название компании """
    name: str = None
    """ ФИО контактного лица """
    email: str = None
    """ Email """
    phones: List[CDEKPhone] = []

    def __init__(self, company: str = None, name: str = None, email: str = None, phones: List[CDEKPhone] = []):
        self.company = company
        self.name = name
        self.email = email
        self.phones = phones


class CDEKSeller(CDEKSerializable):
    """ Реквизиты реального продавца """
    name: str = None
    """ Наименование истинного продавца """
    inn: str = None
    """ ИНН истинного продавца """
    phone: str = None
    """ Телефон истинного продавца """
    ownership_form: int = None
    """ Код формы собственности  (подробнее см. приложение 3 https://confluence.cdek.ru/pages/viewpage.action?pageId=29923926#)"""

    def __init__(self, name: str = None, inn: str = None, phone: str = None, ownership_form: int = None):
        self.name = name
        self.inn = inn
        self.phone = phone
        self.ownership_form = ownership_form
    
    

class CDEKRecipient(CDEKSerializable):
    """ Получатель """

    company: str = None
    """ Название компании """
    name: str = None
    """ ФИО контактного лица """
    passport_series: str = None
    """ Серия паспорта """
    passport_number: str = None
    """ Номер паспорта """
    passport_date_of_issue: Union[datetime, str] = None
    """ Дата выдачи паспорта """
    passport_organization: str = None
    """ Орган выдачи паспорта """
    tin: str = None
    """ ИНН """
    passport_date_of_birth: Union[datetime, str] = None
    """ Дата рождения """
    email: str = None
    """ Email """
    phones: List[CDEKPhone] = []

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class CDEKLocation(CDEKSerializable):
    """ Местоположение """
    code: int = None
    """ Код локации СДЭК """
    fias_guid: str = None
    """ Уникальный идентификатор ФИАС """
    postal_code: str = None
    """ Почтовый индекс """
    longitude: float = None
    """ Долгота """
    latitude: float = None
    """ Широта """
    country_code: str = None
    """ Код страны в формате  ISO_3166-1_alpha-2 """
    region: str = None
    """ Название региона """
    region_code: int = None
    """ Код региона СДЭК """
    sub_region: str = None
    """ Название района региона """
    city: str = None
    """ Название города """
    kladr_code: str = None
    """ Код КЛАДР """
    address: str = None
    """ Строка адреса """


class CDEKService(CDEKSerializable):
    """ Дополнительная услуга """
    code: int = None
    """ Тип дополнительной услуги (подробнее см. приложение 4) """
    parameter: float = None
    """
    Параметр дополнительной услуги:

     - количество упаковок для услуги "Упаковка 1" (для всех типов заказа)
     - объявленная стоимость заказа для услуги "Страхование" (только для заказов с типом "доставка")
    """

class CDEKItem(CDEKSerializable):
    """ Позиции товаров в упаковке """
    name: str = None
    """ Наименование товара (может также содержать описание товара: размер, цвет) """
    ware_key: str = None
    """ Идентификатор/артикул товара """
    marking: str = None
    """ Маркировка товара. Если для товара/вложения указана маркировка, Amount не может быть больше 1. """
    payment: CDEKMoney = None
    """ Оплата за товар при получении (за единицу товара в валюте страны получателя, значение >=0) — наложенный платеж, в случае предоплаты значение = 0 """
    cost: float = None
    """ Объявленная стоимость товара (за единицу товара в валюте взаиморасчетов, значение >=0). С данного значения рассчитывается страховка """
    weight: int = None
    """ Вес (за единицу товара, в граммах) """
    weight_gross: int = None
    """ Вес брутто """
    amount: int = None
    """ Количество единиц товара (в штуках) """
    name_i18n: str = None
    """ Наименование на иностранном языке """
    brand: str = None
    """ Бренд на иностранном языке """
    country_code: str = None
    """ Код страны производителя товара в формате  ISO_3166-1_alpha-2 """
    material: int  = None
    """ Код материала (подробнее см. приложение 5) """
    wifi_gsm: bool = None
    """ Содержит wifi/gsm """
    url: str = None
    """ Ссылка на сайт интернет-магазина с описанием товара """

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class CDEKPackage(CDEKSerializable):
    """ Упаковка """
    number: str = None
    """ Номер упаковки (можно использовать порядковый номер упаковки заказа или номер заказа), уникален в пределах заказа. Идентификатор заказа в ИС Клиента """
    weight: int = None
    """ Общий вес (в граммах) """
    length: int = None
    """ Габариты упаковки. Длина (в сантиметрах) """
    width: int = None
    """ Габариты упаковки. Ширина (в сантиметрах) """
    height: int = None
    """ Габариты упаковки. Высота (в сантиметрах) """
    comment: str = None
    """ Комментарий к упаковке """
    items: List[CDEKItem] = []

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class RegisterOrderRequest(CDEKSerializable):
    type: int = OrderRequestType.SHOP.value
    """ Тип заказа """

    number: str = None
    """ Номер заказа в ИС Клиента (если не передан, будет присвоен номер заказа в ИС СДЭК - uuid) """

    tariff_code: int = Tariff.STOCK_STOCK.value
    """ Код тарифа (подробнее см. https://confluence.cdek.ru/pages/viewpage.action?pageId=29923926) """

    comment: str = None
    """ Комментарий к заказу """

    shipment_point: str = None
    """ Код ПВЗ СДЭК, на который будет производится забор отправления, либо самостоятельный привоз клиентом """

    delivery_point: str = None
    """ Код ПВЗ СДЭК, на который будет доставлена посылка """

    date_invoice: Union[datetime, str] = None
    """ Дата инвойса. Только для заказов "интернет-магазин" """

    shipper_name: str = None
    """ Грузоотправитель. Только для заказов "интернет-магазин" """

    shipper_address: str = None
    """ Адрес грузоотправителя. Только для заказов "интернет-магазин" """

    delivery_recipient_cost: CDEKMoney = None
    """ Доп. сбор за доставку, которую ИМ берет с получателя. Только для заказов "интернет-магазин" """

    sender: CDEKSender = None
    """ Отправитель """

    seller: CDEKSeller = None
    """ Реквизиты реального продавца """

    recipient: CDEKRecipient = None
    """ Получатель """

    from_location: CDEKLocation = None
    """ Адрес отправления """

    to_location: CDEKLocation = None
    """ Адрес получения """

    services: List[CDEKService] = []
    """ Дополнительные услуги """

    packages: List[CDEKPackage] = []
    """ Список информации по местам (упаковкам) """



class CDEKClient:
    def __init__(self, client_id: str, client_secret: str, test: bool = False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.test = test
        self.access_token = None
        self.expires_token = 0
        self.timestamp_token = None


    def _get_api_url(self) -> str:
        if self.test:
            return API_URL_TEST
        else:
            return API_URL_TEST

    def _handle_errors(self, response):
        if isinstance(response, dict):
            if 'code' in response:
                raise CDEKException(code=response.get('code'), message=response.get('message'))

    def _execute_request(self, url: str, params: dict = None, data: dict = None, method: str='GET') -> dict:
        request_url = self._get_api_url() + url
        if params:
            request_url += '?' + urlencode(params, True)
        if method == 'GET':
            request = Request(request_url)
        elif method == 'POST':
            request = Request(request_url, data=json.dumps(data).encode() if data else None, method='POST')
        else:
            raise NotImplementedError('Unknown method %s' % method)

        if self.access_token:
            request.add_header('Authorization', 'Bearer ' + self.access_token)
        print('EXECUTE: %s' % request.full_url)
        print('DATA: %s' % json.dumps(data))
        response = urlopen(request).read()
        # print('RESPONSE: %s' % response)
        data = json.loads(response)
        self._handle_errors(data)
        return data

    def _is_authorized(self) -> bool:
        if self.access_token and self.expires_token and self.timestamp_token:
            if datetime.now().timestamp() < self.timestamp_token + self.expires_token:
                return True
        return False

    def auth(self):
        response = self._execute_request(ACCESS_URL, params={
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }, method='POST')
        self.access_token = response.get('access_token')
        self.expires_token = int(response.get('expires_in'))
        self.timestamp_token = datetime.now().timestamp

        if not self.access_token:
            raise CDEKException('Not authorized')

    def _execute_authorized(self, url: str, params: dict = None, data: dict = None, method: str='GET') -> dict:
        if not self._is_authorized():
            self.auth()
        return self._execute_request(url, params, data, method)

    def get_regions(self, country_codes: List[str]=[], region_code: str = None, kladr_region_code: str = None,
                    fias_region_guid: str = None, size: int = None, page: int = None, lang: str = None) -> Dict[str, str]:
        """ Возвращает список регионов, в которых есть доставка """
        params = dict()
        if country_codes:
            params['country_codes'] = country_codes
        if region_code:
            params['region_code'] = region_code
        if kladr_region_code:
            params['kladr_region_code'] = kladr_region_code
        if fias_region_guid:
            params['fias_region_guid'] = fias_region_guid
        if size is not None:
            params['size'] = size
        if page is not None:
            params['page'] = page
        if lang:
            params['lang'] = lang
        return self._execute_authorized('location/regions', params=params)

    def get_cities(self, country_codes: List[str]=[], region_code: str = None, kladr_region_code: str = None,
                    fias_region_guid: str = None, kladr_code: str = None, fias_guid: str = None, 
                    postal_code: str = None, code: str = None, city: str = None, size: int = None, page: int = None, lang: str = None,
                    payment_limit: float = None) -> Dict[str, str]:
        """ Возвращает список городов, в которых есть доставка """
        params = dict()
        if country_codes:
            params['country_codes'] = country_codes
        if region_code:
            params['region_code'] = region_code
        if kladr_region_code:
            params['kladr_region_code'] = kladr_region_code
        if fias_region_guid:
            params['fias_region_guid'] = fias_region_guid
        if kladr_code:
            params['kladr_code'] = kladr_code
        if fias_guid:
            params['fias_guid'] = fias_guid
        if postal_code:
            params['postal_code'] = postal_code
        if code:
            params['code'] = code
        if city:
            params['city'] = city
        if size is not None:
            params['size'] = size
        if page is not None:
            params['page'] = page
        if lang:
            params['lang'] = lang
        if payment_limit is not None:
            params['payment_limit'] = payment_limit
        return self._execute_authorized('location/cities', params=params)

    def get_deliverypoints(self, postal_code: str = None, city_code: str = None, dptype: DeliveryPointType = None,
                        country_code:str = None, region_code: str = None, have_cashless: bool = None,
                        have_cash: bool = None, allowed_cod: bool = None, is_dressing_room: bool = None,
                        weight_max: float = None, weight_min: float = None, lang: str = None, take_only: bool = None) -> Dict[str, str]:
        """ 
        Возвращает список пунктов выдачи заказов

        postal_code -- Почтовый индекс города, для которого необходим список ПВЗ
        city_code -- Код города по базе СДЭК 
        dptype -- Тип пункта выдачи
        country_code -- Код страны в формате ISO_3166-1_alpha-2
        region_code -- Код региона по базе СДЭК
        have_cashless -- Наличие терминала оплаты
        have_cash -- Есть прием наличных
        allowed_cod -- Разрешен наложенный платеж
        is_dressing_room -- Наличие примерочной
        weight_max -- Максимальный вес в кг, который может принять ПВЗ 
            (значения больше 0  - передаются ПВЗ, которые принимают этот вес; 0 - все ПВЗ; 
            значение не указано - ПВЗ с нулевым весом не передаются).
        lang -- Локализация ПВЗ. По умолчанию "rus".
        take_only -- Является ли ПВЗ только пунктом выдачи
        """
        params = dict()
        if postal_code:
            params['postal_code'] = postal_code
        if city_code:
            params['city_code'] = city_code
        if dptype:
            params['type'] = dptype.value
        if country_code:
            params['country_code'] = country_code
        if region_code:
            params['region_code'] = region_code
        if have_cashless is not None:
            params['have_cashless'] = str(have_cashless)
        if have_cash is not None:
            params['have_cash'] = str(have_cash)
        if allowed_cod is not None:
            params['allowed_cod'] = str(allowed_cod)
        if is_dressing_room is not None:
            params['is_dressing_room'] = str(is_dressing_room)
        if weight_max is not None:
            params['weight_max'] = weight_max
        if weight_min is not None:
            params['weight_min'] = weight_min
        if lang:
            params['lang'] = lang
        if take_only is not None:
            params['take_only'] = str(take_only)
        return self._execute_authorized('deliverypoints', params=params)

    def register_order(self, request: RegisterOrderRequest):
        return self._execute_authorized('orders', data=json.dumps(request, cls=CDEKEncoder), method='POST')


    