from rest_framework import serializers
from api.planner.const import PROJECTS

DAYS = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]

class ListSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    number_of_lists = serializers.IntegerField(required=True)
    length_of_lists = serializers.IntegerField(required=True)

class DaySerializer(serializers.Serializer):
    day = serializers.ChoiceField(choices=DAYS)
    lists = ListSerializer(required=True, many=True)

class WeekListSerializer(serializers.Serializer):
    opening_date = serializers.DateField(required=True)
    opening_reasons = serializers.MultipleChoiceField(required=True, choices=PROJECTS)
    # TODO: Better validation for days (optional, since we're probably removing the weekplanning anyways).
    days = DaySerializer(required=True, many=True)
