from django.contrib import admin
from api.cases.models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('address', 'postal_code', 'stadium_code')
