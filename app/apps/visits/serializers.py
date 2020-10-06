from apps.visits.models import Visit, Observation, Situation, SuggestNextVisit, ChoiceItem
from apps.itinerary.models import ItineraryItem
from rest_framework import serializers


class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = [
            'value',
            'verbose',
        ]

class SuggestNextVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestNextVisit
        fields = [
            'value',
            'verbose',
        ]

class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = [
            'value',
            'verbose',
        ]


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = [
            'id',
            'situation',
            'observations',
            'itinerary_item',
            'author',
            'start_time',
            'description',
            'can_next_visit_go_ahead',
            'can_next_visit_go_ahead_description',
            'suggest_next_visit',
            'suggest_next_visit_description',
            'personal_notes',
        ]
