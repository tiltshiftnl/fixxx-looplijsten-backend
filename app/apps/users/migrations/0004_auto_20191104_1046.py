# Generated by Django 2.1.9 on 2019-11-04 10:46

from apps.users import user_manager
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_auto_20191104_1040"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", user_manager.UserManager()),
            ],
        ),
    ]
