from datetime import datetime
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.decorators import action

from api.itinerary.models import Itinerary, ItineraryItem, Note, ItineraryTeamMember, ItinerarySettings
from api.users.models import User
from api.itinerary.serializers import ItinerarySerializer, ItineraryItemSerializer, NoteCrudSerializer
from api.itinerary.serializers import ItineraryTeamMemberSerializer
from api.cases.models import Case, Project, Stadium

from utils.safety_lock import safety_lock

class ItineraryViewSet(
        ViewSet,
        GenericAPIView,
        DestroyModelMixin,
        CreateModelMixin
):
    """
    CRUD for itineraries and teams
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ItinerarySerializer
    queryset = Itinerary.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']

    def __get_all_itineraries__(self, user, date=None):
        itineraries = Itinerary.objects.filter(team_members__user=user)

        if date:
            itineraries = itineraries.filter(created_at=date)

        serializer = self.serializer_class(itineraries, many=True)

        return serializer.data

    def __get_date_from_query_parameter__(self, request):
        '''
        Returns a datetime date object if the query parameters contained a date
        '''
        date_string = self.request.query_params.get('created_at', None)

        if not date_string:
            return

        try:
            date = datetime.strptime(date_string, '%Y-%m-%d')
            return date
        except ValueError as e:
            raise APIException('Could not read date query parameter: {}'.format(e))

    def __get_serialized_team__(self, itinerary_pk):
        itinerary = get_object_or_404(Itinerary, pk=itinerary_pk)
        team_members = itinerary.team_members
        team_members_serialized = ItineraryTeamMemberSerializer(team_members, many=True)

        return Response({'team_members': team_members_serialized.data})

    def __replace_team_members__(self, itinerary_pk, user_ids):
        itinerary = get_object_or_404(Itinerary, pk=itinerary_pk)
        serializer = ItineraryTeamMemberSerializer(data=user_ids, many=True)

        if not serializer.is_valid():
            raise APIException('Could not add team members: {}'.format(serializer.errors))

        user_ids = [user_id.get('user').get('id') for user_id in user_ids]

        itinerary.clear_team_members()
        itinerary.add_team_members(user_ids)

    # TODO: Figure out how to add the safety lock decorator
    @action(detail=True, methods=['get', 'put'])
    def team(self, request, pk):
        if request.method == 'GET':
            return self.__get_serialized_team__(pk)

        if request.method == 'PUT':
            new_team_members = request.data.get('team_members')
            self.__replace_team_members__(pk, new_team_members)
            return self.__get_serialized_team__(pk)

    @safety_lock
    def create(self, request):
        # TODO: Cleanup and shorten this function
        # TODO: Check if we need to make this atomic
        serializer = ItinerarySerializer(data=request.data)

        if not serializer.is_valid():
            raise APIException('Could not create itinerary: {}'.format(serializer.errors))

        itinerary = Itinerary.objects.create()
        team_members = request.data.get('team_members', [])

        for team_member in team_members:
            user_id = team_member.get('user').get('id')
            user = get_object_or_404(User, id=user_id)
            ItineraryTeamMember.objects.create(itinerary=itinerary, user=user)

        settings = request.data.get('settings')
        opening_date = settings.get('opening_date')
        target_itinerary_length = settings.get('target_itinerary_length')

        projects = settings.get('projects')
        projects = [project.get('name') for project in projects]
        projects = [Project.objects.get_or_create(name=project)[0] for project in projects]

        primary_stadium = settings.get('primary_stadium').get('name')
        primary_stadium = Stadium.objects.get_or_create(name=primary_stadium)[0]

        secondary_stadia = settings.get('secondary_stadia')
        secondary_stadia = [stadium.get('name') for stadium in secondary_stadia]
        secondary_stadia = [Stadium.objects.get_or_create(name=stadium)[0] for stadium in secondary_stadia]

        exclude_stadia = settings.get('exclude_stadia')
        exclude_stadia = [stadium.get('name') for stadium in exclude_stadia]
        exclude_stadia = [Stadium.objects.get_or_create(name=stadium)[0] for stadium in exclude_stadia]

        itinerary_settings = ItinerarySettings.objects.create(
            opening_date=opening_date,
            itinerary=itinerary,
            primary_stadium=primary_stadium,
            target_itinerary_length=target_itinerary_length
        )
        itinerary_settings.projects.set(projects)
        itinerary_settings.secondary_stadia.set(secondary_stadia)
        itinerary_settings.exclude_stadia.set(exclude_stadia)

        serializer = self.serializer_class(itinerary)
        return Response(serializer.data)

    @safety_lock
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @safety_lock
    def list(self, request):
        date = self.__get_date_from_query_parameter__(request)
        user = get_object_or_404(User, id=request.user.id)
        itineraries = self.__get_all_itineraries__(user, date)

        return Response({
            'itineraries': itineraries
        })


class ItineraryItemViewSet(
        ViewSet,
        GenericAPIView,
        CreateModelMixin,
        UpdateModelMixin,
        DestroyModelMixin):
    """
    A view for adding/removing an item to a user's itinerary
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ItineraryItemSerializer

    def get_object(self):
        user = self.request.user
        itinerary = get_object_or_404(Itinerary, user=user)
        itinerary_item = ItineraryItem.objects.get(itinerary=itinerary, id=self.kwargs['pk'])
        return itinerary_item

    @safety_lock
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            raise APIException(str(e))

    @safety_lock
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @safety_lock
    def create(self, request):
        # Get the current user and it's itinerary
        user = get_object_or_404(User, id=request.user.id)
        itinerary = Itinerary.objects.get_or_create(user=user)[0]

        # Create itinerary item if the case exists
        case = Case.objects.get_or_create(case_id=request.data['id'])[0]
        position = request.data.get('position', None)

        try:
            itinerary_item = ItineraryItem.objects.create(
                itinerary=itinerary, case=case, position=position)
        except Exception as e:
            raise APIException(str(e))

        # Serialize and return data
        serializer = ItineraryItemSerializer(itinerary_item, many=False)
        return Response(serializer.data)


class NoteViewSet(
        ViewSet,
        GenericAPIView,
        CreateModelMixin,
        UpdateModelMixin,
        DestroyModelMixin):
    """
    A view for adding/updating/removing a note
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteCrudSerializer
    queryset = Note.objects.all()

    @safety_lock
    def retrieve(self, request, pk=None):
        note = get_object_or_404(self.queryset, pk=pk)
        serializer = NoteCrudSerializer(note)
        return Response(serializer.data)

    @safety_lock
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @safety_lock
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @safety_lock
    def create(self, request):
        # Get the current user and it's itinerary
        user = get_object_or_404(User, id=request.user.id)

        text = request.data['text']
        itinerary_item_id = request.data['itinerary_item']

        itinerary_item = get_object_or_404(ItineraryItem, id=itinerary_item_id)
        note = Note.objects.create(author=user, text=text, itinerary_item=itinerary_item)
        note.save()

        # Serialize and return data
        serializer = NoteCrudSerializer(note, many=False)
        return Response(serializer.data)
