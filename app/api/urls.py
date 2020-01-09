from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
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
router.register(r'notes', NoteViewSet, basename='search')

urlpatterns = [

    # OIDC authentication
    path('looplijsten/oidc/', include('mozilla_django_oidc.urls')),

    # Admin environment
    path('looplijsten/admin/', admin.site.urls),

    # Health check url
    path('looplijsten/health', health_default),
    path('looplijsten/health_bwv', health_bwv),

    # The API for requesting data
    path('looplijsten/api/v1/', include(router.urls)),

    # Authentication endpoints
    path('looplijsten/api-token-auth/', views.obtain_auth_token),
    path('looplijsten/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # JWT authentication endpoints
    path('looplijsten/token_obtain_pair/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('looplijsten/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger/OpenAPI documentation
    path('looplijsten/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('looplijsten/oidc-authenticate/', ObtainAuthTokenOIDC.as_view()),
    path('looplijsten/is-authenticated/', IsAuthenticatedView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
