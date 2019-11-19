from rest_framework import serializers
from api.itinerary.models import Itinerary, ItineraryItem

class ItineraryItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ItineraryItem
        fields = ('id', 'wng_id', 'stadium', 'address', 'postal_code_area', 'postal_code_street')

class ItinerarySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ('id', 'user', 'items',)
