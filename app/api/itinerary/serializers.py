from rest_framework import serializers
from api.itinerary.models import Itinerary, ItineraryItem
from api.cases.models import Case

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ('id', 'address', 'postal_code', 'stadium_code', 'stadium')

class ItineraryItemSerializer(serializers.ModelSerializer):
    case = CaseSerializer(read_only=True)

    class Meta:
        model = ItineraryItem
        fields = ('id', 'case')

class ItineraryItemCreateRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryItem
        fields = ('id', )

class ItinerarySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ('id', 'user', 'items',)
