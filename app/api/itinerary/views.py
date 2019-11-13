from django.http import JsonResponse
import json
from rest_framework import viewsets
from rest_framework.response import Response

from api.itinerary.models import Itinerary
from api.itinerary.serializers import ItinerarySerializer

from utils.safety_lock import safety_lock


class ItineraryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing itineraries.
    """
    @safety_lock
    def list(self, request):
        queryset = Itinerary.objects.all()
        serializer = ItinerarySerializer(queryset, many=True)
        return Response(serializer.data)


class TeamItineraryViewset(viewsets.ViewSet):
    """
    A simple ViewSet for listing an itinerary of a team

    """
    @safety_lock
    def retrieve(self, request, pk=None):
        queryset = Itinerary.objects.filter(team=pk)
        serializer = ItinerarySerializer(queryset, many=True)
        return Response(serializer.data)


class CaseViewSet(viewsets.ViewSet):
    """
    A temporary viewset for cases with mock data

    """
    @safety_lock
    def retrieve(self, request, pk):
        with open('/app/datasets/case.json') as json_file:
            data = json.load(json_file)
            return JsonResponse(data)
