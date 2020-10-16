from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from core.apps.game import services as game_services


class GamesListAPIView(APIView):
    def get(self, request):

        return Response(data=game_services.get_games(), status=status.HTTP_200_OK)


class GameInfoAPIView(ListAPIView):
    lookup_field = 'tg_id'
    lookup_url_kwarg = 'tg_id'

    def list(self, request, *args, **kwargs):
        game_id = self.kwargs['game_id']
        type_game = self.kwargs['type']
        tg_id = self.kwargs['tg_id']

        game_info = game_services.get_game(game_id, tg_id, type_game)
        return Response(data=game_info, status=status.HTTP_200_OK)
