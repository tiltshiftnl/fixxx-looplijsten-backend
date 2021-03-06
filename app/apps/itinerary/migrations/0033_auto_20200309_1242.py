# Generated by Django 2.2.10 on 2020-03-09 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("itinerary", "0032_auto_20200309_1240"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itinerarysettings",
            name="itinerary",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="settings",
                to="itinerary.Itinerary",
            ),
        ),
    ]
