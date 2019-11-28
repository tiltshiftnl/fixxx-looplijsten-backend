from django.contrib import admin
from api.itinerary.models import Itinerary, ItineraryItem, Note

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

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = ('itinerary_item', 'text')
