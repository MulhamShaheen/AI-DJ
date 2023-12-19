import torch
from transformers import BertModel, BertTokenizerFast
import torch.nn.functional as F
import pandas as pd
from datasets import Dataset
from typing import List

FEATURE_LIST = [
    "text_emb",
    "activity",
    "dress_code",
    "place",
]


class RecoDummyPipline:
    def __init__(self, features: list):
        for f in features:
            if f not in FEATURE_LIST:
                print("features should be in one of: ", FEATURE_LIST)
                return
        self.features = features

    def predict_list(self, prompt: str, image: str):
        out_filters = {}
        for f in self.features:
            # DO MAGIC
            out_filters[f] = 0

        return out_filters


class TextDummyPipline:
    def __init__(self):
        # LOAD DATA AND FITTING
        pass

    def sample_mapper(self, sample):
        id = 0
        return id

    def predict_list(self, prompt: str):
        # DO MAGIC
        # predict
        # map

        return [1, 2, 3, 4]


class TextFaissPipeline:
    def __init__(self, prompt: str, model_checkpoint: str = 'setu4993/LEALLA-small'):
        self.prompt = prompt

        # todo: shouldn't the model be loaded only once?
        # load model
        if 'LEALLA' in model_checkpoint:
            self.tokenizer = BertTokenizerFast.from_pretrained(model_checkpoint)
            self.model = BertModel.from_pretrained(model_checkpoint)
            self.model = self.model.eval()

        df_lyrics = pd.read_csv(
            'https://raw.githubusercontent.com/MulhamShaheen/AI-DJ/main/prototype/NLP/data/lyrics.csv')
        song_lyrics = df_lyrics['lyrics'].tolist()
        lyrics_dataset = Dataset.from_pandas(df_lyrics)
        lyrics_dataset = lyrics_dataset.map(lambda x: {'lyrics_embeddings': self._get_embeddings(x['lyrics'])[0]})
        lyrics_dataset.add_faiss_index(column='lyrics_embeddings')
        self.lyrics_dataset = lyrics_dataset

    def _get_embeddings(self, texts: List[str], normalize=True):
        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True)

        with torch.no_grad():
            outputs = self.model(**inputs)

        embeddings = outputs.pooler_output

        if normalize:
            normalized_embeddings = F.normalize(embeddings, p=2)
            return normalized_embeddings
        else:
            return embeddings

    def predict_list(self, top_k=10):
        scores, samples = self.lyrics_dataset.get_nearest_examples('lyrics_embeddings',
                                                                   self._get_embeddings(
                                                                       [self.prompt]).cpu().detach().numpy(),
                                                                   k=top_k)
        return scores, samples
