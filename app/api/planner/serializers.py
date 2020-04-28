from django.conf import settings
from rest_framework import serializers
from api.cases.const import PROJECTS, STADIA

class PlannerListSettingsSerializer(serializers.Serializer):
    length_of_list = serializers.IntegerField(required=False, min_value=1, max_value=20, default=8)
    primary_stadium = serializers.ChoiceField(required=False, choices=STADIA)
    secondary_stadia = serializers.MultipleChoiceField(required=False, choices=STADIA)
    exclude_stadia = serializers.MultipleChoiceField(required=False, choices=STADIA)

    def validate_mutual_exclusivity(self, stadia_a, stadia_b, message):
        for stadium in stadia_a:
            if stadium in stadia_b:
                raise serializers.ValidationError(message)

    def validate_does_not_contain(self, stadium, stadia, message):
        if stadium in stadia:
            raise serializers.ValidationError(message)

    def validate(self, data):
        secondary_stadia = data.get('secondary_stadia', [])
        exclude_stadia = data.get('exclude_stadia', [])
        error_message = "exclude_stadia and secondary_stadia should be mutually exclusive"
        self.validate_mutual_exclusivity(secondary_stadia, exclude_stadia, error_message)

        primary_stadium = data.get('primary_stadium', None)
        if primary_stadium:
            error_message = "The primary_stadium cannot be in exclude_stadia "
            self.validate_does_not_contain(primary_stadium, exclude_stadia, error_message)

        return data

class PlannerDaySettingsSerializer(serializers.Serializer):
    day = PlannerListSettingsSerializer(required=False, many=False)
    evening = PlannerListSettingsSerializer(required=False, many=False)

class PlannerWeekSettingsSerializer(serializers.Serializer):
    monday = PlannerDaySettingsSerializer(required=True)
    tuesday = PlannerDaySettingsSerializer(required=True)
    wednesday = PlannerDaySettingsSerializer(required=True)
    thursday = PlannerDaySettingsSerializer(required=True)
    friday = PlannerDaySettingsSerializer(required=True)
    saturday = PlannerDaySettingsSerializer(required=True)
    sunday = PlannerDaySettingsSerializer(required=True)

class PlannerPostalCodeSettingsSerializer(serializers.Serializer):
    range_start = serializers.IntegerField(
        required=True,
        min_value=settings.CITY_MIN_POSTAL_CODE,
        max_value=settings.CITY_MAX_POSTAL_CODE)

    range_end = serializers.IntegerField(
        required=True,
        min_value=settings.CITY_MIN_POSTAL_CODE,
        max_value=settings.CITY_MAX_POSTAL_CODE)

    def validate(self, data):
        start_range = data.get('range_start')
        end_range = data.get('range_end')

        if end_range < start_range:
            raise serializers.ValidationError("The start range can't be higher than the end range")

        return data

class PlannerSettingsSerializer(serializers.Serializer):
    opening_date = serializers.DateField(required=True)
    projects = serializers.MultipleChoiceField(required=True, choices=PROJECTS)
    postal_code = PlannerPostalCodeSettingsSerializer(required=False)
    days = PlannerWeekSettingsSerializer(required=True)
