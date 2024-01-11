from django.conf import settings
from .models import Song
import pandas as pd
import os


def handle_uploaded_file(file):
    folder = f'{settings.MEDIA_ROOT}/uploads/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(f'{folder}/{file.name}.jpg', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return f'{folder}/{file.name}.jpg'


def csv_to_bd(csv_file: str):
    df = pd.read_csv(csv_file,
                     names=['title', 'artists', 'album', 'popularity', 'camelot', 'BPM',
                            'key', 'acousticness', 'happiness', 'instrumentalness', 'liveness', 'loudness',
                            'danceability', 'energy', 'label'])
    # df = df.reset_index()
    for index, row in df.iterrows():
        row["artists"] = str(row["artists"])
        song = Song(**row)
        song.save()
        print(song)



