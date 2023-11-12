from abc import ABC, abstractmethod

import PIL
import torch
import torchvision.models
from PIL import Image
from torchvision.transforms import functional as F
from typing import List
from dataclasses import dataclass
import logging
from .classes import Activity
from torchvision import datasets, models, transforms
from torch import nn
import numpy as np


@dataclass
class ClassifierPrediction:
    predicted_class: Activity
    contour_probability: float


class Classifier(ABC):

    @abstractmethod
    def __init__(self):
        pass



class DummyClassifier(Classifier):
    def __init__(self, detection_model_path: str):
        logging.info('Loading Classifier')
        self.model_path = detection_model_path

    def predict_class(self, image: PIL.Image) -> ClassifierPrediction:
        dummy_class = Activity(activity_id=0)
        prediction = ClassifierPrediction(predicted_class=dummy_class, contour_probability=0.98)
        return prediction


class ResnetDetector(DummyClassifier):
    def __init__(self, detection_model_path: str):
        super().__init__(detection_model_path)
        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self._load_model()

    def _load_model(self, ):
        self.model = models.resnet18(weights=None)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 15)
        self.model = self.model.to(self._device)
        self.model.load_state_dict(torch.load(self.model_path))

    def predict_class(self, img_path: str):
        img = Image.open(img_path)
        img = F.pil_to_tensor(img)
        transformer = transforms.Resize(244)
        img = transformer(img).to(self._device, dtype=torch.float32)
        pred = self.model(torch.unsqueeze(img, dim=0))
        result = torch.max(pred, 1)
        return result
