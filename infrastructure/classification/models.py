from abc import ABC, abstractmethod

import torch
import torchvision.models
from PIL import Image
from torchvision.transforms import functional as F
from typing import List
from dataclasses import dataclass
import logging
from classes import Activity
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

    @abstractmethod
    def detect_contours(self, image: np.ndarray) -> ClassifierPrediction:
        """
        Return boxes of all detected contours from image.
        :param image: np.ndarray RGB image
        :return: Activity
        """
        pass


class DummyClassifier(Classifier):
    def __init__(self, detection_model_path: str):
        logging.info('Loading Classifier')
        self.model_path = detection_model_path

    def predict_class(self, image: np.ndarray) -> ClassifierPrediction:
        dummy_class = Activity(activity_id=0)
        prediction = ClassifierPrediction(predicted_class=dummy_class, contour_probability=0.98)
        return prediction


class ResnetDetector(DummyClassifier):
    def __init__(self, detection_model_path: str):
        super().__init__(detection_model_path)
        self._load_model()
        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def _load_model(self, trained_model_path="trained/model.pt"):
        self.model = models.resnet18(weights=None)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 15)
        self.model = self.model.to(self._device)
        self.model.load_state_dict(torch.load(trained_model_path))

    def predict_class(self, img_path: str):
        img = Image.open(img_path)
        img = F.pil_to_tensor(img)
        transformer = transforms.Resize([3, 224, 224])
        img = transformer(img).to(self._device)
        pred = self.model(img)
        result = torch.max(pred, 1)
        return result
