from django.db import models
from api.itinerary.models import ItineraryItem
from api.users.models import User

class Visit(models.Model):
    """ Captures data of a visit """
    itinerary_item = models.ForeignKey(ItineraryItem, on_delete=models.CASCADE, null=False, related_name='visits')
    author = models.ForeignKey(to=User, null=False, blank=False, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False)
    description = models.CharField(null=True, max_length=255)
    nobody_present = models.BooleanField(null=True)
    suggest_next_visit_day = models.BooleanField(null=True)
    suggest_next_visit_evening = models.BooleanField(null=True)
    suggest_next_visit_weekend = models.BooleanField(null=True)
    suggest_next_visit_unknown = models.BooleanField(null=True)
    suggest_discontinue_case = models.BooleanField(null=True)
    no_cooperation = models.BooleanField(null=True)
    no_cooperation_malfunctioning_doorbell = models.BooleanField(null=True)
    no_cooperation_video_call = models.BooleanField(null=True)
    no_cooperation_hotel_furnished = models.BooleanField(null=True)
    no_cooperation_vacant = models.BooleanField(null=True)
    no_cooperation_likely_inhabited = models.BooleanField(null=True)
    cooperation = models.BooleanField(null=True)
    cooperation_likely_fraud = models.BooleanField(null=True)







