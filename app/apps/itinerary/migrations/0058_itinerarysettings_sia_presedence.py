# Generated by Django 3.1.2 on 2020-11-25 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("itinerary", "0057_remove_itinerarysettings_team_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="itinerarysettings",
            name="sia_presedence",
            field=models.BooleanField(default=False),
        ),
    ]
