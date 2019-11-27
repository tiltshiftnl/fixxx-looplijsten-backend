from django.contrib import admin
from api.itinerary.models import Itinerary, ItineraryItem

class ItineraryItemInline(admin.StackedInline):
    fields = ('case',)
    model = ItineraryItem
    extra = 0

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('user',)

    inlines = [
        ItineraryItemInline,
    ]
