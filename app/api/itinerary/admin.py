from django.contrib import admin
from api.itinerary.models import Itinerary, ItineraryItem, Note, ItineraryTeamMember, ItinerarySettings

class ItinerarySettingsInline(admin.StackedInline):
    fields = ('opening_date', 'target_length', 'projects',
              'primary_stadium', 'secondary_stadia', 'exclude_stadia', 'start_case')
    model = ItinerarySettings

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
        ItinerarySettingsInline
    ]

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = ('itinerary_item', 'text', 'author')


@admin.register(ItineraryItem)
class ItineraryItemAdmim(admin.ModelAdmin):
    fields = ('itinerary', 'case', 'position', 'checked')
