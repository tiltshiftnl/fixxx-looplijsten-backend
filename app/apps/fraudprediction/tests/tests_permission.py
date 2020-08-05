from types import SimpleNamespace

from django.test import TestCase

from apps.fraudprediction.permissions import FraudPredictionApiKeyAuth


class FraudPredictionPermissions(TestCase):

    def test_with_no_key(self):
        """
        Should not have permission if the request has no key
        """
        KEY = 'FRAUD_PREDICTION_KEY'

        with self.settings(FRAUD_PREDICTION_SECRET_KEY=KEY):
            fraud_prediction_auth = FraudPredictionApiKeyAuth()
            request = SimpleNamespace(META={})
            has_permission = fraud_prediction_auth.has_permission(request, None)
            self.assertFalse(has_permission)

    def test_with_incorrect_permission(self):
        """
        Should not have permission if the request has the incorrect key
        """
        KEY = 'FRAUD_PREDICTION_KEY'

        with self.settings(FRAUD_PREDICTION_SECRET_KEY=KEY):
            fraud_prediction_auth = FraudPredictionApiKeyAuth()
            request = SimpleNamespace(META={'HTTP_AUTHORIZATION': 'OTHER KEY'})
            has_permission = fraud_prediction_auth.has_permission(request, None)
            self.assertFalse(has_permission)

    def test_with_correct_permission(self):
        """
        Should have permission if the request has the correct key
        """
        KEY = 'FRAUD_PREDICTION_KEY'

        with self.settings(FRAUD_PREDICTION_SECRET_KEY=KEY):
            fraud_prediction_auth = FraudPredictionApiKeyAuth()
            request = SimpleNamespace(META={'HTTP_AUTHORIZATION': KEY})
            has_permission = fraud_prediction_auth.has_permission(request, None)
            self.assertTrue(has_permission)
