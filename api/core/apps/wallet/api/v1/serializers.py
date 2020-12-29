from decimal import Decimal

from django.conf import settings
from rest_framework import serializers

from core.apps.account import models as account_models
from core.apps.common import choices
from core.apps.wallet import models as wallet_models


class CheckWalletSerializer(serializers.ModelSerializer):
    withdraw_in_progress_amount = serializers.SerializerMethodField()

    class Meta:
        model = account_models.TelegramAccount
        fields = ("real_balance", "virtual_balance", "withdraw_in_progress_amount", "max_withdrawal")

    def get_withdraw_in_progress_amount(self, account: "account_models.TelegramAccount") -> Decimal:
        withdraw_requests = wallet_models.WithdrawRequest.objects.filter(
            status=choices.WithdrawRequestStatus.IN_PROGRESS, account=account
        ).values_list("amount", flat=True)
        return sum(withdraw_requests)


class RefillWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        decimal_places=2, max_digits=9, min_value=0, max_value=settings.MAX_REFILL_AMOUNT_PER_REQUEST
    )

    class Meta:
        fields = ("amount",)


class WithdrawWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        decimal_places=2, max_digits=9, min_value=0, max_value=settings.MAX_WITHDRAW_AMOUNT_PER_REQUEST
    )
    card_number = serializers.CharField(max_length=20)

    class Meta:
        fields = ("amount", "card_number",)
