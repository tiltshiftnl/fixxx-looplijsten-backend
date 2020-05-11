import json

from constance.backends.database.models import Constance
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from api.cases.const import STADIA, PROJECTS
from api.planner.const import EXAMPLE_PLANNER_SETTINGS
from api.planner.serializers import PlannerSettingsSerializer
from utils.safety_lock import safety_lock


@method_decorator(safety_lock, 'list')
class ConstantsProjectsViewSet(ViewSet):
    """
    Retrieve the projects constants which are used for cases
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return JsonResponse({'constants': PROJECTS})


@method_decorator(safety_lock, 'list')
class ConstantsStadiaViewSet(ViewSet):
    """
    Retrieve the stadia constants which are used for cases
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return JsonResponse({'constants': STADIA})


@method_decorator(safety_lock, 'list')
@method_decorator(safety_lock, 'create')
class SettingsPlannerViewSet(ViewSet, CreateAPIView):
    """
    Retrieves the planner settings which are used for generating lists
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PlannerSettingsSerializer

    def list(self, request):
        planner_settings, _ = Constance.objects.get_or_create(key=settings.CONSTANCE_PLANNER_SETTINGS_KEY)
        settings_data = planner_settings.value

        if settings_data:
            # Make sure the string from constance is converted to JSON
            settings_data = json.loads(settings_data)
        else:
            # Set the default value if nothing is set, and store it
            settings_data = EXAMPLE_PLANNER_SETTINGS
            planner_settings.value = json.dumps(settings_data)
            planner_settings.save()

        return JsonResponse(settings_data)

    def create(self, request):
        data = request.data
        serializer = PlannerSettingsSerializer(data=data)
        is_valid = serializer.is_valid()

        if not is_valid:
            return JsonResponse({
                'message': 'Could not validate posted data',
                'errors': serializer.errors
            }, status=HttpResponseBadRequest.status_code)

        planner_settings, _ = Constance.objects.get_or_create(key=settings.CONSTANCE_PLANNER_SETTINGS_KEY)
        planner_settings.value = json.dumps(data)
        planner_settings.save()

        return JsonResponse(data)
