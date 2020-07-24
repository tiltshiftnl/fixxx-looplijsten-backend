from rest_framework.viewsets import ViewSet
from rest_framework.generics import (
    ListCreateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from api.visits.serializers import VisitSerializer
from api.visits.models import Visit

# Create your views here.
class VisitViewSet(ViewSet, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()