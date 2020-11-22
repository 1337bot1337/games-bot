from django.conf import settings
from rest_framework import serializers


class RegisterUserStatisticSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField(max_value=settings.MAX_INT_VALUE)
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    type_action = serializers.CharField(max_length=50)
    data = serializers.JSONField()

    class Meta:
        fields = (
            "tg_id",
            "username",
            "first_name",
            "last_name",
            "type_action",
            "data",
        )
