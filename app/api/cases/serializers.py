from rest_framework import serializers
from api.cases.models import Case, Project, State
from api.cases.const import STAGES, PROJECTS

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ('id', 'case_id', 'bwv_data')


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(required=True, choices=PROJECTS)

    class Meta:
        model = Project
        fields = ('name', )

class StateSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(required=True, choices=STAGES)

    class Meta:
        model = State
        fields = ('name', )
