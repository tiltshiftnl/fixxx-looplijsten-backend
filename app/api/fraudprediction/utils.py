from api.fraudprediction.models import FraudPrediction
from api.fraudprediction.serializers import FraudPredictionSerializer

def get_fraud_prediction(case_id):
    try:
        fraud_prediction = FraudPrediction.objects.get(case_id=case_id)
        serializer = FraudPredictionSerializer(fraud_prediction)
        return serializer.data
    except FraudPrediction.DoesNotExist:
        pass
