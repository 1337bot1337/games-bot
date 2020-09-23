from django.conf import settings
from rest_framework import serializers


class RegisterUserSourceSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField(max_value=settings.MAX_INT_VALUE)
    source = serializers.CharField(max_length=50)

    class Meta:
        fields = (
            "tg_id",
            "source",
        )
