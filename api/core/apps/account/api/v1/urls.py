from django.urls import path

from . import views


app_name = "core.apps.account"


urlpatterns = [
    path("user/", views.RegisterUserSourceAPIView.as_view(), name="register-source"),
    path("<int:tg_id>/", views.UserCheckAPIView.as_view(), name="check-user"),
    path("ref/<int:tg_id>/", views.RefCheckAPIView.as_view(), name="check-ref"),
    path("refcount/<int:tg_id>/", views.RefCountCheckAPIView.as_view(), name="ref-count")
]
