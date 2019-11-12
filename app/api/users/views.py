from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from api.users.models import Team
from api.users.serializers import TeamSerializer

class TeamsViewset(viewsets.ViewSet):
    """
    A simple ViewSet for listing teams
    """

    def list(self, request):
        queryset = Team.objects.all()
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Team.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = TeamSerializer(user)
        return Response(serializer.data)
