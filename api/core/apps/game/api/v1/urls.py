from django.urls import path

from . import views


app_name = 'core.apps.game'


urlpatterns = [
    path("", views.GamesListAPIView.as_view(), name='games-list'),
    path("<int:game_id>/<str:type>/<int:tg_id>/", views.GameInfoAPIView.as_view(), name='game-info')
]
