from abc import ABC, abstractmethod
from PIL import Image
import torch.hub
from torch import hub
from torchvision.transforms import functional as F
from typing import List
from dataclasses import dataclass
import logging

import numpy as np

from .contour import Contour

@dataclass
class DetectorPrediction:
    predicted_contour: Contour
    contour_probability: float


class Detector(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def detect_contours(self, image: np.ndarray) -> List[DetectorPrediction]:
        """
        Return boxes of all detected contours from image.
        :param image: np.ndarray RGB image
        :return: List[Contour]
        """
        pass


class DummyDetector(Detector):

    def __init__(self, detection_model_path: str):
        logging.info('Loading Classifior')
        self.model_path = detection_model_path

    def detect_contours(self, image: np.ndarray) -> List[DetectorPrediction]:
        # create square 100x100 pixels contour
        dummy_contour = Contour(bounding_rect=(0, 0, 100, 100))
        prediction = DetectorPrediction(predicted_contour=dummy_contour, contour_probability=0.98)
        return [prediction]


class YoloV5Detector(DummyDetector):

    def __init__(self, detection_model_path: str = None):
        super().__init__(detection_model_path)
        self._load_model()

    def _load_model(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.model.classes = [0]

    def detect_contours(self, img_path: str):
        predictions = []
        img = Image.open(img_path)
        img = F.pil_to_tensor(img)
        results = self.model(img)
        for result in results.xyxy[0]:

            if int(result[5]) == 0:
                width = result[2] - result[0]
                height = result[3] - result[1]
                contour = Contour(bounding_rect=(result[0], result[1], width, height))
                predictions.append(contour)

        return predictions

    def save_predictions(self, img_path: str, path: str):
        predictions = self.model(img_path)
        return predictions.crop(save=True, save_dir=path)
