from rest_framework import serializers
from api.itinerary.models import Itinerary, ItineraryItem, Note, ItineraryTeamMember, ItinerarySettings
from api.cases.serializers import CaseSerializer, ProjectSerializer, StadiumSerializer
from api.users.serializers import UserIdSerializer

class NoteCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'text', 'itinerary_item')

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'text')

class ItinerarySettingsSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    primary_stadium = StadiumSerializer()
    secondary_stadia = StadiumSerializer(many=True)
    exclude_stadia = StadiumSerializer(many=True)

    class Meta:
        model = ItinerarySettings
        fields = ('opening_date', 'target_itinerary_length', 'projects',
                  'primary_stadium', 'secondary_stadia', 'exclude_stadia')

class ItineraryItemSerializer(serializers.ModelSerializer):
    case = CaseSerializer(read_only=True)
    notes = NoteSerializer(read_only=True, many=True)

    class Meta:
        model = ItineraryItem
        fields = ('id', 'position', 'notes', 'case', 'itinerary')

class ItineraryTeamMemberSerializer(serializers.ModelSerializer):
    user = UserIdSerializer(read_only=True)

    class Meta:
        model = ItineraryTeamMember
        fields = ('id', 'user',)

class ItinerarySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(read_only=True, many=True)
    created_at = serializers.DateField(read_only=True)
    team_members = ItineraryTeamMemberSerializer(many=True)
    settings = ItinerarySettingsSerializer(read_only=True)

    class Meta:
        model = Itinerary
        fields = ('id', 'created_at', 'team_members', 'items', 'settings')
