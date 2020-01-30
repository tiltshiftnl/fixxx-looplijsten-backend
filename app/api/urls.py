from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.itinerary.views import ItineraryViewSet, ItineraryItemViewSet, NoteViewSet
from api.cases.views import CaseViewSet, CaseSearchViewSet
from api.health.views import health_default, health_bwv
from api.users.views import ObtainAuthTokenOIDC, IsAuthenticatedView

admin.site.site_header = "Wonen looplijsten"
admin.site.site_title = "Wonen looplijsten"
admin.site.index_title = "Wonen looplijsten"

schema_view = get_schema_view(
    openapi.Info(title="Looplijsten API", default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'itineraries', ItineraryViewSet, basename='itinerary')
router.register(r'itineraries/items', ItineraryItemViewSet, basename='itinerary-item')
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'search', CaseSearchViewSet, basename='search')
router.register(r'notes', NoteViewSet, basename='notes')

# Temporary prefix for production environment.
# Will be removed once we have all domains and subdomains ready.
prefix = 'api/' if settings.ENVIRONMENT == 'production' else ''

urlpatterns = [
    # Admin environment
    path(prefix + 'looplijsten/admin/', admin.site.urls),

    # Health check url
    path('looplijsten/health', health_default),
    path('looplijsten/health_bwv', health_bwv),

    # The API for requesting data
    path(prefix + 'looplijsten/api/v1/', include(router.urls)),

    # Authentication endpoints for exchanging user credentials for a token
    path(prefix + 'looplijsten/credentials-authenticate/',
         TokenObtainPairView.as_view(), name='credentials-authenticate'),

    # Authentication endpoint for exchanging an OIDC code for a token
    path(prefix + 'looplijsten/oidc-authenticate/', ObtainAuthTokenOIDC.as_view(), name='oidc-authenticate'),

    # Endpoint for retrieving a fresh new token
    path(prefix + 'looplijsten/token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # OIDC helper urls
    path(prefix + 'looplijsten/oidc/', include('mozilla_django_oidc.urls')),

    # Endpoint for checking if user is authenticated
    path(prefix + 'looplijsten/is-authenticated/', IsAuthenticatedView.as_view(), name='is-authenticated'),

    # Swagger/OpenAPI documentation
    path(prefix + 'looplijsten/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
