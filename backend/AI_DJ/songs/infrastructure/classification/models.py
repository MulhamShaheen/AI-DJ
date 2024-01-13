from abc import ABC, abstractmethod
import logging
from typing import List, Union, Literal
from dataclasses import dataclass

import PIL
import numpy as np
import torch
from torch import nn
from torchvision.models import densenet121
from torchvision import datasets, models, transforms
from torchvision.transforms import functional as F
from PIL import Image
from .classes import Activity, DressCode


@dataclass
class ClassifierPrediction:
    predicted_class: Union[Activity, DressCode]
    probability: float


class Classifier(ABC):

    @abstractmethod
    def __init__(self):
        pass


class DummyClassifier(Classifier):
    def __init__(self, detection_model_path: str):
        logging.info('Loading Classifier')
        self.model_path = detection_model_path

    def predict_class(self, img_path: str) -> ClassifierPrediction:
        dummy_class = Activity(activity_id=0)
        prediction = ClassifierPrediction(predicted_class=dummy_class, probability=0.98)
        return prediction


class ResnetClassifier(DummyClassifier):
    def __init__(self, detection_model_path: str):
        super().__init__(detection_model_path)
        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self._load_model()

    def _load_model(self):
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


class DenseNetClassifier(DummyClassifier):
    def __init__(self, detection_model_path: str, target: Literal["dress_code", "activity"]):
        super().__init__(detection_model_path)
        if target == "activity":
            self.model = densenet121(num_classes=15)
        else:
            self.model = densenet121()
        self.model.load_state_dict(torch.load(self.model_path))
        self.model.eval()
        self.target = target

    def predict_class(self, img_path: str, ) -> ClassifierPrediction:
        img = Image.open(img_path)
        # img = F.pil_to_tensor(img)

        transform = transforms.Compose([
            transforms.Resize(
                size=(224, 224)
            ),
            transforms.ToTensor(),
        ])

        img_t = transform(img)
        batch_t = torch.unsqueeze(img_t, 0)
        out = self.model(batch_t)

        probabilities = torch.nn.functional.softmax(out[0], dim=0)
        top_prob, top_catid = torch.topk(probabilities, 1)
        if self.target == "dress_code":
            pred = ClassifierPrediction(predicted_class=DressCode(int(top_catid)), probability=top_prob)
        else:
            pred = ClassifierPrediction(predicted_class=Activity(int(top_catid)), probability=top_prob)

        return pred

