from django.conf import settings

from rest_framework.permissions import BasePermission


class FraudPredicionApiKeyAuth(BasePermission):
    def has_permission(self, request, view):
        api_key_secret = request.META.get('HTTP_AUTHORIZATION')
        return api_key_secret == settings.FRAUD_PREDICTION_SECRET_KEY
