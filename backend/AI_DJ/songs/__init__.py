import pandas as pd

from .infrastructure.pipelines import HumanDetectionPipeline, ClassificationPipeline, TextFaissPipeline, \
    EnsemblePipeline
from .infrastructure.ranking.feature_ranker import FeatureRanker

text_pipeline = TextFaissPipeline()
detection_pipeline = HumanDetectionPipeline()
dress_pipeline = ClassificationPipeline(
    model_path="songs/infrastructure/classification/saved_models/dress_code_model.ckpt", target="dress_code")

act_pipeline = ClassificationPipeline(
    model_path="songs/infrastructure/classification/saved_models/model_100.pt", target="activity")

ensamble_pipeline = EnsemblePipeline(detection_pipeline, act_pipeline, dress_pipeline)

ranker = FeatureRanker(text_pipeline)
