# Generated by Django 2.2.10 on 2020-03-04 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itinerary', '0026_auto_20200304_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerary',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
