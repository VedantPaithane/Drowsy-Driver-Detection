# -*- coding: utf-8 -*-
"""YOLO_Pretrained.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lYw4qbCLVD2z6BEv694Ov6Pb55uH-fEW
"""

!pip install ultralytics
!pip install roboflow

from ultralytics import YOLO
from PIL import Image
import matplotlib.pyplot as plt
import os
from IPython.display import Image, display
from IPython import display
display.clear_output()
#!yolo mode=checks

from roboflow import Roboflow

rf = Roboflow(api_key="lYsrKbC6Xq347glFDeA7")
project = rf.workspace("luka-24jet").project("drowsy_driver-i2wpd")
version = project.version(8)
dataset = version.download("yolov8")

# List all versions to check
#print(project.list_versions())

!yolo task=detect mode=train model=yolov8m.pt data={dataset.location}/data.yaml epochs=30 imgsz=640

#confusion matrix
Image(filename='/content/runs/detect/train/confusion_matrix.png', width=600)

# plot the model training results
Image(filename='/content/runs/detect/train/results.png', width=800)

!yolo task=detect mode=val model=/content/runs/detect/train/weights/best.pt data={dataset.location}/data.yaml

!yolo task=detect mode=predict model=/content/runs/detect/train/weights/best.pt source={dataset.location}/test/images

import glob
from IPython.display import Image, display
file_list = glob.glob('/content/runs/detect/predict/*.jpg')
for filename in file_list[:10]:
  display(Image(filename=filename))

# Load a model
model = YOLO("yolov8n.pt")  # pretrained YOLOv8n model


def yolo_process(results):
  for i in range(len(results)):
      result = results[i]
      boxes = result.boxes  # Boxes object for bounding box outputs
      masks = result.masks  # Masks object for segmentation masks outputs
      keypoints = result.keypoints  # Keypoints object for pose outputs
      probs = result.probs  # Probs object for classification outputs
      obb = result.obb  # Oriented boxes object for OBB outputs
      #result.show()  # display to screen
      result.save(filename=f"result_{i}.jpg")  # save to disk

def viz_yolo_image(results):
  for i in range(len(results)):
    # Path to the image
    image_path = f'/content/result_{i}.jpg'

    # Load the image
    image = Image.open(image_path)

    # Display the image
    plt.figure(figsize=(8, 8))  # Adjust display size
    plt.imshow(image)
    plt.axis('off')  # Hide axes ticks
    plt.show()

# Run batched inference on a list of images
results = model(["/content/0EDC4054-0278-467C-BF40-EC582CB0A95E.jpeg","/content/05DD18C9-B285-4597-9656-9F50382B0A2F.jpeg"])  # return a list of Results objects
yolo_process(results)
viz_yolo_image(results)