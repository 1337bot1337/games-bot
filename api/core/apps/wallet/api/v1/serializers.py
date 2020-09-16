from django.conf import settings
from rest_framework import serializers


class RefillWalletSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField()
    amount = serializers.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        fields = (
            "tg_id",
            "amount",
        )

    @staticmethod
    def validate_tg_id(value):
        # TODO: add validation - Invalid Telegram user ID. Ensure the user has an account in the system.
        return value


class WithdrawWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        decimal_places=2, max_digits=9, min_value=0, max_value=settings.MAX_WITHDRAW_AMOUNT_PER_REQUEST
    )
    card_number = serializers.CharField(max_length=20)
