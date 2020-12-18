import logging
import json
from typing import List, Dict, Optional, Union
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from datetime import datetime

from .exceptions import CDEKException
from .serialize import CDEKSerializable, CDEKEncoder
from .types import *


API_URL = 'http://api.cdek.ru/v2/'
APIV1_URL = 'http://api.cdek.ru/'
API_URL_TEST = 'http://api.edu.cdek.ru/v2/'
ACCESS_URL = 'oauth/token'

logger = logging.getLogger('cdek')


class CDEKClient:
    def __init__(self, client_id: str, client_secret: str, test: bool = False, account: str = None, secure_password: str = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.test = test
        self.access_token = None
        self.expires_token = 0
        self.timestamp_token = None

        self.account = account
        self.secure_password = secure_password


    def _get_api_url(self, version: str = '2') -> str:
        if version == '2':
            if self.test:
                return API_URL_TEST
            else:
                return API_URL
        elif version == '1':
            return APIV1_URL
        else:
            raise CDEKException('Invalid API version')

    def _handle_errors(self, response):
        if isinstance(response, dict):
            if response.get('errors', []):
                error = response['errors'][0]
                raise CDEKException(code=error.get('code'), message=error.get('message'))

            # обработчик ошибок 1 версии API
            if response.get('error', []):
                error = response['error'][0]
                raise CDEKException(code=error.get('code'), message=error.get('text'))

            for r in response.get('requests', []):
                if r.get('state') == 'INVALID':
                    if r.get('errors', []):
                        error = r['errors'][0]
                        raise CDEKException(code=error.get('code'), message=error.get('message'))
                    raise CDEKException(code='unknown', message='Unknown error')

    def _execute_request(self, url: str, params: dict = None, data: dict = None, method: str='GET', content_type: str='application/json', version: str = '2') -> dict:
        request_url = self._get_api_url(version=version) + url
        if params:
            request_url += '?' + urlencode(params, True)
        if method == 'GET':
            request = Request(request_url)
        elif method in ['POST', 'DELETE']:
            json_dump = data.encode() if data else None
            request = Request(request_url, data=json_dump, method=method, headers={
                'content-type': content_type,
                'content-length': len(json_dump) if json_dump else 0,
            })
        else:
            raise NotImplementedError('Unknown method %s' % method)

        if self.access_token:
            request.add_header('Authorization', 'Bearer ' + self.access_token)
        logger.debug('EXECUTE: %s %s' % (method, request.full_url))
        logger.debug('HEADERS: %s' % request.header_items())
        logger.debug('DATA: %s' % data)
        response = urlopen(request, timeout=10).read()
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
        self.timestamp_token = datetime.now().timestamp()

        if not self.access_token:
            raise CDEKException('Not authorized')

    def _execute_authorized(self, url: str, params: dict = None, data: dict = None, method: str='GET', content_type: str='application/json') -> dict:
        if not self._is_authorized():
            self.auth()
        return self._execute_request(url, params, data, method, content_type)

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

    def get_tarifflist(self, from_location: CDEKLocation, to_location: CDEKLocation, packages: CDEKPackage,
                       type: int = 1, date: Union[datetime, str] = None) -> str:
        """
        Калькулятор. Расчет по доступным тарифам
        """
        data = dict()
        data['from_location'] = from_location
        data['to_location'] = to_location
        data['packages'] = packages        
        return self._execute_authorized(
            'calculator/tarifflist', data=json.dumps(data), method='POST')

    def get_tariff(self, tarif_code:CDEKTariff ,from_location: CDEKLocation, to_location: CDEKLocation, packages: CDEKPackage,
                   type: int = 1, services: List[CDEKService] = None, date: Union[datetime, str] = None) -> str:
        """
        Калькулятор. Расчет по коду тарифа
        """
        data = dict()
        data['tariff_code'] = tarif_code        
        data['from_location'] = from_location
        data['to_location'] = to_location
        data['packages'] = packages
        data['services'] = services
        return self._execute_authorized(
            'calculator/tariff', data=json.dumps(data, cls=CDEKEncoder), method='POST')
        
    def register_order(self, request: RegisterOrderRequest) -> str:
        """ 
        Регистрирует заказ в системе CDEK 

        request -- запрос на регистрацию заказа
        return идентификатор заказа
        """
        response = self._execute_authorized('orders', data=json.dumps(request, cls=CDEKEncoder), method='POST')
        try:
            return response['entity']['uuid']
        except KeyError:
            raise CDEKException(code='nouuid', message='No entity UUID')

    def order_info(self, uuid: str) -> dict:
        """ 
        Возвращает информацию о заказе

        uuid - идентификатор заказа
        """
        return self._execute_authorized('orders/' + uuid)

    def delete_order(self, uuid: str) -> dict:
        """ 
        Удаляет заказ в системе CDEK

        uuid - идентификатор заказа
        """
        return self._execute_authorized('orders/' + uuid, method='DELETE')

    def print_request(self, uuids: List[str], copy_count: int = 2) -> str:
        """ 
        Отправляет запрос на формирование квитанций к заказу 
        
        uuids -- список идентификаторов заказов
        copy_count -- количество копий на листе
        return индентификатор квитанций
        """
        query = {
            'orders': [{'order_uuid': uuid} for uuid in uuids],
            'copy_count': copy_count,
        }
        response = self._execute_authorized('print/orders', data=json.dumps(query, cls=CDEKEncoder), method='POST')
        try:
            return response['entity']['uuid']
        except KeyError:
            raise CDEKException(code='nouuid', message='no entity uuid')

    def print_info(self, uuid: str) -> dict:
        """
        Возвращает информацию о квитанции

        uuid -- идентификатор квитанции
        return информация о кваитанции 
        """
        return self._execute_authorized('print/orders/' + uuid)

    def get_print_status(self, print_info: dict) -> CDEKPrintStatus:
        """
        Возвращает текущий статус квитанции

        print_info -- словарь с информациоей о квитанции полученный методом print_info(uuid)
        """
        try:
            statuses = print_info['entity']['statuses']
            if len(statuses) > 0:
                return CDEKPrintStatus[statuses[-1]['code']]
        except KeyError:
            raise CDEKException(code='noentity', message='no entity status')


    def get_print_url(self, print_info: dict) -> Optional[str]:
        """
        Возвращает url для скачивания квитанции

        print_info -- словарь с информациоей о квитанции полученный методом print_info(uuid)
        """
        try:
            url = print_info['entity']['url']
        except KeyError:
            return None

    def barcode_request(self, uuids: List[str], copy_count: int = 2, format: CDEKBarcodeFormat = CDEKBarcodeFormat.A4) -> str:
        """ 
        Отправляет запрос на формирование штрихкодов к заказу 
        
        uuids -- список идентификаторов заказов
        copy_count -- количество копий на листе
        return индентификатор квитанций
        """
        query = {
            'orders': [{'order_uuid': uuid} for uuid in uuids],
            'copy_count': copy_count,
            'format': format.value,
        }
        response = self._execute_authorized('print/barcodes', data=json.dumps(query, cls=CDEKEncoder), method='POST')
        try:
            return response['entity']['uuid']
        except KeyError:
            raise CDEKException(code='nouuid', message='no entity uuid')

    def barcode_info(self, uuid: str) -> dict:
        """
        Возвращает информацию о штрихкоде

        uuid -- идентификатор шртрихкода
        return информация о штрихкоде 
        """
        return self._execute_authorized('print/barcodes/' + uuid)

    def get_barcode_status(self, barcode_info: dict) -> CDEKPrintStatus:
        """
        Возвращает текущий статус штрихкода

        barcode_info -- словарь с информациоей о штрихкоде полученный методом barcode_info(uuid)
        """
        try:
            statuses = barcode_info['entity']['statuses']
            if len(statuses) > 0:
                return CDEKPrintStatus[statuses[-1]['code']]
        except KeyError:
            raise CDEKException(code='noentity', message='no entity status')


    def get_barcode_url(self, barcode_info: dict) -> Optional[str]:
        """
        Возвращает url для скачивания штрихкода

        barcode_info -- словарь с информациоей о штрихкоде полученный методом barcode_info(uuid)
        return ссылка на скачивание штрихкода
        """
        try:
            url = barcode_info['entity']['url']
        except KeyError:
            return None

    def get_delivery_price(self, request: CDEKDeliveryRequest) -> float:
        """
        DEPRECATED: Используй get_tariff

        Возвращает стоимость доставки по переданным параметрам

        request -- объект запроса доставки

        Работает по API v1
        """
        if not request.authLogin and self.account:
            request.authLogin = self.account
            request.secure = self.secure_password
        response = self._execute_request('calculator/calculate_price_by_json.php', method='POST', data=json.dumps(request, cls=CDEKEncoder), version='1')
        if 'result' in response:
            return CDEKDeliveryResponse(**response['result'])
        else:
            raise CDEKException(code='invalid response', message='Invalid delivery response')

    
