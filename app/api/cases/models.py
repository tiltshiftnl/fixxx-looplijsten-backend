from django.db import models
from utils.queries import get_case

class Case(models.Model):
    '''
    A simple case model
    '''
    case_id = models.CharField(max_length=255, null=True, blank=False)

    @property
    def bwv_data(self):
        return get_case(self.case_id)

    def __str__(self):
        if self.case_id:
            return self.case_id
        return ''
