from apps.planner.models import PostalCodeRange, PostalCodeRangeSet, TeamSettings
from django.contrib import admin


@admin.register(TeamSettings)
class TeamSettingsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    # readonly_fields = ("settings",)


class PostalCodeRangeInline(admin.TabularInline):
    model = PostalCodeRange
    extra = 1


@admin.register(PostalCodeRangeSet)
class PostalCodeRangeSetAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [PostalCodeRangeInline]
