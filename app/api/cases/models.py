from django.db import models
from utils.queries import get_case
from api.cases.const import PROJECTS, STADIA
# from api.fraudprediction.models import FraudPrediction

class Case(models.Model):
    class Meta:
        ordering = ['case_id']

    '''
    A simple case model
    '''
    case_id = models.CharField(max_length=255, null=True, blank=False)

    def get(case_id):
        return Case.objects.get_or_create(case_id=case_id)[0]

    def __get_case__(self, case_id):
        return get_case(case_id)

    def get_location(self):
        case_data = self.__get_case__(self.case_id)
        return {'lat': case_data.get('lat'), 'lng': case_data.get('lng')}

    @property
    def bwv_data(self):
        return self.__get_case__(self.case_id)

    @property
    def fraud_prediction(self):
        return {}
        # fraud_prediction = FraudPrediction.objects.get(case_id=self.case_id)
        # return fraud_prediction

    def __str__(self):
        if self.case_id:
            return self.case_id
        return ''

class Project(models.Model):
    CHOICES = [(project, project) for project in PROJECTS]

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        choices=CHOICES)

    def get(name):
        return Project.objects.get_or_create(name=name)[0]

    def __str__(self):
        return self.name

class Stadium(models.Model):
    CHOICES = [(stadium, stadium) for stadium in STADIA]

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        choices=CHOICES)

    def get(name):
        return Stadium.objects.get_or_create(name=name)[0]

    def __str__(self):
        return self.name
