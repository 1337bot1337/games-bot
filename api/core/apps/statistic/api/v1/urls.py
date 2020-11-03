from django.urls import path

from . import views

app_name = "core.apps.statistic"


urlpatterns = [
    path("register/", views.RegisterUserStatisticAPIView.as_view(), name="register_record_stat")
]
