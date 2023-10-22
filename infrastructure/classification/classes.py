from enum import Enum
from typing import Optional, Tuple

import cv2
import numpy as np


class Activity:

    def __init__(self,
                 activity_id: Optional[int] = None,
                 activity: Optional[str] = None,
                 ):
        """
           :param activity_id: int value of predicted class
           :param activity: str value of the class name
           """

        self._activity_dict = {
            0: "calling",
            1: "clapping",
            2: "cycling",
            3: "dancing",
            4: "drinking",
            5: "eating",
            6: "fighting",
            7: "hugging",
            8: "laughing",
            9: "listening_to_music",
            10: "running",
            11: "sitting",
            12: "sleeping",
            13: "texting",
            14: "using_laptop",
        }
        self._activity_count = 14

        if activity is None:
            if activity_id is None or activity_id > self._activity_count:
                raise ValueError(f'activity_id is not correct. Got = {activity_id}')
            else:
                self._activity = self._activity_dict[activity_id]
        else:
            self._activity_id = list(self._activity_dict.values()).index(activity)
            self._activity = activity

    @property
    def get_name(self):
        return self._activity
