# Generated by Django 4.2.11 on 2024-05-20 03:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('swe573app', '0005_community_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='community',
            name='moderators',
            field=models.ManyToManyField(blank=True, related_name='moderating', to=settings.AUTH_USER_MODEL),
        ),
    ]
