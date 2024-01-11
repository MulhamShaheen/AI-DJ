from django.db import models


# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=200)


class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True)
    artists = models.CharField(max_length=200, blank=True)
    popularity = models.IntegerField(default=0)
    camelot = models.CharField(max_length=10, blank=True)
    BPM = models.IntegerField(default=0)
    key = models.CharField(max_length=10, blank=True)
    acousticness = models.IntegerField(default=0)
    happiness = models.IntegerField(default=0)
    instrumentalness = models.IntegerField(default=0)
    liveness = models.IntegerField(default=0)
    loudness = models.IntegerField(default=0)
    danceability = models.IntegerField(default=0)
    energy = models.IntegerField(default=0)
    label = models.CharField(max_length=200, default="background")

    def __str__(self):
        return f"{self.title} {self.artists}"
