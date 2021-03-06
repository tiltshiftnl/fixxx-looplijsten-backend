# Generated by Django 3.1.2 on 2020-10-06 13:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visits", "0008_visitmetadata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visitmetadata",
            name="visit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meta_data",
                to="visits.visit",
                unique=True,
            ),
        ),
    ]
