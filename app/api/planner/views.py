from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from utils.safety_lock import safety_lock
from api.planner.queries_planner import get_cases
from api.planner.serializers import WeekListSerializer
from api.planner.utils import sort_by_postal_code

# Create your views here.
class GenerateWeeklyItinerariesViewset(ViewSet, CreateAPIView):
    """
    A viewset for generating weekly itineraries
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WeekListSerializer

    def fill_week_list(self, cases, days):
        """
        A very crude MVP for filling the lists
        """
        for day in days:
            lists = day.get('lists')

            for list_item in lists:
                number_of_lists = list_item.get('number_of_lists')
                length_of_lists = list_item.get('length_of_lists')
                list_item['itineraries'] = []

                for i in range(number_of_lists):
                    list_cases = []

                    for x in range(length_of_lists):
                        case = cases.pop()
                        list_cases.append(case)

                    list_item['itineraries'].append(list_cases)

        return cases

    @safety_lock
    def create(self, request):
        """
        Generates a weekly planning with itineraries.
        (Note this is an MVP and very crude at the moment)
        """
        data = request.data
        serializer = WeekListSerializer(data=data)
        is_valid = serializer.is_valid()

        if not is_valid:
            return JsonResponse({
                'message': 'Could not validate posted data',
                'errors': serializer.errors
            }, status=HttpResponseBadRequest.status_code)

        # TODO: Actually use the opening_data, opening_reason and necessary parameters to get cases
        # opening_date = data.get('opening_date')
        # opening_reasons = data.get('opening_reasons')

        days = data.get('days')
        cases = get_cases()
        sorted_cases = sort_by_postal_code(cases)

        # Fills the days data with cases
        unplanned_cases = self.fill_week_list(sorted_cases, days)
        data['unplanned_cases'] = unplanned_cases

        # return the right data here
        return JsonResponse(data)
