from yandex import get_lyrics
import pandas as pd
from tqdm import tqdm
import math


def add_lyrics(songs_df: pd.DataFrame, id_col='id'):
    lyrics = []
    for id in tqdm(songs_df[id_col]):
        if not id or math.isnan(id):
            lyrics.append(None)
        else:
            lyrics.append(get_lyrics(int(id)))
    songs_df['lyrics'] = lyrics

    return songs_df


if __name__ == '__main__':
    songs_df = pd.read_csv('data/songs_latest_database.csv', index_col=0)
    lyrics_df = add_lyrics(songs_df, id_col='yt_id')
    lyrics_df.to_csv('data/latest_database_with_lyrics.csv', index=False)
