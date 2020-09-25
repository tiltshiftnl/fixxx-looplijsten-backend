from apps.itinerary.models import ItineraryItem
from apps.users.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from apps.visits import const as visits_const


class Visit(models.Model):
    """ Captures data of a visit """

    situation = models.CharField(
        max_length=50, choices=visits_const.SITUATIONS, null=True, blank=True
    )
    observations = ArrayField(
        models.CharField(max_length=50, choices=visits_const.OBSERVATIONS), blank=True, null=True
    )
    itinerary_item = models.ForeignKey(
        ItineraryItem, on_delete=models.CASCADE, related_name="visits"
    )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False)

    description = models.TextField(
        null=True
    )  # these are the notes when access was granted

    # Describe if next visit can go ahead and why yes or no
    can_next_visit_go_ahead = models.BooleanField(default=True, blank=True, null=True)
    can_next_visit_go_ahead_description = models.TextField(null=True)

    # suggest_visit_next_time = models.BooleanField(default=True) # TODO not sure about this one
    suggest_next_visit = models.CharField(
        null=True, max_length=50, choices=visits_const.SUGGEST_NEXT_VISIT
    )
    suggest_next_visit_description = models.TextField(null=True, blank=True)

    # personal notes to help make report at the office/as reminders for TH.
    personal_notes = models.TextField(blank=True, null=True)
