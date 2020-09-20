from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.game import services as game_services


class GamesListAPIView(APIView):
    def get(self, request):
        return Response(data=game_services.get_games(), status=status.HTTP_200_OK)
