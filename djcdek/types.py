import enum
from datetime import datetime
from typing import List, Dict, Optional, Union

from .serialize import CDEKSerializable


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


class CDEKTariff(enum.Enum):
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

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class CDEKService(CDEKSerializable):
    """ Дополнительная услуга """
    code: str = None
    """ Тип дополнительной услуги (подробнее см. приложение 4) """
    parameter: float = None
    """
    Параметр дополнительной услуги:

     - количество упаковок для услуги "Упаковка 1" (для всех типов заказа)
     - объявленная стоимость заказа для услуги "Страхование" (только для заказов с типом "доставка")
    """

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

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

    tariff_code: int = CDEKTariff.STOCK_STOCK.value
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

    def __init__(self, *args, **kwargs):
        # self.type = OrderRequestType.SHOP.value
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class CDEKPrintStatus(enum.Enum):
    """ Статусы кваитанций заказов """
    ACCEPTED = 'ACCEPTED'
    """ Запрос на формирование квитанции принят """
    PROCESSING = 'PROCESSING'
    """ Файл с квитанцией формируется """
    READY = 'READY'
    """ Файл с квитанцией и ссылка на скачивание файла сформированы """
    REMOVED = 'REMOVED'
    """ Истекло время жизни ссылки на скачивание файла с квитанцией """
    INVALID = 'INVALID'
    """ Некорректный запрос на формирование квитанции """