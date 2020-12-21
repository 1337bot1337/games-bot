from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import redirect
from django.conf import settings
from core.apps.game import services as game_services
from core.apps.statistic import services as statistic_services
import urllib
from core.apps.game.utils import GAME_LIST
from core.apps.account import models as account_models


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
        account = account_models.TelegramAccount.objects.get(tg_id=int(tg_id))
        game_info = game_services.get_game(game_id, tg_id, type_game)

        if game_info['url']:
            url = urllib.parse.quote(game_info['url'], safe='https://chcplay.net?p=')
            statistic_services.register_statistic(tg_id=tg_id,
                                                  username=account.username,
                                                  first_name=account.first_name,
                                                  last_name=account.last_name,
                                                  type_action='start_game',
                                                  data={"game_id": game_id, "name": GAME_LIST[int(game_id)],"type_game": type_game})
            return redirect(url)
        else:
            return redirect(f'https://t.me/{settings.BOT_USERNAME}')
            #return Response(data={'error_text': game_info['err_text']}, status=status.HTTP_409_CONFLICT)
