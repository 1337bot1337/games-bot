from django.urls import path

from . import views


app_name = 'core.apps.account'


urlpatterns = [
    path('user/', views.RegisterUserSourceAPIView.as_view(), name='register-source'),
]
