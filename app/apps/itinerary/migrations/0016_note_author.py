# Generated by Django 2.1.11 on 2019-11-28 00:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("itinerary", "0015_note"),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                unique=True,
            ),
        ),
    ]
