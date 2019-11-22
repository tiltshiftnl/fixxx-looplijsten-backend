from rest_framework import serializers
from api.cases.models import Case

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ('id', 'case_id')
