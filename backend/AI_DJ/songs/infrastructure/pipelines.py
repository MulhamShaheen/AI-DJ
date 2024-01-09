import torch
from transformers import BertModel, BertTokenizerFast
import torch.nn.functional as F
import pandas as pd
from datasets import Dataset
from typing import List, Union, Literal
from pathlib import Path

from .detection.models import YoloV5Detector
from .classification.models import DenseNetClassifier
from .classification.classes import ACTIVITY_DICT, DRESS_DICT

FEATURE_LIST = [
    "text_emb",
    "activity",
    "dress_code",
    "place",
]


class RecoDummyPipeline:
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


class TextFaissPipeline:
    def __init__(self, model_checkpoint: str = 'setu4993/LEALLA-small'):
        # load model
        if 'LEALLA' in model_checkpoint:
            self.tokenizer = BertTokenizerFast.from_pretrained(model_checkpoint)
            self.model = BertModel.from_pretrained(model_checkpoint)
            self.model = self.model.eval()

        df_lyrics = pd.read_csv(
            'https://raw.githubusercontent.com/MulhamShaheen/AI-DJ/dev/search/scraper/songs_database_mini.csv')
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

    def predict_list(self, prompt: str, top_k=10):
        scores, samples = self.lyrics_dataset.get_nearest_examples('lyrics_embeddings',
                                                                   self._get_embeddings(
                                                                       [prompt]).cpu().detach().numpy(), k=top_k)
        return scores, samples


class HumanDetectionPipeline:
    def __init__(self):
        self.detector = YoloV5Detector()

    def detect_humans(self, img_path: str, media_path: str = "media/detections/"):
        path = media_path + Path(img_path).name
        self.detector.save_predictions(img_path, path)

        return path


class ActivityClassificationPipeline:
    def __init__(self, model_path: str, target: Literal["dress_code", "activity"]):
        self.classifier = DenseNetClassifier(detection_model_path=model_path, target=target)
        if target is "activity":
            self.classes = ACTIVITY_DICT.values()
        else:
            self.classes = DRESS_DICT.values()

    def predict(self, img_path: Union[str, List[str]]):
        pred_dict = {c: 0 for c in ACTIVITY_DICT.values()}
        if type(img_path) is str:
            pred = self.classifier.predict_class(img_path)
            pred_dict[pred.predicted_class.get_name()] += 1

        elif type(img_path) is List:
            for img in img_path:
                pred = self.classifier.predict_class(img)
                pred_dict[pred.predicted_class.get_name()] += 1

        return pred_dict
