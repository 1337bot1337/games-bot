from django.urls import path

from . import views


app_name = 'core.apps.payment'


urlpatterns = [
    path('callback', views.CallbackPayment.as_view(), name='callback'),
    path('generate/<int:tg_id>/<int:amount>/', views.GeneratePaymentLink.as_view(), name='generate payment link'),
]
