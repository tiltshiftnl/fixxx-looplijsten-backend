from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from utils.safety_lock import safety_lock
from utils.queries import get_search_results, get_related_case_ids, get_rental_information
from utils.queries import get_bwv_hotline_melding, get_bwv_hotline_bevinding
from utils.queries import get_bwv_personen, get_import_adres, get_import_stadia, get_bwv_tmp
from utils.queries_bag_api import get_bag_data
from utils.queries_brk_api import get_brk_data, brk_request
from api.itinerary.serializers import CaseSerializer

class CaseViewSet(ViewSet):
    """
    A temporary viewset for cases with mock data
    """

    permission_classes = [IsAuthenticated]

    @safety_lock
    @brk_request
    def retrieve(self, request, pk):
        case_id = pk

        related_case_ids = get_related_case_ids(case_id)

        wng_id = related_case_ids.get('wng_id', None)
        adres_id = related_case_ids.get('adres_id', None)

        if not wng_id or not adres_id:
            return HttpResponseNotFound('Case not found')

        real_data = {
            'bwv_hotline_bevinding': get_bwv_hotline_bevinding(wng_id),
            'bwv_hotline_melding': get_bwv_hotline_melding(wng_id),
            'bwv_personen': get_bwv_personen(adres_id),
            'import_adres': get_import_adres(wng_id),
            'import_stadia': get_import_stadia(case_id),
            'bwv_tmp': get_bwv_tmp(case_id, adres_id),
            'vakantie_verhuur': get_rental_information(wng_id),
            'bag_data': get_bag_data(wng_id),
            'brk_data': get_brk_data()
        }
        return JsonResponse(real_data)


class CaseSearchViewSet(ViewSet, ListAPIView):
    """
    A temporary search ViewSet for listing cases
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CaseSerializer

    @safety_lock
    def list(self, request):
        postal_code = request.GET.get('postalCode', None)
        street_number = request.GET.get('streetNumber', None)
        suffix = request.GET.get('suffix', None)

        if not postal_code or not street_number:
            return Response(HttpResponseBadRequest)
        else:
            items = get_search_results(postal_code, street_number, suffix)
            return JsonResponse({'cases': items})
