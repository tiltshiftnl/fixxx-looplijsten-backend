import logging
from api.fraudprediction.models import FraudPrediction
from api.fraudprediction.serializers import FraudPredictionSerializer


LOGGER = logging.getLogger(__name__)

def get_fraud_prediction(case_id):
    try:
        fraud_prediction = FraudPrediction.objects.get(case_id=case_id)
        serializer = FraudPredictionSerializer(fraud_prediction)
        return serializer.data
    except FraudPrediction.DoesNotExist:
        LOGGER.warning('Fraud prediction object for case does not exist: {}'.format(case_id))
