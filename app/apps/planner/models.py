from apps.cases.models import Project, Stadium, StadiumLabel
from apps.visits.models import Observation, Situation, SuggestNextVisit
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from settings.const import EXAMPLE_PLANNER_SETTINGS

from .const import TEAM_TYPE_CHOICES, TEAM_TYPE_VAKANTIEVERHUUR


def team_settings_settings_default():
    return EXAMPLE_PLANNER_SETTINGS


class TeamSettings(models.Model):
    name = models.CharField(
        max_length=100,
    )
    team_type = models.CharField(
        max_length=100, choices=TEAM_TYPE_CHOICES, default=TEAM_TYPE_VAKANTIEVERHUUR
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
    fraud_predict = models.BooleanField(
        default=True,
    )
    marked_stadia = models.ManyToManyField(
        to=StadiumLabel,
        blank=True,
        related_name="stadium_label_team_settings_list",
    )
    observation_choices = models.ManyToManyField(
        to=Observation,
        blank=True,
        related_name="team_settings_list",
    )
    suggest_next_visit_choices = models.ManyToManyField(
        to=SuggestNextVisit,
        blank=True,
        related_name="team_settings_list",
    )
    settings = models.JSONField(
        default=team_settings_settings_default,
    )

    @property
    def situation_choices(self):
        return list(Situation.objects.all().values_list("value", flat=True))

    def __str__(self):
        return self.name


class PostalCodeRangeSet(models.Model):
    name = models.CharField(
        max_length=50,
    )


class PostalCodeRange(models.Model):
    range_start = models.PositiveSmallIntegerField(
        default=1000, validators=[MaxValueValidator(9999), MinValueValidator(1000)]
    )
    range_end = models.PositiveSmallIntegerField(
        default=1000, validators=[MaxValueValidator(9999), MinValueValidator(1000)]
    )
    postal_code_range_set = models.ForeignKey(
        to=PostalCodeRangeSet,
        on_delete=models.CASCADE,
        related_name="postal_code_ranges",
    )

    def save(self, *args, **kwargs):
        if not self.range_end or self.range_end < self.range_start:
            self.range_end = self.range_start
        super().save(*args, **kwargs)
