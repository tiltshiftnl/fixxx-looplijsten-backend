from rest_framework import serializers
from api.users.models import Team, User

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'members',)
