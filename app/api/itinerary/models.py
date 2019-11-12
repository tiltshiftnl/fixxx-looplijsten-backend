from django.db import models
from utils import helpers
from api.users.models import Team

class Itinerary(models.Model):
    """ Itinerary for visiting cases """
    team = models.ForeignKey(to=Team, blank=True, null=True, on_delete=models.CASCADE)
    plain_text_itinerary = models.TextField(max_length=4000, blank=True)
    date = models.DateField(blank=True)

    def __str__(self):
        return '{} {}'.format(self.date, self.team)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.items.all().delete()

        if self.plain_text_itinerary.strip():
            for line in self.plain_text_itinerary.split('\n'):
                itinerary_item_data = helpers.get_postal_code(line)
                itinerary_item = ItineraryItem(itinerary=self, **itinerary_item_data)
                itinerary_item.save()


class ItineraryItem(models.Model):
    """ Single Itinerary """
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, null=False, related_name='items')
    address = models.CharField(max_length=255, null=False)
    postal_code_area = models.CharField(max_length=255, null=False)
    postal_code_street = models.CharField(max_length=255, null=False)
    stadium = models.CharField(max_length=255, blank=True)
    wng_id = models.CharField(max_length=255, blank=True)
    adres_id = models.CharField(max_length=255, blank=True)

    @property
    def postal_code(self):
        return '{}{}'.format(self.postal_code_area, self.postal_code_street)

    # def save(self, *args, **kwargs):
        # ids = mock_readers.get_adress_ids(self.address, self.postal_code)
        # self.wng_id = ids['wng_id']
        # self.adres_id = ids['adres_id']
        # super().save(*args, **kwargs)

    def __str__(self):
        return self.address
