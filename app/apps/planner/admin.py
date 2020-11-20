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
    fieldsets = ((None, {"fields": ("name", "week_day", "start_time")}),)


@admin.register(TeamSettings)
class TeamSettingsAdmin(admin.ModelAdmin):
    list_display = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "fraud_predict", "show_issuemelding")}),
        (
            "Projects & stadia options",
            {
                "classes": ("collapse",),
                "fields": ("project_choices", "stadia_choices"),
            },
        ),
        (
            "Visit options",
            {
                "classes": ("collapse",),
                "fields": ("observation_choices", "suggest_next_visit_choices"),
            },
        ),
        (
            "Visual options",
            {
                "classes": ("collapse",),
                "fields": ("marked_stadia", "show_vakantieverhuur"),
            },
        ),
    )
    # readonly_fields = ("settings",)
    inlines = [DaySettingsInline]


class PostalCodeRangeInline(admin.TabularInline):
    model = PostalCodeRange
    extra = 1


@admin.register(PostalCodeRangeSet)
class PostalCodeRangeSetAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [PostalCodeRangeInline]
