from django.contrib import admin
from api.itinerary.models import Itinerary, ItineraryItem

class ItineraryItemInline(admin.StackedInline):
    model = ItineraryItem
    readonly_fields = ('pk', 'wng_id', 'adres_id', 'address', 'postal_code_area', 'postal_code_street')
    can_delete = False
    extra = 0

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('user',)

    inlines = [
        ItineraryItemInline,
    ]
