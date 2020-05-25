from django.contrib import admin

from api.fraudprediction.models import FraudPrediction


@admin.register(FraudPrediction)
class FraudPredictionAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'fraud_probability', 'sync_date')

    search_fields = ('case_id',)

    fields = ('case_id', 'fraud_probability',
              'fraud_prediction', 'business_rules', 'shap_values', 'sync_date',)

    readonly_fields = fields
