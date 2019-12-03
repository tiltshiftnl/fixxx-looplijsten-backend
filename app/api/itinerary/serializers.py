from rest_framework import serializers
from api.itinerary.models import Itinerary, ItineraryItem, Note
from api.cases.serializers import CaseSerializer

class NoteCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'text', 'itinerary_item')

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'text')

class ItineraryItemSerializer(serializers.ModelSerializer):
    case = CaseSerializer(read_only=True)
    notes = NoteSerializer(read_only=True, many=True)

    class Meta:
        model = ItineraryItem
        fields = ('id', 'case', 'notes', 'position')

class ItinerarySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(read_only=True, many=True)

    class Meta:
        model = Itinerary
        fields = ('id', 'user', 'items',)
