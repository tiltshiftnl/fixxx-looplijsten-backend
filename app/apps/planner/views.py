import json

from apps.planner.models import PostalCodeRangeSet, TeamSettings
from apps.planner.serializers import (
    PlannerSettingsSerializer,
    PostalCodeRangeSetSerializer,
    TeamSettingsSerializer,
)
from constance.backends.database.models import Constance
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from settings.const import ISSUEMELDING, PROJECTS, STADIA


class ConstantsProjectsViewSet(ViewSet):
    """
    Retrieve the projects constants which are used for cases
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        return JsonResponse({"constants": PROJECTS})


class ConstantsStadiaViewSet(ViewSet):
    """
    Retrieve the stadia constants which are used for cases
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        constants_stadia = STADIA[:]
        constants_stadia.remove(ISSUEMELDING)
        return JsonResponse({"constants": constants_stadia})


class SettingsPlannerViewSet(ViewSet, CreateAPIView):
    """
    Retrieves the planner settings which are used for generating lists
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PlannerSettingsSerializer

    def list(self, request):
        planner_settings, _ = Constance.objects.get_or_create(
            key=settings.CONSTANCE_PLANNER_SETTINGS_KEY
        )
        settings_data = planner_settings.value

        if settings_data:
            # Make sure the string from constance is converted to JSON
            settings_data = json.loads(settings_data)
        else:
            # Set the default value if nothing is set, and store it
            settings_data = settings.EXAMPLE_PLANNER_SETTINGS
            planner_settings.value = json.dumps(settings_data)
            planner_settings.save()

        return JsonResponse(settings_data)

    def create(self, request):
        data = request.data
        serializer = PlannerSettingsSerializer(data=data)
        is_valid = serializer.is_valid()

        if not is_valid:
            return JsonResponse(
                {
                    "message": "Could not validate posted data",
                    "errors": serializer.errors,
                },
                status=HttpResponseBadRequest.status_code,
            )

        planner_settings, _ = Constance.objects.get_or_create(
            key=settings.CONSTANCE_PLANNER_SETTINGS_KEY
        )
        planner_settings.value = json.dumps(data)
        planner_settings.save()

        return JsonResponse(data)


class PostalCodeRangesViewSet(ModelViewSet):
    """
    A view for listing PostalCodeRangeSets
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PostalCodeRangeSetSerializer
    queryset = PostalCodeRangeSet.objects.all()


class TeamSettingsViewSet(ModelViewSet):
    """
    A view for listing/adding/updating/removing a TeamSettings
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TeamSettingsSerializer
    queryset = TeamSettings.objects.all()

    # def retrieve(self, request, pk=None):
    #     team_settings = get_object_or_404(self.queryset, pk=pk)
    #     serializer = TeamSettingsSerializer(team_settings)
    #     return Response(serializer.data)

    # TODO PlannerSettings is not defined!
    # def create(self, request):
    #     team_settings = PlannerSettings.objects.create(**request.data)
    #     team_settings.save()

    #     # Serialize and return data
    #     serializer = TeamSettingsSerializer(team_settings, many=False)
    #     return Response(serializer.data)
