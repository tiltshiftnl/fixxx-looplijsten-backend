# Generated by Django 2.1.9 on 2019-11-04 14:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("itinerary", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="itineraryitem",
            name="postal_code_area",
            field=models.CharField(default="AH", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="itineraryitem",
            name="postal_code_street",
            field=models.CharField(default=1234, max_length=255),
            preserve_default=False,
        ),
    ]
