from django.contrib import admin
from django.http import JsonResponse

from api.itinerary.models import Itinerary, ItineraryItem, Note, ItineraryTeamMember, ItinerarySettings, PostalCodeSettings
from api.itinerary.serializers import ItinerarySerializer

class PostalCodeSettingsInline(admin.StackedInline):
    fields = ('range_start', 'range_end')
    model = PostalCodeSettings

class ItinerarySettingsInline(admin.StackedInline):
    fields = ('opening_date', 'target_length', 'projects', 'primary_stadium',
              'secondary_stadia', 'exclude_stadia', 'start_case')
    model = ItinerarySettings


class ItineraryTeamMemberInline(admin.StackedInline):
    fields = ('user',)
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
        ItinerarySettingsInline,
        PostalCodeSettingsInline
    ]

    actions = ['export_as_json']

    def export_as_json(self, request, queryset):
        serializer = ItinerarySerializer(queryset.all(), many=True)
        return JsonResponse({'looplijsten': serializer.data})


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = ('itinerary_item', 'text', 'author')


@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    fields = ('itinerary', 'case', 'position', 'checked')
