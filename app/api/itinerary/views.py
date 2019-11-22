from rest_framework.viewsets import ViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from api.itinerary.models import Itinerary, ItineraryItem
from api.users.models import User
from api.itinerary.serializers import ItinerarySerializer, ItineraryItemSerializer
from api.cases.models import Case

from utils.safety_lock import safety_lock

class ItineraryViewSet(ViewSet, GenericAPIView):
    """
    A simple ViewSet for listing an itinerary of a user

    """

    permission_classes = [IsAuthenticated]
    serializer_class = ItinerarySerializer

    @safety_lock
    def list(self, request):
        user = User.objects.get(id=request.user.id)
        queryset = Itinerary.objects.get_or_create(user=user)[0]
        serializer = ItinerarySerializer(queryset, many=False)
        return Response(serializer.data)


class ItineraryItemViewSet(
        ViewSet,
        GenericAPIView,
        CreateModelMixin,
        DestroyModelMixin):
    """
    A view for adding/removing an item to a user's itinerary
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ItineraryItemSerializer

    def get_object(self):
        user = self.request.user
        itinerary = Itinerary.objects.get(user=user)
        itinerary_item = ItineraryItem.objects.get(itinerary=itinerary, id=self.kwargs['pk'])
        return itinerary_item

    @safety_lock
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @safety_lock
    def create(self, request):
        # Get the current user and it's itinerary
        user = User.objects.get(id=request.user.id)
        itinerary = Itinerary.objects.get_or_create(user=user)[0]

        # Create itinerary item if the case exists
        case = get_object_or_404(Case, id=request.data['id'])
        itinerary_item = ItineraryItem.objects.create(itinerary=itinerary, case=case)
        itinerary_item.save()

        # Serialize and return data
        serializer = ItineraryItemSerializer(itinerary_item, many=False)
        return Response(serializer.data)
