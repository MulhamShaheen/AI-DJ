import os.path

from PIL import Image
from infrastructure.classification.models import DummyClassifier
from infrastructure.detection.models import YoloV5Detector


def main(image_path: str, media_path: str, *args, **kwargs):
    if not os.path.isfile(image_path):
        print("path should be an image")
        return False

    file_name = os.path.split(image_path)[-1]
    out_path = os.path.join(media_path, file_name)
    os.makedirs(out_path)

    image = Image.open(image_path)
    detector = YoloV5Detector(detection_model_path="yolov5s")

    detector.save_predictions(image_path, path=out_path)

    classifier = DummyClassifier("model.pt")
    preds = []
    for f in os.scandir(out_path+"/crops/person/"):
        crop = Image.open(f.path)
        pred = classifier.predict_class(crop)
        preds.append(pred)

    return preds