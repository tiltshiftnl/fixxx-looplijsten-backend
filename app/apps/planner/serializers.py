from apps.cases.serializers import Project, Stadium, StadiumLabelSerializer
from apps.planner.models import (
    DaySettings,
    PostalCodeRange,
    PostalCodeRangeSet,
    TeamSettings,
)
from apps.visits.serializers import (
    ObservationSerializer,
    SituationSerializer,
    SuggestNextVisitSerializer,
)
from django.conf import settings
from rest_framework import serializers
from rest_framework.relations import PKOnlyObject

from .const import TEAM_TYPE_SETTINGS


class PlannerListSettingsSerializer(serializers.Serializer):
    length_of_list = serializers.IntegerField(
        required=False, min_value=1, max_value=20, default=8
    )
    primary_stadium = serializers.CharField(required=False)
    secondary_stadia = serializers.ListField(required=False)
    exclude_stadia = serializers.ListField(required=False)

    def validate_mutual_exclusivity(self, stadia_a, stadia_b, message):
        for stadium in stadia_a:
            if stadium in stadia_b:
                raise serializers.ValidationError(message)

    def validate_does_not_contain(self, stadium, stadia, message):
        if stadium in stadia:
            raise serializers.ValidationError(message)

    def validate(self, data):
        secondary_stadia = data.get("secondary_stadia", [])
        exclude_stadia = data.get("exclude_stadia", [])
        error_message = (
            "exclude_stadia and secondary_stadia should be mutually exclusive"
        )
        self.validate_mutual_exclusivity(
            secondary_stadia, exclude_stadia, error_message
        )

        primary_stadium = data.get("primary_stadium", None)
        if primary_stadium:
            error_message = "The primary_stadium cannot be in exclude_stadia "
            self.validate_does_not_contain(
                primary_stadium, exclude_stadia, error_message
            )

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
        max_value=settings.CITY_MAX_POSTAL_CODE,
    )

    range_end = serializers.IntegerField(
        required=True,
        min_value=settings.CITY_MIN_POSTAL_CODE,
        max_value=settings.CITY_MAX_POSTAL_CODE,
    )

    def validate(self, data):
        range_start = data.get("range_start")
        range_end = data.get("range_end")

        if range_end < range_start:
            raise serializers.ValidationError(
                "The start range can't be higher than the end range"
            )

        return data


class PlannerSettingsSerializer(serializers.Serializer):
    opening_date = serializers.DateField(required=True)
    projects = serializers.ListField(required=True)
    postal_codes = PlannerPostalCodeSettingsSerializer(required=False, many=True)
    days = PlannerWeekSettingsSerializer(required=True)


class PostalCodeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalCodeRange
        fields = (
            "range_start",
            "range_end",
        )


class PostalCodeRangePresetSerializer(serializers.ModelSerializer):
    postal_code_ranges_presets = PostalCodeRangeSerializer(
        many=True, read_only=True, source="postal_code_ranges"
    )

    class Meta:
        model = PostalCodeRangeSet
        fields = (
            "id",
            "name",
            "postal_code_ranges_presets",
        )


class TeamTypeSerializer(serializers.DictField):
    def to_representation(self, instance):
        return TEAM_TYPE_SETTINGS.get(instance)


class StringRelatedToIdField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        instances = self.queryset.filter(name=data)
        if instances and len(instances) == 1:
            return super().to_internal_value(instances.get().id)
        else:
            raise serializers.ValidationError("Object with name: %s not found" % data)

    def to_representation(self, data):
        if isinstance(data, PKOnlyObject):
            return self.queryset.get(id=data.pk).name
        return data.name


class DaySettingsSerializer(serializers.ModelSerializer):
    projects = StringRelatedToIdField(many=True, queryset=Project.objects.all())
    primary_stadium = StringRelatedToIdField(queryset=Stadium.objects.all())
    secondary_stadia = StringRelatedToIdField(many=True, queryset=Stadium.objects.all())
    exclude_stadia = StringRelatedToIdField(many=True, queryset=Stadium.objects.all())

    class Meta:
        model = DaySettings
        fields = "__all__"


class TeamSettingsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    team_type = TeamTypeSerializer(read_only=True, required=False)
    situation_choices = serializers.ListField(read_only=True)
    observation_choices = ObservationSerializer(read_only=True, many=True)
    suggest_next_visit_choices = SuggestNextVisitSerializer(read_only=True, many=True)
    project_choices = serializers.StringRelatedField(read_only=True, many=True)
    stadia_choices = serializers.StringRelatedField(read_only=True, many=True)
    marked_stadia = StadiumLabelSerializer(read_only=True, many=True)
    settings = serializers.JSONField(required=True)
    day_settings_list = DaySettingsSerializer(read_only=True, many=True)

    class Meta:
        model = TeamSettings
        fields = (
            "id",
            "name",
            "team_type",
            "observation_choices",
            "situation_choices",
            "suggest_next_visit_choices",
            "project_choices",
            "stadia_choices",
            "marked_stadia",
            "settings",
            "day_settings_list",
        )

    def clean_projects(self, data):
        projects = self.instance.project_choices.values_list("name", flat=True)
        data["settings"]["projects"] = [
            p for p in projects if p in data["settings"]["projects"]
        ]
        return data

    def clean_stadia(self, data):
        stadia = self.instance.stadia_choices.values_list("name", flat=True)
        for k, v in data["settings"]["days"].items():
            for kk, vv in v.items():
                for stadia_set in ["secondary_stadia", "exclude_stadia"]:
                    if vv.get(stadia_set):
                        vv[stadia_set] = [s for s in stadia if s in vv[stadia_set]]
                if vv.get("primary_stadium"):
                    vv["primary_stadium"] = (
                        vv["primary_stadium"]
                        if vv["primary_stadium"] in stadia
                        else None
                    )
                    if not vv["primary_stadium"]:
                        del vv["primary_stadium"]
        return data

    def validate(self, data):
        data = super().validate(data)

        data = self.clean_projects(data)
        data = self.clean_stadia(data)

        settings = PlannerSettingsSerializer(data=data.get("settings"), required=True)
        if not settings.is_valid():
            raise serializers.ValidationError("Wrong settings format")
        return data
