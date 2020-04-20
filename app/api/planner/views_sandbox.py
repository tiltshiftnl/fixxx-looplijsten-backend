from types import SimpleNamespace
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from constance.backends.database.models import Constance

from utils.safety_lock import safety_lock
from api.planner.serializers import WeekListSerializer
from api.cases.const import STADIA, PROJECTS, PROJECTS_WITHOUT_SAHARA
from api.planner.const import SCORING_WEIGHTS
from api.planner.algorithm.knapsack import ItineraryKnapsackList
from api.planner.utils import remove_cases_from_list

class AlgorithmView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    template_name = 'body.html'

    def get_context_data(self):
        key, _ = Constance.objects.get_or_create(key=settings.CONSTANCE_MAPS_KEY)
        return {
            'projects': PROJECTS,
            'selected_projects': PROJECTS_WITHOUT_SAHARA,
            'stadia': STADIA,
            'selected_stadia': [],
            'main_stadium': None,
            'selected_exclude_stadia': [],
            'selected_opening_date': '2019-01-01',
            'number_of_lists': 1,
            'length_of_lists': 8,
            'maps_key': key.value,
            'weight_distance': SCORING_WEIGHTS.DISTANCE.value,
            'weight_fraud_probability': SCORING_WEIGHTS.FRAUD_PROBABILITY.value,
            'weight_primary_stadium': SCORING_WEIGHTS.PRIMARY_STADIUM.value,
            'weight_secondary_stadium': SCORING_WEIGHTS.SECONDARY_STADIUM.value,
            'weight_issuemelding': SCORING_WEIGHTS.ISSUEMELDING.value,
            'start_case_id': '',
        }

    @safety_lock
    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data()

        settings = SettingsMock(context_data)
        generator = ItineraryKnapsackList(settings)
        unplanned_cases = generator.__get_eligible_cases__()

        context_data['planning'] = {
            'planned_cases': [],
            'unplanned_cases': unplanned_cases,
        }

        return render(request, self.template_name, context_data)

    @safety_lock
    def post(self, request, *args, **kwargs):
        opening_date = request.POST.get('opening_date')
        projects = request.POST.getlist('projects')
        length_of_lists = int(request.POST.get('length_of_lists'))
        stadia = request.POST.getlist('stadia')
        exclude_stadia = request.POST.getlist('exclude_stadia')
        main_stadium = request.POST.get('main_stadium')
        start_case_id = request.POST.get('start_case_id', '')

        weight_distance = float(request.POST.get('weight_distance'))
        weight_fraud_probability = float(request.POST.get('weight_fraud_probability'))
        weight_primary_stadium = float(request.POST.get('weight_primary_stadium'))
        weight_secondary_stadium = float(request.POST.get('weight_secondary_stadium'))
        weight_issuemelding = float(request.POST.get('weight_issuemelding'))

        context_data = self.get_context_data()
        context_data['selected_opening_date'] = opening_date
        context_data['selected_projects'] = projects
        context_data['length_of_lists'] = length_of_lists
        context_data['selected_stadia'] = stadia
        context_data['selected_exclude_stadia'] = exclude_stadia
        context_data['main_stadium'] = main_stadium
        context_data['weight_distance'] = weight_distance
        context_data['weight_fraud_probability'] = weight_fraud_probability
        context_data['weight_primary_stadium'] = weight_primary_stadium
        context_data['weight_secondary_stadium'] = weight_secondary_stadium
        context_data['weight_issuemelding'] = weight_issuemelding
        context_data['start_case_id'] = start_case_id

        post = {
            "opening_date": opening_date,
            "projects": projects,
            "lists": [
                {
                    "length_of_lists": length_of_lists,
                    "number_of_lists": 1,
                    "secondary_stadia": stadia,
                    "exclude_stadia": exclude_stadia,
                }
            ]
        }

        if main_stadium:
            post["lists"][0]["primary_stadium"] = main_stadium

        serializer = WeekListSerializer(data=post)
        is_valid = serializer.is_valid()
        if not is_valid:
            return JsonResponse({
                'message': 'Could not validate posted data',
                'errors': serializer.errors
            }, status=HttpResponseBadRequest.status_code)

        settings = SettingsMock(context_data)
        settings_weights = SettingsWeightMock(context_data)

        generator = ItineraryKnapsackList(settings, settings_weights)

        eligible_cases = generator.__get_eligible_cases__()
        planned_cases = generator.generate()
        unplanned_cases = remove_cases_from_list(eligible_cases, planned_cases)

        context_data['planning'] = {
            'planned_cases': planned_cases,
            'unplanned_cases': unplanned_cases
        }

        return render(request, self.template_name, context_data)


class SettingsWeightMock(SimpleNamespace):
    '''
    Creates a mock settings weight objects using context data. Should only be used for prototyping.
    '''

    def __init__(self, context):
        super().__init__()
        self.distance = context['weight_distance']
        self.fraud_probability = context['weight_fraud_probability']
        self.primary_stadium = context['weight_primary_stadium']
        self.secondary_stadium = context['weight_secondary_stadium']
        self.issuemelding = context['weight_issuemelding']


class SettingsMock(SimpleNamespace):
    '''
    Creates a mock settings objects using context data. Should only be used for prototyping.
    '''

    def __init__(self, context):
        super().__init__()
        self.opening_date = context['selected_opening_date']
        self.target_length = context['length_of_lists']

        self.projects = SimpleNamespace()
        self.projects.all = lambda: [SimpleNamespace(name=project)
                                     for project in context['selected_projects']]

        if context.get('main_stadium', None):
            self.primary_stadium = SimpleNamespace(name=context['main_stadium'])

        self.secondary_stadia = SimpleNamespace()
        self.secondary_stadia.all = lambda: [SimpleNamespace(
            name=project) for project in context['selected_stadia']]

        self.exclude_stadia = SimpleNamespace()
        self.exclude_stadia.all = lambda: [SimpleNamespace(name=project)
                                           for project in context['selected_exclude_stadia']]

        self.start_case = SimpleNamespace()
        self.start_case.case_id = context['start_case_id']
