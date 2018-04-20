# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-26 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine_learning', '0003_history_movie_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='confidence',
        ),
        migrations.AddField(
            model_name='history',
            name='actual_rating',
            field=models.CharField(max_length=25, null=True),
        ),
    ]