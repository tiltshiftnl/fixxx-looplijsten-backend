from django.db import models
from utils.queries import get_case
from api.cases.const import PROJECTS, STAGES

class Case(models.Model):
    '''
    A simple case model
    '''
    case_id = models.CharField(max_length=255, null=True, blank=False)

    def __get_case__(self, case_id):
        return get_case(case_id)

    @property
    def bwv_data(self):
        return self.__get_case__(self.case_id)

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

    def __str__(self):
        return self.name

class State(models.Model):
    CHOICES = [(state, state) for state in STAGES]

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        choices=CHOICES)

    def __str__(self):
        return self.name
