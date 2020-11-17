from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from core.apps.account import services as account_services
from .serializers import RegisterUserSourceSerializer
from core.apps.account.models import TelegramAccount


class RegisterUserSourceAPIView(GenericAPIView):
    serializer_class = RegisterUserSourceSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            if account_services.register_user_source(
                    tg_id=serializer.validated_data["tg_id"],
                    username=serializer.validated_data["username"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    source=serializer.validated_data["source"]
            ):
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)


class UserCheckAPIView(ListAPIView):
    lookup_field = 'tg_id'
    lookup_url_kwarg = 'tg_id'

    def list(self, request, *args, **kwargs):
        tg_id = self.kwargs['tg_id']
        users = [user.tg_id for user in TelegramAccount.objects.all()]
        if tg_id in users:
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)




