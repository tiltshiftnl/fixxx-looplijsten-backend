from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from api.cases.views import CaseViewSet, CaseSearchViewSet
from api.fraudprediction.views import FraudPredictionScoringViewSet
from api.health.views import health_default, health_bwv
from api.itinerary.views import ItineraryViewSet, ItineraryItemViewSet, NoteViewSet
from api.planner.views import ConstantsStadiaViewSet, ConstantsProjectsViewSet, SettingsPlannerViewSet
from api.planner.views_sandbox import AlgorithmView
from api.users.views import ObtainAuthTokenOIDC, IsAuthenticatedView, UserListView
from api.visits.views import VisitViewSet

admin.site.site_header = "Wonen looplijsten"
admin.site.site_title = "Wonen looplijsten"
admin.site.index_title = "Wonen looplijsten"

api_router = DefaultRouter()
api_router.register(r'itineraries', ItineraryViewSet, basename='itinerary')
api_router.register(r'itinerary-items', ItineraryItemViewSet, basename='itinerary-item')
api_router.register(r'cases', CaseViewSet, basename='case')
api_router.register(r'search', CaseSearchViewSet, basename='search')
api_router.register(r'notes', NoteViewSet, basename='notes')
api_router.register(r'users', UserListView, basename='users')
api_router.register(r'visits', VisitViewSet, basename='visits')
api_router.register(r'constants/projects', ConstantsProjectsViewSet, basename='constants-projects')
api_router.register(r'constants/stadia', ConstantsStadiaViewSet, basename='constants-stadia')
api_router.register(r'settings/planner', SettingsPlannerViewSet, basename='settings-planner')
api_router.register(r'fraud-prediction/scoring', FraudPredictionScoringViewSet,
                    basename='fraud-prediction-score')

urlpatterns = [
                  # Admin environment
                  path('admin/', admin.site.urls),

                  # Algorithm sandbox environment
                  path('algorithm/', AlgorithmView.as_view(), name='algorithm'),

                  # Health check urls
                  path('looplijsten/health', health_default, name='health-default'),
                  path('looplijsten/health_bwv', health_bwv, name='health-bwv'),

                  # The API for requesting data
                  path('api/v1/', include(api_router.urls)),

                  # Authentication endpoint for exchanging an OIDC code for a token
                  path('api/v1/oidc-authenticate/', ObtainAuthTokenOIDC.as_view(), name='oidc-authenticate'),

                  # Endpoint for checking if user is authenticated
                  path('api/v1/is-authenticated/', IsAuthenticatedView.as_view(), name='is-authenticated'),

                  # # Swagger/OpenAPI documentation
                  path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

                  # Temporary redirect for meetup
                  path('meetup', RedirectView.as_view(url='https://meet.google.com/ags-apae-wqs')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# JSON handlers for errors
handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'
