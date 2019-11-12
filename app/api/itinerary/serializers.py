from rest_framework import serializers
from api.itinerary.models import Itinerary, ItineraryItem

class ItineraryItemSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='case-detail',
    #     lookup_field='wng_id',
    #     lookup_url_kwarg='pk'
    # )

    class Meta:
        model = ItineraryItem
        fields = ('wng_id', 'stadium', 'address', 'postal_code_area', 'postal_code_street')

class ItinerarySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ('items', 'date',)
