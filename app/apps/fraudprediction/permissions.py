from django.conf import settings
from rest_framework.permissions import BasePermission


class FraudPredictionApiKeyAuth(BasePermission):
    def has_permission(self, request, view):
        api_key_secret = request.META.get("HTTP_AUTHORIZATION", None)

        if api_key_secret:
            return api_key_secret == settings.FRAUD_PREDICTION_SECRET_KEY

        return False
