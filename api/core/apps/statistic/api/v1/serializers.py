from django.conf import settings
from rest_framework import serializers


class RegisterUserStatisticSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField(max_value=settings.MAX_INT_VALUE)
    type_action = serializers.CharField(max_length=50)
    data = serializers.JSONField()

    class Meta:
        fields = (
            "tg_id",
            "type_action"
            "data",
        )
