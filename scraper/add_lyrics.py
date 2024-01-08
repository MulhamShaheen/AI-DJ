from yandex import get_lyrics
import pandas as pd
from tqdm import tqdm


def add_lyrics(songs_df: pd.DataFrame):
    lyrics = []
    for id in tqdm(songs_df['id']):
        lyrics.append(get_lyrics(int(id)))
    songs_df['lyrics'] = lyrics

    return songs_df


if __name__ == '__main__':
    songs_df = pd.read_csv('data/yandex.csv')
    lyrics_df = add_lyrics(songs_df)
    lyrics_df.to_csv('data/songs_with_lyrics.csv', index=False)
