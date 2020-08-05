from apps.visits.models import Visit
from apps.visits.serializers import VisitSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class VisitViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()
