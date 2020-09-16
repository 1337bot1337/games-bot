from django.urls import path

from . import views


app_name = 'core.apps.wallet'


urlpatterns = [
    path('<int:pk>/refill/', views.RefillAPIView.as_view(), name='refill'),
    path('<int:pk>/check/', views.CheckAPIView.as_view(), name='check'),
    path('<int:pk>/withdraw/', views.WithdrawAPIView.as_view(), name='withdraw'),
]
