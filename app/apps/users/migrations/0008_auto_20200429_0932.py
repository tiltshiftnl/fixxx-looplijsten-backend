# Generated by Django 3.0.5 on 2020-04-29 09:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_auto_20191119_0859"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["email"]},
        ),
    ]
