from apps.visits.models import Visit, ObservationChoices, Observation
from apps.itinerary.models import ItineraryItem
from rest_framework import serializers


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = [
            'value',
            'verbose',
        ]
    def to_representation(self, instance):
        out = {}
        out[instance.value] = instance.verbose
        return out


class ObservationChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationChoices
        fields = [
            'observations',
        ]
    def to_representation(self, instance):
        return dict((i.value, i.verbose) for i in instance.observations.all())


class VisitSerializer(serializers.ModelSerializer):
    observation_choices = ObservationChoicesSerializer(read_only=True)
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
            'observation_choices',
        ]
