from rest_framework import serializers
from .models import Song


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('pk', 'title', 'artists', 'popularity')