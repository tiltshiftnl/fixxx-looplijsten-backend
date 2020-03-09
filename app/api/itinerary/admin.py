from django.contrib import admin
from api.itinerary.models import Itinerary, ItineraryItem, Note, ItineraryTeamMember


class ItineraryTeamMemberInline(admin.StackedInline):
    fields = ('user', )
    model = ItineraryTeamMember
    extra = 0

class ItineraryItemInline(admin.StackedInline):
    fields = ('case',)
    model = ItineraryItem
    extra = 0

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at',)

    inlines = [
        ItineraryTeamMemberInline,
        ItineraryItemInline,
    ]

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = ('itinerary_item', 'text', 'author')
