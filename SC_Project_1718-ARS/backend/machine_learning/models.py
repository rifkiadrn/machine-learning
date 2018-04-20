# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class History(models.Model):
    movie_id = models.CharField(max_length=50, null=True, default="")
    movie_thumbnail = models.URLField(null=True)
    movie_name = models.CharField(max_length=250, null=True,default="")
    movie_rating = models.FloatField(null=True)
    actual_rating = models.CharField(null=True, max_length=25)

class Movie(models.Model):
    movie_id = models.CharField(max_length=50, primary_key=True)
    movie_thumbnail = models.URLField(null=True)
    movie_name = models.CharField(max_length=250, null=True,default="")
    plot = models.TextField()
    genre = models.TextField()
    director_name = models.CharField(max_length=50, null=True)
    director_fbl = models.IntegerField(blank=True, null=True)
    actor_1_name = models.CharField(max_length=50, null=True)
    actor_1_fbl = models.IntegerField(blank=True, null=True)
    actor_2_name = models.CharField(max_length=50, null=True)
    actor_2_fbl = models.IntegerField(blank=True, null=True)
    actor_3_name = models.CharField(max_length=50, null=True)
    actor_3_fbl = models.IntegerField(blank=True, null=True)
    year = models.CharField(max_length=4, null=True )
    duration = models.CharField(max_length=5, null=True)