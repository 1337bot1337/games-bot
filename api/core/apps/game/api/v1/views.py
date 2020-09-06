from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.apps.game import services as game_services
from core.apps.game.utils import GAME_LIST
from .serializers import StartGameSerializer


class GamesListAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        response_items = [{key: GAME_LIST[key]} for key in GAME_LIST.keys()]
        return Response(data=response_items, status=status.HTTP_200_OK)


class StartGameAPIView(GenericAPIView):
    serializer_class = StartGameSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        game_data = game_services.start_game(
            tg_id=serializer.validated_data["tg_id"],
            game_id=serializer.validated_data["game_id"],
            amount=serializer.validated_data["amount"],
        )
        return Response(data=game_data, status=status.HTTP_200_OK)
