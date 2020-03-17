from django.contrib import admin
from api.fraudprediction.models import FraudPrediction

@admin.register(FraudPrediction)
class FraudPredictionAdmin(admin.ModelAdmin):
    list_display = ('case_id',)
