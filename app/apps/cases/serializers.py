from apps.cases.const import PROJECTS, STADIA
from apps.cases.models import Case, Project, Stadium
from apps.fraudprediction.serializers import FraudPredictionSerializer
from rest_framework import serializers


class CaseSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ("case_id",)


class CaseSerializer(serializers.ModelSerializer):
    fraud_prediction = FraudPredictionSerializer(required=False, read_only=True)

    class Meta:
        model = Case
        fields = ("id", "case_id", "bwv_data", "fraud_prediction")


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(required=True, choices=PROJECTS)

    class Meta:
        model = Project
        fields = ("name",)


class StadiumSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(required=True, choices=STADIA)

    class Meta:
        model = Stadium
        fields = ("name",)


class UnplannedCasesSerializer(serializers.Serializer):
    """
    Serializer used to validate coming in from the unplanned-cases view
    """

    date = serializers.DateField(required=True)
    stadium = serializers.ChoiceField(required=True, choices=STADIA)


class PermitCheckmarkSerializer(serializers.Serializer):
    has_b_and_b_permit = serializers.BooleanField()
    has_vacation_rental_permit = serializers.BooleanField()
