from django.urls import path

from . import views


app_name = 'core.apps.wallet'


urlpatterns = [
    path('refill-dev/', views.RefillDevAPIView.as_view(), name='refill-dev'),
    path('refill/', views.RefillAPIView.as_view(), name='refill'),
    path('check/', views.CheckAPIView.as_view(), name='check'),
    path('withdraw/<int:pk>/', views.WithdrawAPIView.as_view(), name='withdraw'),
]
