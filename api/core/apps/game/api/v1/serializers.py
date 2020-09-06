from django.utils.translation import gettext as _
from rest_framework import serializers

from core.apps.game.utils import GAME_LIST


class StartGameSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField()
    game_id = serializers.IntegerField()
    amount = serializers.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        fields = (
            "tg_id",
            "game_id",
            "amount",
        )

    @staticmethod
    def validate_game_id(value):
        if value not in GAME_LIST.keys():
            raise serializers.ValidationError(_("Invalid game ID. Ensure the game ID in the list of available IDs"))
        return value

    @staticmethod
    def validate_tg_id(value):
        # TODO: add validation - Invalid Telegram user ID. Ensure the user has an account in the system.
        return value
