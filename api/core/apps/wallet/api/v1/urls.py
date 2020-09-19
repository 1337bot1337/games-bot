from django.urls import path

from . import views


app_name = 'core.apps.wallet'


urlpatterns = [
    path('<int:tg_id>/refill/', views.RefillAPIView.as_view(), name='refill'),
    path('<int:tg_id>/check/', views.CheckAPIView.as_view(), name='check'),
    path('<int:tg_id>/withdraw/', views.WithdrawAPIView.as_view(), name='withdraw'),
]
