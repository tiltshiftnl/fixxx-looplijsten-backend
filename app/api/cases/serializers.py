from rest_framework import serializers
from api.cases.models import Case, Project, Stadium
from api.cases.const import STADIA, PROJECTS

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ('id', 'case_id', 'bwv_data')


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(required=True, choices=PROJECTS)

    class Meta:
        model = Project
        fields = ('name', )


class StadiumSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(required=True, choices=STADIA)

    class Meta:
        model = Stadium
        fields = ('name', )
