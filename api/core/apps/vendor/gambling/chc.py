import hashlib
from decimal import Decimal
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.utils.http import urlencode
from rest_framework import status

from core.apps.vendor.exceptions import ThirdPartyVendorException


class CHCBlackPayloadMixin:
    def get_base_payload(self, transaction_id: str):
        return {
            "tr": transaction_id,
            "key": settings.CHC_BLACK_API_KEY,
        }

    def get_last_jackpot_payload(self, start: str, end: str, page: int, psize: int):
        return {
            "start": start,
            "end": end,
            "page": page,
            "psize": psize
        }

    def get_new_invoice_payload(self, amount: Decimal):
        return {
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

    base_url = "https://chcgreen.net/"
    invoice_uri = "/api/invoice/new/"
    last_jackpot_uri = "/api/last-jackpots/"

    @staticmethod
    def get_url(uri: str) -> str:
        return urljoin(CHCAPIClient.base_url, uri)

    @staticmethod
    def create_request(url: str, params: dict):
        response = requests.get(url, params=params)
        if response.status_code != status.HTTP_200_OK or not response.json()["success"]:
            raise ThirdPartyVendorException()
        return response.json()

    def create_invoice(self, transaction_id: str, amount: Decimal):
        sign_payload = {
            **self.get_base_payload(transaction_id),
            **self.get_new_invoice_payload(amount),
        }
        sign = self.build_sign(self.invoice_uri, sign_payload)
        response_data = self.create_request(
            self.get_url(self.invoice_uri), {**self.get_base_payload(transaction_id), "sign": sign}
        )
        return response_data["invoice"]

    def get_last_jackpot(self, transaction_id: str, start: str, end: str, page: int, psize: int):
        sign_payload = {
            **self.get_base_payload(transaction_id),
            **self.get_last_jackpot_payload(start, end, page, psize),
        }
        sign = self.build_sign(self.last_jackpot_uri, sign_payload)
        response_data = self.create_request(
            self.get_url(self.last_jackpot_uri), {**self.get_base_payload(transaction_id), "sign": sign}
        )
        return response_data
