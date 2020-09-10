# Generated by Django 3.0.7 on 2020-08-18 08:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visits", "0006_auto_20200812_1604"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visit",
            name="observations",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("malfunctioning_doorbell", "Bel functioneert niet"),
                        ("intercom", "Contact via intercom"),
                        ("hotel_furnished", "Hotelmatig ingericht"),
                        ("vacant", "Leegstaand"),
                        ("likely_inhabited", "Vermoedelijk bewoond"),
                    ],
                    max_length=50,
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]