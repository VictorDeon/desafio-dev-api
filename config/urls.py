from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularRedocView
from .overrides import (
    ExcludedSpectacularYAMLAPIView, TokenView,
    AccessTokenRefreshView
)


urlpatterns = [
    path('schema/', ExcludedSpectacularYAMLAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('auth/', TokenView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', AccessTokenRefreshView.as_view(), name='token_refresh'),
    path('users/', include('apps.accounts.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
