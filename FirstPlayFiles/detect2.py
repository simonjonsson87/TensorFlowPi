import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

import Arducam

model = 'efficientdet_lite0.tflite'
num_threads = 1
enable_edgetpu = False

# Variables to calculate FPS
counter, fps = 0, 0
start_time = time.time()

# Start capturing video input from the camera
cam = Arducam.Arducam()

# Visualization parameters
row_size = 20  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 255)  # red
font_size = 1
font_thickness = 1
fps_avg_frame_count = 10

# Initialize the object detection model
base_options = core.BaseOptions(file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
detection_options = processor.DetectionOptions(max_results=3, score_threshold=0.3)
options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)

# Continuously capture images from the camera and run inference
while cam.isOpened():

    image = cam.getFrame()
    
    # Calculate the FPS
    counter += 1
    if counter % fps_avg_frame_count == 0:
      end_time = time.time()
      fps = fps_avg_frame_count / (end_time - start_time)
      print(fps)
      start_time = time.time()

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)
    print(detection_result)

    # Draw keypoints and edges on input image
    image = utils.visualize(image, detection_result)

    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)

    cv2.imwrite('out.jpg', image)

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break