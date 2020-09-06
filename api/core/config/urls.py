from django.conf import settings
from django.contrib import admin
from django.urls import include, path


api_v1_urlpatterns = [
    path('accounts/', include('core.apps.account.api.v1.urls', namespace='account'), name='account'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_urlpatterns), name='api-v1'),
]

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
