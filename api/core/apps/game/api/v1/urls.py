from django.urls import path

from . import views


app_name = 'core.apps.game'


urlpatterns = [
    path("", views.GamesListAPIView.as_view(), name='games-list'),
]
