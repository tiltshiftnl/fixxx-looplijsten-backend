from django.contrib.postgres.fields import JSONField
from django.db import models


class FraudPrediction(models.Model):
    """
    A case fraud prediction
    """

    case_id = models.CharField(max_length=255, null=True, blank=False, unique=True)
    fraud_probability = models.FloatField(null=False)
    fraud_prediction = models.BooleanField(null=False)
    business_rules = JSONField(null=False)
    shap_values = JSONField(null=False)
    sync_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.case_id
