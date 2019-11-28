from django.db import models
from api.users.models import User
from api.cases.models import Case

class Itinerary(models.Model):
    """ Itinerary for visiting cases """
    plain_text_itinerary = models.TextField(max_length=4000, blank=True)
    user = models.ForeignKey(to=User, null=True, blank=False, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        if self.user:
            return '{}'.format(self.user.email)
        else:
            return ''


class ItineraryItem(models.Model):
    """ Single Itinerary """
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, null=False, related_name='items')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=False, related_name='cases')

    def __str__(self):
        if self.case:
            return self.case.__str__()
        else:
            return ''


class Note(models.Model):
    """ A note for an Itinerary Item """
    itinerary_item = models.ForeignKey(ItineraryItem, on_delete=models.CASCADE,
                                       null=False, related_name='notes')
    text = models.TextField(null=False, blank=False)
    author = models.ForeignKey(to=User, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        max_length = 20
        if len(self.text) > max_length:
            return '{}...'.format(self.text[:max_length])
        return self.text
