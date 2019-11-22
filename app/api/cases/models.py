from django.db import models

class Case(models.Model):
    '''
    A simple case model
    '''
    case_id = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        if self.case_id:
            return self.case_id
        return ''
