from clearml import PipelineController
from clearml.automation.controller import PipelineDecorator


@PipelineDecorator.component(return_values=['model'], cache=True)
def step_one(yolo_version: str, extra: int = 43):
  import torch.hub

  model = torch.hub.load('ultralytics/yolov5', yolo_version)
  return model

@PipelineDecorator.component(return_values=['img'], cache=True)
def step_two(img_url: str, extra: int = 43):
  from PIL import Image
  from torchvision.transforms import functional as F
  from clearml import StorageManager

  local_img_path = StorageManager.get_local_copy(remote_url=img_url)
  img = Image.open(local_img_path)
  img = F.pil_to_tensor(img)

  return img

@PipelineDecorator.component(return_values=['predictions'], cache=True)
def step_three(model, img):
  predictions = []
  results = model(img)

  for result in results.xyxy[0]:
    # 0  749.50   43.50  1148.0  704.5    0.874023      0  person

    if int(result[5]) == 0:
      width = result[2] - result[0]
      height = result[3] - result[1]
      predictions.append([result[0], result[1], width, height])

  return predictions


@PipelineDecorator.pipeline(
  name='pipeline', project='examples', version='0.1',
  args_map={'General':['yolo_version'], 'Mock':['mock_parameter']}
)
def main(yolo_version, mock_parameter="Mock"):
  pass


