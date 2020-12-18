from django.conf import settings
from djcdek.client import CDEKClient
from djcdek.exceptions import CDEKException


class CDEKDjangoClient(CDEKClient):
    def __init__(self):
        if not hasattr(settings, 'CDEK_CLIENT_ID'):
            raise CDEKException(code='notsettings', message='Settings has not CDEK_CLIENT_ID param')
        if not hasattr(settings, 'CDEK_CLIENT_SECRET'):
            raise CDEKException(code='notsettings', message='Settings has not CDEK_CLIENT_SECRET param')
        if not hasattr(settings, 'CDEK_CLIENT_TEST'):
            raise CDEKException(code='notsettings', message='Settings has not CDEK_CLIENT_TEST param')
        super(CDEKDjangoClient, self).__init__(None, None, settings.CDEK_CLIENT_TEST)
        self.client_id = settings.CDEK_CLIENT_ID
        self.client_secret = settings.CDEK_CLIENT_SECRET
        self.account = getattr(settings, 'CDEK_ACCOUNT', None)
        self.secure = getattr(settings, 'CDEK_SECURE', None)

        