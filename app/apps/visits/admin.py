from apps.visits.models import Visit
from django.contrib import admin


@admin.register(Visit)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ("author", "start_time")
