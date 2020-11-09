from apps.planner.models import (
    DaySettings,
    PostalCodeRange,
    PostalCodeRangeSet,
    TeamSettings,
)
from django.contrib import admin


class DaySettingsInline(admin.TabularInline):
    model = DaySettings
    # readonly_fields = ("settings",)
    extra = 0


@admin.register(TeamSettings)
class TeamSettingsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    # readonly_fields = ("settings",)
    inlines = [DaySettingsInline]


class PostalCodeRangeInline(admin.TabularInline):
    model = PostalCodeRange
    extra = 1


@admin.register(PostalCodeRangeSet)
class PostalCodeRangeSetAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [PostalCodeRangeInline]
