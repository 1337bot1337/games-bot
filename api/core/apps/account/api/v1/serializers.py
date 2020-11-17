from django.conf import settings
from rest_framework import serializers


class RegisterUserSourceSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField(max_value=settings.MAX_INT_VALUE)
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    source = serializers.CharField(max_length=50)

    class Meta:
        fields = (
            "tg_id",
            "user_name",
            "first_name",
            "last_name"
            "source",
        )
