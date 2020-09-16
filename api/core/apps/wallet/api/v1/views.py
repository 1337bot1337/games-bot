from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.apps.account import models as account_models
from core.apps.common.api.mixins import ExceptionHandlerMixin
from core.apps.wallet import services as wallet_services
from . import serializers as wallet_serializers


class RefillDevAPIView(GenericAPIView):
    serializer_class = wallet_serializers.RefillWalletSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class RefillAPIView(GenericAPIView):
    pass


class CheckAPIView(GenericAPIView):
    pass


class WithdrawAPIView(ExceptionHandlerMixin, GenericAPIView):
    queryset = account_models.TelegramAccount.objects.all()
    serializer_class = wallet_serializers.WithdrawWalletSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        tg_account = self.get_object()
        wallet_services.withdraw_wallet(
            tg_account=tg_account,
            amount=serializer.validated_data["amount"],
            card_number=serializer.validated_data["card_number"],
        )
        return Response(status=status.HTTP_200_OK)
