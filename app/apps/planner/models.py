from django.db import models
from settings.const import EXAMPLE_PLANNER_SETTINGS
from .const import TEAM_TYPE_CHOICES, TEAM_TYPE_VAKANTIEVERHUUR
from apps.cases.models import Project, Stadium

class TeamSettings(models.Model):
    name = models.CharField(
        max_length=100,
    )
    team_type = models.CharField(
        max_length=100,
        choices=TEAM_TYPE_CHOICES,
        default=TEAM_TYPE_VAKANTIEVERHUUR
    )
    project_choices = models.ManyToManyField(
        to=Project,
        blank=True, 
        related_name="team_settings_list",
    )
    stadia_choices = models.ManyToManyField(
        to=Stadium,
        blank=True, 
        related_name="team_settings_list",
    )
    settings = models.JSONField(
        default=EXAMPLE_PLANNER_SETTINGS,
    )
    settings = models.JSONField(
        default=EXAMPLE_PLANNER_SETTINGS,
    )

    def __str__(self):
        return self.name
