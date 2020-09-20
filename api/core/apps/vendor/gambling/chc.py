import hashlib
from decimal import Decimal
from urllib.parse import urljoin
from uuid import uuid4

import requests
from django.conf import settings
from django.utils.http import urlencode
from rest_framework import status

from core.apps.vendor.exceptions import ThirdPartyVendorException


def append_transaction(func):
    def inner(*args, **kwargs):
        transaction_id = kwargs.get("transaction_id", None)
        if not transaction_id:
            transaction_id = str(uuid4())
        kwargs.update(transaction_id=transaction_id)
        return func(*args, **kwargs)
    return inner


class CHCBlackPayloadMixin:
    @staticmethod
    def get_base_payload(transaction_id: str):
        return {
            "tr": transaction_id,
            "key": settings.CHC_BLACK_API_KEY,
        }

    @staticmethod
    def get_last_jackpot_payload(start: str, end: str, page: int, psize: int):
        return {
            "start": start,
            "end": end,
            "page": page,
            "psize": psize,
        }

    @staticmethod
    def get_new_invoice_payload(amount: Decimal):
        return {
            "sum": amount,
        }

    @staticmethod
    def get_check_invoice_payload(invoice_id: str):
        return {
            "invoice": invoice_id,
        }

    get_close_invoice_payload = get_check_invoice_payload

    @staticmethod
    def get_add_invoice_payload(invoice_id: str, amount: Decimal):
        return {
            "invoice": invoice_id,
            "sum": amount,
        }


class SignBuilderMixin:
    @staticmethod
    def build_sign(uri: str, sign_payload: dict):
        """
        >>> SignBuilderMixin.build_sign("/api/invoice/new/", {"tr": "555", "key": "gmi6ea7", "sum": Decimal(100)})
        '5e4fe46797002cd375ba273b183558f3'
        """
        api_uri = "?".join([uri, urlencode(sign_payload)])
        bytes_hash_payload = f"{api_uri}:{settings.CHC_BLACK_SECRET_KEY}".encode("utf-8")
        return hashlib.md5(bytes_hash_payload).hexdigest()


class CHCAPIClient(CHCBlackPayloadMixin, SignBuilderMixin):

    base_url = "https://chcgreen.net"
    add_invoice_uri = "/api/invoice/add"
    create_invoice_uri = "/api/invoice/new/"
    check_invoice_uri = "/api/invoice/check"
    close_invoice_uri = "/api/invoice/close"
    last_jackpot_uri = "/api/last-jackpots/"

    @staticmethod
    def get_url(uri: str) -> str:
        return urljoin(CHCAPIClient.base_url, uri)

    @staticmethod
    def create_request(url: str, params: dict = None):
        response = requests.get(url, params=params)
        if response.status_code != status.HTTP_200_OK or not response.json()["success"]:
            raise ThirdPartyVendorException()
        return response.json()

    @append_transaction
    def get_last_jackpot(self, start: str, end: str, page: int, psize: int, *, transaction_id: str = None):
        """ Test method. """
        sign_payload = {
            **self.get_base_payload(transaction_id),
            **self.get_last_jackpot_payload(start, end, page, psize),
        }
        sign = self.build_sign(self.last_jackpot_uri, sign_payload)
        response_data = self.create_request(
            self.get_url(self.last_jackpot_uri), {**sign_payload, "sign": sign}
        )
        return response_data, transaction_id

    @append_transaction
    def create_invoice(self, amount: Decimal, *, transaction_id: str = None):
        sign_payload = {
            **self.get_base_payload(transaction_id),
            **self.get_new_invoice_payload(amount),
        }
        sign = self.build_sign(self.create_invoice_uri, sign_payload)
        response_data = self.create_request(
            self.get_url(self.create_invoice_uri), {**sign_payload, "sign": sign}
        )
        return response_data["invoice"], transaction_id

    @append_transaction
    def check_invoice(self, invoice_id: str, *, transaction_id: str = None):
        sign_payload = {
            **self.get_base_payload(transaction_id),
            **self.get_check_invoice_payload(invoice_id),
        }
        sign = self.build_sign(self.check_invoice_uri, sign_payload)
        response_data = self.create_request(
            self.get_url(self.check_invoice_uri), {**sign_payload, "sign": sign}
        )
        return response_data["sum"], transaction_id

    @append_transaction
    def close_invoice(self, invoice_id: str, *, transaction_id: str = None):
        sign_payload = {
            **self.get_base_payload(transaction_id),
            **self.get_close_invoice_payload(invoice_id),
        }
        sign = self.build_sign(self.close_invoice_uri, sign_payload)
        response_data = self.create_request(
            self.get_url(self.close_invoice_uri), {**sign_payload, "sign": sign}
        )
        return response_data["sum"], transaction_id

    @append_transaction
    def add_invoice(self, invoice_id: str, amount: Decimal, *, transaction_id: str = None):
        sign_payload = {
            **self.get_base_payload(transaction_id),
            **self.get_add_invoice_payload(invoice_id, amount),
        }
        sign = self.build_sign(self.add_invoice_uri, sign_payload)
        response_data = self.create_request(
            self.get_url(self.add_invoice_uri), {**sign_payload, "sign": sign}
        )
        return response_data["sum"], transaction_id


def get_game_url(
    invoice_id: str,
    game_id: int,
    menu_exit: str = "close",
    game_exit: str = "close",
    back_url: str = "https://push.money"
):
    base_url = "https://chcplay.net"
    payload = {
        "login_code": f"[[{invoice_id}]]",
        "game_id": game_id,
        "menu_exit": f"[[{menu_exit}]]",
        "game_exit": f"[[{game_exit}]]",
        "toolbar": ["quality", "full+screen"],
        "back_url": back_url,
    }
    str_payload = str(payload).replace("\'", "\"")
    return "?p=".join([base_url, str_payload])
