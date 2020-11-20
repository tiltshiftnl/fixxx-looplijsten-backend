from apps.cases.models import Project, Stadium, StadiumLabel
from apps.visits.models import Observation, Situation, SuggestNextVisit
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from settings.const import (
    EXAMPLE_DAY_SETTINGS,
    EXAMPLE_PLANNER_SETTINGS,
    POSTAL_CODE_RANGES,
    WEEK_DAYS_CHOICES,
)


def team_settings_settings_default():
    return EXAMPLE_PLANNER_SETTINGS


def day_settings_default():
    return EXAMPLE_DAY_SETTINGS


def day_settings__postal_code_ranges__default():
    return POSTAL_CODE_RANGES


class TeamSettings(models.Model):
    name = models.CharField(
        max_length=100,
    )
    show_issuemelding = models.BooleanField(
        default=True,
    )
    show_vakantieverhuur = models.BooleanField(
        default=True,
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

    class Meta:
        verbose_name_plural = "Team settings"

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


class DaySettings(models.Model):
    team_settings = models.ForeignKey(
        to=TeamSettings, related_name="day_settings_list", on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=50,
    )
    week_day = models.PositiveSmallIntegerField(
        choices=WEEK_DAYS_CHOICES,
        blank=True,
        null=True,
    )
    start_time = models.TimeField(
        blank=True,
        null=True,
    )
    opening_date = models.DateField(
        default="2019-01-01",
    )
    postal_code_ranges = models.JSONField(
        default=day_settings__postal_code_ranges__default,
    )
    postal_code_ranges_presets = models.ManyToManyField(
        to=PostalCodeRangeSet,
        blank=True,
        related_name="postal_code_ranges_presets_day_settings_list",
    )
    length_of_list = models.PositiveSmallIntegerField(
        default=8,
    )
    projects = models.ManyToManyField(
        to=Project,
        blank=True,
        related_name="projects_day_settings_list",
    )
    primary_stadium = models.ForeignKey(
        to=Stadium,
        null=True,
        blank=True,
        related_name="primary_stadium_day_settings_list",
        on_delete=models.SET_NULL,
    )
    secondary_stadia = models.ManyToManyField(
        to=Stadium,
        blank=True,
        related_name="secondary_stadia_day_settings_list",
    )
    exclude_stadia = models.ManyToManyField(
        to=Stadium,
        blank=True,
        related_name="exclude_stadia_day_settings_list",
    )

    class Meta:
        ordering = ("week_day", "start_time")
        verbose_name_plural = "Day settings"

    def __str__(self):
        return "%s - %s" % (
            self.team_settings.name,
            self.name,
        )
