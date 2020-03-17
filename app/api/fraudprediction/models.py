from django.db import models
from django.contrib.postgres.fields import JSONField

class FraudPrediction(models.Model):
    '''
    A case fraud prediction
    '''
    case_id = models.CharField(max_length=255, null=True, blank=False, unique=True)
    fraud_probability = models.FloatField(null=False)
    fraud_prediction = models.BooleanField(null=False)
    business_rules = JSONField(null=False)
    shap_values = JSONField(null=False)

    def __str__(self):
        return self.case_id
