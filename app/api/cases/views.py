from django.http import JsonResponse
import json
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from utils.safety_lock import safety_lock

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
