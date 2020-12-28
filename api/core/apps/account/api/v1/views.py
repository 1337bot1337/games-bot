from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from core.apps.account import services as account_services
from core.apps.affiliate import services as affiliate_services
from .serializers import RegisterUserSourceSerializer
from core.apps.account import models as account_models
from core.apps.affiliate import models as affiliate_models


class RegisterUserSourceAPIView(GenericAPIView):
    serializer_class = RegisterUserSourceSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            if request.data.get("referrer_id", None):
                type_bonus = "ref"
            elif serializer.validated_data["source"] != "none":
                type_bonus = "source"
            else:
                type_bonus = "none"

            if account_services.register_user_source(
                    tg_id=serializer.validated_data["tg_id"],
                    username=serializer.validated_data["username"],
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    source=serializer.validated_data["source"],
                    type_bonus=type_bonus
            ):
                if request.data.get("referrer_id", None):
                    affiliate_services.create_new_ref(int(serializer.validated_data["tg_id"]), int(request.data["referrer_id"]))
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print("reg user", e)


class UserCheckAPIView(ListAPIView):
    lookup_field = "tg_id"
    lookup_url_kwarg = "tg_id"

    def list(self, request, *args, **kwargs):
        tg_id = self.kwargs["tg_id"]
        users = [user.tg_id for user in account_models.TelegramAccount.objects.all()]
        if tg_id in users:
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class RefCheckAPIView(ListAPIView):
    lookup_field = "tg_id"
    lookup_url_kwarg = "tg_id"

    def list(self, request, *args, **kwargs):
        tg_id = self.kwargs["tg_id"]
        account = account_models.TelegramAccount.objects.get(tg_id=tg_id)
        check = affiliate_models.UserAffiliate.objects.filter(referral=account).exists()
        if check:
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class RefCountCheckAPIView(ListAPIView):
    lookup_field = "tg_id"
    lookup_url_kwarg = "tg_id"

    def list(self, request, *args, **kwargs):
        tg_id = self.kwargs["tg_id"]
        account = account_models.TelegramAccount.objects.get(tg_id=tg_id)
        refs = affiliate_models.UserAffiliate.objects.filter(referrer=account)
        count = refs.count()

        return Response(status=status.HTTP_200_OK, data={"count": count})
