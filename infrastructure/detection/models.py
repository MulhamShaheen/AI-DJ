from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
import logging

import numpy as np

from contour import Contour


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
        logging.info('Loading Detector')
        self.model_path = detection_model_path

    def detect_contours(self, image: np.ndarray) -> List[DetectorPrediction]:
        # create square 100x100 pixels contour
        dummy_contour = Contour(bounding_rect=(0, 0, 100, 100))
        prediction = DetectorPrediction(predicted_contour=dummy_contour, contour_probability=0.98)
        return [prediction]
