from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.apps.account import services as account_services
from .serializers import RegisterUserSourceSerializer


class RegisterUserSourceAPIView(GenericAPIView):
    serializer_class = RegisterUserSourceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_services.register_user_source(
            tg_id=serializer.validated_data["tg_id"],
            source=serializer.validated_data["source"]
        )
        return Response(status=status.HTTP_200_OK)
