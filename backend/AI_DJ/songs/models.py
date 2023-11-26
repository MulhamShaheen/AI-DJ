from django.db import models


# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=200)


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    popularity = models.IntegerField(default=0)
    energy = models.IntegerField(default=0)
    danceability = models.IntegerField(default=0)
    happiness = models.IntegerField(default=0)
    accousticness = models.IntegerField(default=0)
    instrumentalness = models.IntegerField(default=0)
    liveness = models.IntegerField(default=0)
    speechiness = models.IntegerField(default=0)
    loudness = models.IntegerField(default=0)
