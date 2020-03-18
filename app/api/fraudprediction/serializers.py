from rest_framework import serializers
from api.fraudprediction.models import FraudPrediction

class FraudPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudPrediction
        fields = ('fraud_probability', 'fraud_prediction', 'business_rules', 'shap_values')
