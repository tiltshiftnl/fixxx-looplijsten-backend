from rest_framework import serializers
from api.visits.models import Visit

class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = "__all__"