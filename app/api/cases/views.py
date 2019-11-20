from random import randint
import json
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from utils.safety_lock import safety_lock
from api.itinerary.serializers import CaseSerializer
from api.cases.models import Case

class CaseViewSet(ViewSet):
    """
    A temporary viewset for cases with mock data
    """

    permission_classes = [IsAuthenticated]

    @safety_lock
    def retrieve(self, request, pk):
        with open('/app/datasets/case.json') as json_file:
            data = json.load(json_file)
            return JsonResponse(data)


class CaseSearchViewSet(ViewSet, GenericAPIView):
    """
    A temporary search ViewSet for listing cases

    """

    permission_classes = [IsAuthenticated]
    serializer_class = CaseSerializer

    @safety_lock
    def list(self, request):
        random_numer = randint(0, 5)
        queryset = Case.objects.all().order_by('?')[:random_numer]
        serializer = CaseSerializer(queryset, many=True)
        return Response(serializer.data)
