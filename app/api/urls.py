from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.itinerary.views import ItineraryViewSet, CaseViewSet, TeamItineraryViewset
from api.users.views import TeamsViewset
from api.health.views import health

schema_view = get_schema_view(
    openapi.Info(title="Looplijsten API", default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'itineraries', ItineraryViewSet)
router.register(r'teams', TeamsViewset, basename='teams')
router.register(r'team-itineraries', TeamItineraryViewset, basename='team-itineraries')
router.register(r'cases', CaseViewSet, basename='case')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health),
    path('api/v1/', include(router.urls)),

    # authentication endpoints
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Swagger/OpenAPI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # the 'api-root' from django rest-frameworks default router
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('schema-swagger-ui'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
