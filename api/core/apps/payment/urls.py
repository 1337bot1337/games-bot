from django.urls import path

from . import views


app_name = 'core.apps.payment'


urlpatterns = [
    path('callback', views.CallbackPayment.as_view(), name='callback')
]
