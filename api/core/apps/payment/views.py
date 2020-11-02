from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect

from core.apps.account.models import TelegramAccount
from core.apps.payment.models import PaymentOrder
from core.apps.payment.freekassa.api import FreeKassaApi

from .services import generate_order_id


class CallbackPayment(ListAPIView):

    def post(self, request, *args, **kwargs):
        remote_ip = str(request.META.get('HTTP_X_FORWARDED_FOR'))
        if remote_ip not in ('136.243.38.147', '136.243.38.149', '136.243.38.150', '136.243.38.151', '136.243.38.189', '136.243.38.108'):
            return print('HACK')

        order_id = int(request.data['MERCHANT_ORDER_ID'])
        request_sign = request.data['SIGN']

        order_query = PaymentOrder.objects.filter(order_id=order_id)
        if not order_query.exists():
            return
        order = order_query[0]
        client = FreeKassaApi()
        sign = client.generate_form_signature(order.amount, order.order_id)

        if request_sign != sign:
            return print('HACK')

        order.status = 'payed'
        order.save()


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
