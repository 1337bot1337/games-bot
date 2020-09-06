from django.conf import settings
from django.contrib import admin
from django.urls import include, path


internal_api_v1_urlpatterns = [
    path('accounts/', include('core.apps.account.api.v1.urls', namespace='account'), name='account'),
    path('games/', include('core.apps.game.api.v1.urls', namespace='game'), name='game'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('internal/api/v1/', include(internal_api_v1_urlpatterns), name='internal-api-v1'),
]


if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
