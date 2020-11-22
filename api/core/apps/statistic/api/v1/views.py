from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import RegisterUserStatisticSerializer
from core.apps.statistic import services as statistic_services


class RegisterUserStatisticAPIView(GenericAPIView):
    serializer_class = RegisterUserStatisticSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if statistic_services.register_statistic(
                tg_id=serializer.validated_data["tg_id"],
                username=serializer.validated_data["username"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                type_action=serializer.validated_data["type_action"],
                data=serializer.validated_data["data"],
        ):
            return Response(status=status.HTTP_200_OK)
