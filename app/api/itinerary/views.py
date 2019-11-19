from django.http import JsonResponse
import json
from rest_framework.viewsets import ViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.itinerary.models import Itinerary, ItineraryItem
from api.users.models import User
from api.itinerary.serializers import ItinerarySerializer, ItineraryItemSerializer

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
        queryset = Itinerary.objects.get_or_create(user=user)
        serializer = ItinerarySerializer(queryset, many=True)
        return Response(serializer.data)


class ItineraryItemViewSet(
        ViewSet,
        GenericAPIView,
        CreateModelMixin,
        DestroyModelMixin):
    """
    A view for adding an item to a user's itinerary
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
        serializer = ItineraryItemSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            itinerary = Itinerary.objects.get_or_create(user=user)[0]
            ItineraryItem.objects.create(itinerary=itinerary, **serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
