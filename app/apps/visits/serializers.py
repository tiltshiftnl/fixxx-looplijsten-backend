from apps.visits.models import Observation, Situation, SuggestNextVisit, Visit
from rest_framework import serializers


class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = [
            "value",
            "verbose",
        ]


class SuggestNextVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestNextVisit
        fields = [
            "value",
            "verbose",
        ]


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = [
            "value",
            "verbose",
        ]


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"
