from django.http import JsonResponse
import json
# from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from api.itinerary.models import Itinerary
from api.itinerary.serializers import ItinerarySerializer
# from api.user.models import Team


class ItineraryViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """
    A simple ViewSet for listing itineraries.
    """
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer


class TeamItineraryViewset(viewsets.ViewSet):
    """
    A simple ViewSet for listing an itinerary of a team

    """

    def retrieve(self, request, pk=None):
        queryset = Itinerary.objects.filter(team=pk)
        serializer = ItinerarySerializer(queryset, many=True)
        return Response(serializer.data)


class CaseViewSet(viewsets.ViewSet):
    """
    A temporary viewset for cases with mock data

    """

    def retrieve(self, request, pk):
        with open('/app/datasets/case.json') as json_file:
            data = json.load(json_file)
            return JsonResponse(data)
