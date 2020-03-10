from api.users.serializers import UserIdSerializer
from rest_framework import serializers
from api.itinerary.models import Itinerary, ItineraryItem, Note, ItineraryTeamMember, ItinerarySettings
from api.cases.serializers import CaseSerializer, ProjectSerializer, StadiumSerializer
from api.cases.models import Project, Stadium, Case

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
        fields = ('id', 'position', 'notes', 'case')

class ItineraryItemCreateSerializer(serializers.ModelSerializer):
    case_id = serializers.CharField(required=True)

    class Meta:
        model = ItineraryItem
        fields = ('itinerary', 'case_id', 'position')

    def create(self, validated_data):
        case_id = validated_data.get('case_id')
        itinerary_id = validated_data.get('itinerary')
        position = validated_data.get('position', None)

        case = Case.objects.get_or_create(case_id=case_id)[0]
        itinerary = Itinerary.objects.get(id=itinerary_id)

        itinerary_item = ItineraryItem.objects.create(case=case, itinerary=itinerary, position=position)

        return itinerary_item


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

    def __get_stadia_from_settings__(self, settings, list_name):
        ''' Returns a list of Stadium objects from settings '''
        stadia = settings.get(list_name, [])
        stadia = [stadium.get('name') for stadium in stadia]
        stadia = [Stadium.get(name=stadium) for stadium in stadia]

        return stadia

    def __get_stadium_from_settings__(self, settings, name):
        ''' Returns a single Stadium object from settings '''
        if settings.get(name, None):
            stadium = settings.get(name).get('name')
            stadium = Stadium.get(name=stadium)

            return stadium

    def __get_projects_from_settings__(self, settings):
        ''' Returns the Projects objects from settings '''
        projects = settings.get('projects', [])
        projects = [project.get('name') for project in projects]
        projects = [Project.get(name=project) for project in projects]

        return projects

    def create(self, validated_data):
        itinerary = Itinerary.objects.create()

        # Add team members to the itinerary
        team_members = validated_data.get('team_members', [])
        team_members = [team_member.get('user').get('id') for team_member in team_members]
        itinerary.add_team_members(team_members)

        settings = validated_data.get('settings')
        opening_date = settings.get('opening_date')
        target_itinerary_length = settings.get('target_itinerary_length')

        # Get the projects and stadia from settings
        projects = self.__get_projects_from_settings__(settings)
        primary_stadium = self.__get_stadium_from_settings__(settings, 'primary_stadium')
        secondary_stadia = self.__get_stadia_from_settings__(settings, 'secondary_stadia')
        exclude_stadia = self.__get_stadia_from_settings__(settings, 'exclude_stadia')

        # First create the settings
        itinerary_settings = ItinerarySettings.objects.create(
            opening_date=opening_date,
            itinerary=itinerary,
            primary_stadium=primary_stadium,
            target_itinerary_length=target_itinerary_length
        )
        # Next, add the many-to-many relations of the itinerary_Settings
        itinerary_settings.projects.set(projects)
        itinerary_settings.secondary_stadia.set(secondary_stadia)
        itinerary_settings.exclude_stadia.set(exclude_stadia)

        return itinerary

    class Meta:
        model = Itinerary
        fields = ('id', 'created_at', 'team_members', 'items', 'settings')
