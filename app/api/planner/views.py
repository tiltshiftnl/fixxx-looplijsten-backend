from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from utils.safety_lock import safety_lock
from api.planner.queries_planner import get_cases
from api.planner.serializers import WeekListSerializer
from api.planner.const import STAGES, PROJECTS, PROJECTS_WITHOUT_SAHARA, ONDERZOEK_BUITENDIENST
from api.planner.utils import sort_by_postal_code, filter_cases_with_missing_coordinates
from api.planner.clustering import postal_code_clustering
from api.planner.clustering import k_means_clustering, optics_clustering
from api.planner.const import EXAMPLE_POST
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
        return {
            'opening_reasons': PROJECTS,
            'stadia': STAGES
        }

    @safety_lock
    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data()

        opening_date = '2019-01-01'
        opening_reasons = PROJECTS_WITHOUT_SAHARA
        cases = get_cases(opening_date, opening_reasons, STAGES)

        context_data['selected_opening_date'] = opening_date
        context_data['selected_opening_reasons'] = opening_reasons
        context_data['selected_stadia'] = [ONDERZOEK_BUITENDIENST]
        context_data['cases'] = cases
        context_data['unplanned_cases'] = get_cases(opening_date, opening_reasons, STAGES)
        context_data['number_of_lists'] = 30
        context_data['length_of_lists'] = 8
        context_data['clustering_method'] = 'postal_code'

        context_data['planning'] = get_planning(EXAMPLE_POST)

        return render(request, self.template_name, context_data)

    @safety_lock
    def post(self, request, *args, **kwargs):
        opening_date = request.POST.get('opening_date')
        opening_reasons = request.POST.getlist('opening_reasons')
        number_of_lists = int(request.POST.get('number_of_lists'))
        length_of_lists = int(request.POST.get('length_of_lists'))
        clustering_method = request.POST.get('clustering_method')
        stadia = request.POST.getlist('stadia')

        cases = get_cases(opening_date, opening_reasons, stadia)
        context_data = self.get_context_data()
        context_data['cases'] = cases
        context_data['selected_opening_date'] = opening_date
        context_data['selected_opening_reasons'] = opening_reasons
        context_data['number_of_lists'] = number_of_lists
        context_data['length_of_lists'] = length_of_lists
        context_data['clustering_method'] = clustering_method
        context_data['selected_stadia'] = stadia

        # Right now we just always do postal code
        planned_cases, unplanned_cases = postal_code_clustering(number_of_lists, cases, length_of_lists)

        cases = filter_cases_with_missing_coordinates(cases)

        # clustering method here
        if clustering_method == 'postal_code':
            planned_cases, unplanned_cases = postal_code_clustering(number_of_lists, cases, length_of_lists)
        elif clustering_method == 'k_means':
            planned_cases = k_means_clustering(number_of_lists, cases)
            unplanned_cases = []
        elif clustering_method == 'optics':
            planned_cases_1, unplanned_cases_1 = optics_clustering(length_of_lists, cases)
            planned_cases_2, unplanned_cases_2 = optics_clustering(length_of_lists, unplanned_cases_1)
            planned_cases = planned_cases_1 + planned_cases_2
            unplanned_cases = unplanned_cases_2

        context_data['planned_cases'] = planned_cases
        context_data['unplanned_cases'] = unplanned_cases

        return render(request, self.template_name, context_data)
