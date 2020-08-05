from django.contrib import admin
from apps.visits.models import Visit


@admin.register(Visit)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('author', 'start_time')