# Generated by Django 5.2.4 on 2025-07-06 10:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together={('author', 'content')},
        ),
    ]
