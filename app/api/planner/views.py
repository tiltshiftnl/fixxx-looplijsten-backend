from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from constance.backends.database.models import Constance

from utils.safety_lock import safety_lock
from api.planner.serializers import WeekListSerializer
from api.planner.const import STAGES, PROJECTS, PROJECTS_WITHOUT_SAHARA, ONDERZOEK_BUITENDIENST
from api.planner.algorithm import get_planning

class GenerateWeeklyItinerariesViewset(ViewSet, CreateAPIView):
    """
    A viewset for generating weekly itineraries
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WeekListSerializer

    @safety_lock
    def create(self, request):
        """
        Generates a weekly planning with itineraries.
        """
        data = request.data
        serializer = WeekListSerializer(data=data)
        is_valid = serializer.is_valid()

        if not is_valid:
            return JsonResponse({
                'message': 'Could not validate posted data',
                'errors': serializer.errors
            }, status=HttpResponseBadRequest.status_code)

        data = get_planning(data)
        return JsonResponse(data)


class AlgorithmView(LoginRequiredMixin, View):
    login_url = '/looplijsten/admin/login/'
    template_name = 'body.html'

    def get_context_data(self):
        key, _ = Constance.objects.get_or_create(key=settings.CONSTANCE_MAPS_KEY)

        return {
            'opening_reasons': PROJECTS,
            'stadia': STAGES,
            'selected_stadia': [],
            'main_stadium': ONDERZOEK_BUITENDIENST,
            'selected_exclude_stadia': [],
            'number_of_lists': 2,
            'length_of_lists': 8,
            'maps_key': key.value
        }

    @safety_lock
    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data()

        opening_date = '2019-01-01'
        opening_reasons = PROJECTS_WITHOUT_SAHARA
        context_data['selected_opening_date'] = opening_date
        context_data['selected_opening_reasons'] = opening_reasons

        return render(request, self.template_name, context_data)

    @safety_lock
    def post(self, request, *args, **kwargs):
        opening_date = request.POST.get('opening_date')
        opening_reasons = request.POST.getlist('opening_reasons')
        number_of_lists = int(request.POST.get('number_of_lists'))
        length_of_lists = int(request.POST.get('length_of_lists'))
        stadia = request.POST.getlist('stadia')
        exclude_stadia = request.POST.getlist('exclude_stadia')
        main_stadium = request.POST.get('main_stadium')

        context_data = self.get_context_data()
        context_data['selected_opening_date'] = opening_date
        context_data['selected_opening_reasons'] = opening_reasons
        context_data['number_of_lists'] = number_of_lists
        context_data['length_of_lists'] = length_of_lists
        context_data['selected_stadia'] = stadia
        context_data['selected_exclude_stadia'] = exclude_stadia
        context_data['main_stadium'] = main_stadium

        post = {
            "opening_date": opening_date,
            "opening_reasons": opening_reasons,
            "lists": [
                {
                    "number_of_lists": number_of_lists,
                    "length_of_lists": length_of_lists,
                    "primary_stadium": main_stadium,
                    "secondary_stadia": stadia,
                    "exclude_stadia": exclude_stadia,
                }
            ]
        }

        context_data['planning'] = get_planning(post)

        return render(request, self.template_name, context_data)
