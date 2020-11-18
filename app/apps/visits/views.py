from apps.visits.models import Observation, SuggestNextVisit, Visit
from apps.visits.serializers import (
    ObservationSerializer,
    SuggestNextVisitSerializer,
    VisitSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class VisitViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()


class ObservationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ObservationSerializer
    queryset = Observation.objects.all()


class SuggestNextVisitViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SuggestNextVisitSerializer
    queryset = SuggestNextVisit.objects.all()
