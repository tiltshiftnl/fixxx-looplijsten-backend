from rest_framework import serializers
from api.planner.const import PROJECTS, STAGES

class ListSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    number_of_lists = serializers.IntegerField(required=True)
    length_of_lists = serializers.IntegerField(required=True)
    primary_stadium = serializers.ChoiceField(required=False, choices=STAGES)
    secondary_stadia = serializers.MultipleChoiceField(required=False, choices=STAGES)
    exclude_stadia = serializers.MultipleChoiceField(required=False, choices=STAGES)


class WeekListSerializer(serializers.Serializer):
    opening_date = serializers.DateField(required=True)
    opening_reasons = serializers.MultipleChoiceField(required=True, choices=PROJECTS)
    lists = ListSerializer(required=True, many=True)
