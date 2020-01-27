from django.db import models
from utils.queries import get_case

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
