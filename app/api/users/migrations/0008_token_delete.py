from django.db import migrations
from rest_framework.authtoken.models import Token

def delete_tokens(apps, schema_editor):
    Token.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20191119_0859'),
    ]

    operations = [
        migrations.RunPython(delete_tokens),
    ]
