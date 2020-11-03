from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


internal_api_v1_urlpatterns = [
    path('accounts/', include('core.apps.account.api.v1.urls', namespace='account'), name='account'),
    path('games/', include('core.apps.game.api.v1.urls', namespace='game'), name='game'),
    path('wallets/', include('core.apps.wallet.api.v1.urls', namespace='wallet'), name='wallet'),
    path('payment/', include('core.apps.payment.urls', namespace='payment'), name='payment'),
    path('statistic/', include('core.apps.statistic.api.v1.urls', namespace='statistic'), name='statistic'),

]


urlpatterns = [
    #path('', IndexView.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('api/v1/', include(internal_api_v1_urlpatterns), name='internal-api-v1'),
]


if settings.DEBUG:
    from django.conf.urls.static import static

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
