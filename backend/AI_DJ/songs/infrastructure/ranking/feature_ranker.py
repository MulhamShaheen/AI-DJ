from typing import Dict

import pandas as pd
from ..pipelines import TextFaissPipeline

SONGS_FEATURES = ['title', 'label', 'artists', 'album', 'popularity', 'camelot', 'BPM',
                  'key', 'acousticness', 'happiness', 'instrumentalness', 'liveness',
                  'loudness', 'danceability', 'energy', 'yt_id', 'lyrics']


class FeatureRanker:
    def __init__(self, text_pipeline: TextFaissPipeline, song_model=None, ):
        self.song_model = song_model
        self.text_pipeline = text_pipeline

    def _get_from_db(self) -> pd.DataFrame:
        objects = self.song_model.objects.all()
        data = []
        for object in objects:
            data.append(
                list(object.__dict__.values())
            )
        df = pd.DataFrame(data, columns=list(objects[0].__dict__.keys()))
        df = df[SONGS_FEATURES]

        return df

    def rank(self, prompt: str, activity_preds: Dict[str, int], dress_code_preds: Dict[str, int], k_top: int = 10):
        songs_df = pd.read_csv('latest_database_with_lyrics.csv', encoding="utf-8")
        max_act = max(activity_preds, key=activity_preds.get)
        max_dress = max(dress_code_preds, key=dress_code_preds.get)

        if max_act in ["cycling", "running"]:
            act_sort = {"col": "energy", "asc": False}

        elif max_act in ["dancing", "clapping", "laughing", "hugging", "fighting"]:
            act_sort = {"col": "loudness", "asc": False}

        elif max_act in ["eating", "drinking", "sitting"]:
            act_sort = {"col": "loudness", "asc": True}

        else:
            act_sort = {"col": "popularity", "asc": False}

        if max_dress == "classic":
            dress_sort = {"col": "acousticness", "asc": False}

        elif max_dress == "casual":
            dress_sort = {"col": "happiness", "asc": False}

        else:
            dress_sort = {"col": "BPM", "asc": False}

        songs_df = songs_df.sort_values([act_sort["col"], dress_sort["col"]],
                                        ascending=[act_sort["asc"], dress_sort["asc"]]).iloc[:100]
        songs_df = songs_df.drop_duplicates(subset=['title', 'album'])
        songs_df = songs_df.iloc[:100]
        scores, samples = self.text_pipeline.predict_list(prompt, 100)
        samples_df = pd.DataFrame(samples)
        samples_df.insert(2, "score", scores, True)
        reco_df = songs_df.merge(samples_df, on=list(songs_df.columns), how="left").sort_values("score",
                                                                                                ascending=False).iloc[:k_top]

        return reco_df
