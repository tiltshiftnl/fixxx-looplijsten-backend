from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.visits.serializers import VisitSerializer
from apps.visits.models import Visit

# Create your views here.
class VisitViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()