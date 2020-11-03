import hashlib
from urllib.parse import urlencode

from django.conf import settings


class FreeKassaApi:
    base_form_url = 'http://www.free-kassa.ru/merchant/cash.php'

    def __init__(self):
        self.merchant_id = settings.MERCHANT_ID
        self.first_secret = settings.FIRST_SECRET
        self.second_secret = settings.SECOND_SECRET

    def generate_payment_link(self, order_id, amount) -> str:

        params = {
            'm': self.merchant_id,
            'oa': amount,
            'o': order_id,
            's': self.generate_form_signature(amount, order_id),
            'i': 'rub',
            'lang': 'ru',
        }

        return self.base_form_url + "?" + urlencode(params)

    def generate_form_signature(self, amount, order_id):

        return self.__make_hash(sep=":", params=[
            str(self.merchant_id),
            str(amount),
            str(self.first_secret),
            str(order_id),
        ])

    def generate_callback_signature(self, amount, order_id):
        return self.__make_hash(sep=":", params=[
            str(self.merchant_id),
            str(amount),
            str(self.second_secret),
            str(order_id),
        ])

    def __make_hash(self, params, sep=''):

        sign = f'{sep}'.join(params)
        return hashlib.md5(sign.encode()).hexdigest()
