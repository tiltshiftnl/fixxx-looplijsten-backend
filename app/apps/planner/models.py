from django.db import models
from .const import EXAMPLE_PLANNER_SETTINGS


class TeamSettings(models.Model):
    name = models.CharField(
        max_length=100,
    )
    settings = models.JSONField(
        default=EXAMPLE_PLANNER_SETTINGS,
    )