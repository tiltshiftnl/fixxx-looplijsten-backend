from rest_framework import serializers
from api.itinerary.models import Itinerary, ItineraryItem
from api.cases.serializers import CaseSerializer

class ItineraryItemSerializer(serializers.ModelSerializer):
    case = CaseSerializer(read_only=True)

    class Meta:
        model = ItineraryItem
        fields = ('id', 'case')

class ItinerarySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ('id', 'user', 'items',)
