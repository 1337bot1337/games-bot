from rest_framework import serializers


class RegisterUserSourceSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField()
    source = serializers.CharField(max_length=50)

    class Meta:
        fields = (
            "tg_id",
            "source",
        )
