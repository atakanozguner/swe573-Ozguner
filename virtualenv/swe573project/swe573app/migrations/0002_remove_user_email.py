# Generated by Django 4.2.11 on 2024-04-29 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swe573app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]
