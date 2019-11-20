from enum import Enum
from django.db import models

class Stadia(Enum):
    IMD = 'Issuemelding'
    ECE = 'Eerste controle'
    TCE = 'Tweede controle'
    DCE = 'Derde controle'
    EHE = 'Eerste hercontrole'
    THE = 'Tweede hercontrole'
    DHE = 'Derde hercontrole'

class Case(models.Model):
    '''
    A simple case model, temporarily used for now
    '''
    address = models.CharField(max_length=255, null=False)
    postal_code = models.CharField(max_length=8, null=False)
    stadium_code = models.CharField(
        max_length=255,
        choices=[(tag.name, tag.value) for tag in Stadia],
        blank=False)

    @property
    def stadium(self):
        return Stadia[self.stadium_code].value

    def save(self, *args, **kwargs):
        self.postal_code = ''.join(self.postal_code.split(' '))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.address
