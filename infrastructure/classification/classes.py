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


class DressCode:

    def __init__(self,
                 dress_code_id: Optional[int] = None,
                 dress_code: Optional[str] = None,
                 ):
        """
           :param dress_code_id: int value of predicted class
           :param dress_code: str value of the class name
           """

        self._dress_code_dict = {
            0: "casual",
            1: "sport",
            2: "formal",
        }
        self._dress_code_count = 14

        if dress_code is None:
            if dress_code_id is None or dress_code_id > self._dress_code_count:
                raise ValueError(f'dress_code_id is not correct. Got {dress_code_id}')
            else:
                self._dress_code = self._dress_code_dict[dress_code_id]
        else:
            self._dress_code_id = list(self._dress_code_dict.values()).index(dress_code)
            self._dress_code = dress_code

    @property
    def get_name(self):
        return self._dress_code
