from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect

from core.apps.account.models import TelegramAccount
from core.apps.payment.models import PaymentOrder
from core.apps.payment.freekassa.api import FreeKassaApi

from .services import generate_order_id, check_deposit


class CallbackPayment(ListAPIView):

    def post(self, request, *args, **kwargs):
        valid_deposit = check_deposit(request)

        if valid_deposit:

            order_id = int(request.data['MERCHANT_ORDER_ID'])




class GeneratePaymentLink(ListAPIView):
    def list(self, request, *args, **kwargs):
        tg_id = int(self.kwargs['tg_id'])
        amount = int(self.kwargs['amount'])

        if TelegramAccount.objects.filter(tg_id=tg_id).exists():
            client = FreeKassaApi()
            order_id = generate_order_id()
            PaymentOrder.objects.create(order_id=order_id, tg_id=tg_id, amount=amount)
            url = client.generate_payment_link(order_id, amount)

            return redirect(url)
