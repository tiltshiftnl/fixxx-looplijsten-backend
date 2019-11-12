from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from .models import Itinerary
from .serializers import ItinerarySerializer
# from utils.mock_readers import get_data_from_id


class ItineraryViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """
    A simple ViewSet for listing itineraries.
    """
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

class ItineraryItemViewSet(viewsets.ViewSet):
    """
    A temporary viewset for the CSV mock dump data

    """

    def retrieve(self, request, pk):
        return JsonResponse({
            # Data using the wng_id
            'bwv_hotline_bevinding': {},
            'bwv_hotline_melding': {},
            'bwv_vakantieverhuur': {},
            'import_adres': {},
            # Data using the adres_id
            'bwv_personen_hist': {},
            'bwv_personen': {},
            'import_stadia': {},
            'import_wvs': {}
        })

        # TODO: For now we'll just return an empty response

        # queryset = ItineraryItem.objects.all()
        # itinerary_item = get_object_or_404(queryset, wng_id=pk)

        # wng_id = itinerary_item.wng_id
        # adres_id = itinerary_item.adres_id

        # return JsonResponse({
        #     # Data using the wng_id
        #     'bwv_hotline_bevinding': get_data_from_id('/app/datasets/bwv_hotline_bevinding.csv', wng_id, 'wng_id'),
        #     'bwv_hotline_melding': get_data_from_id('/app/datasets/bwv_hotline_melding.csv', wng_id, 'wng_id'),
        #     'bwv_vakantieverhuur': get_data_from_id('/app/datasets/bwv_vakantieverhuur.csv', wng_id, 'wng_id'),
        #     'import_adres': get_data_from_id('/app/datasets/import_adres.csv', wng_id, 'wng_id')[0],
        #     # Data using the adres_id
        #     'bwv_personen_hist': get_data_from_id('/app/datasets/bwv_personen_hist.csv', adres_id, 'ads_id'),
        #     'bwv_personen': get_data_from_id('/app/datasets/bwv_personen.csv', adres_id, 'ads_id_wa'),
        #     'import_stadia': get_data_from_id('/app/datasets/import_stadia.csv', adres_id, 'adres_id'),
        #     'import_wvs': get_data_from_id('/app/datasets/import_wvs.csv', adres_id, '\ufeff"adres_id"')
        # })
