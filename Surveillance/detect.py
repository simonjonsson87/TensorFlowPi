
import argparse
import sys
import time, json, os, shutil
from datetime import datetime
import SimonsUtils as SJUtils

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

import Arducam






script_path = __file__.replace( os.path.basename(__file__), "")
print(script_path )
CONFIG_FILE = script_path + "config.txt"
toDetect_FILE = script_path + "toDetect.txt"

CONFIG = json.load(open(CONFIG_FILE, "r"))
toDetect = json.load(open(toDetect_FILE, "r"))


model = script_path + 'efficientdet_lite0.tflite'
num_threads = 1
enable_edgetpu = False

total, used, free = shutil.disk_usage("/")
print("Total: %d GiB" % (total // (2**30)))
print("Used: %d GiB" % (used // (2**30)))
print("Free: %d GiB" % (free // (2**30)))

SJUtils.getCaptureFolderSize(CONFIG['RESULT_IMAGE_PATH'])

os.system('/usr/local/bin/libcamera-still -t 10000 -n -o libcam-still_out.jpg --autofocus')


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

timer = SJUtils.SimonsTimer()
timerstart = 0

# Continuously capture images from the camera and run inference
while cam.isOpened():
    timer.start("Starting the loop!")

    # Grab a frame
    image = cam.getFrame()
    timer.milestone("Grabbed image")
    
    # Calculate the FPS
    counter += 1
    if counter % fps_avg_frame_count == 0:
      end_time = time.time()
      fps = fps_avg_frame_count / (end_time - start_time)
      print("fps: " + str(fps)[:4])
      start_time = time.time()

    image_small = image
    image_small = cv2.resize(image_small, (640, 480))

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    timer.milestone("Calculated fps, converted image and created object")

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)

    timer.milestone("Done detecting")

    for detection in detection_result.detections:
        #print(detection.categories)
        #print(detection.bounding_box)
        #print("--------------")
        for category in detection.categories:
            print(str(category.category_name) + "\t\t" + str(category.score) + "\t\t")
            for tode in toDetect:
                if category.score > tode['score'] and category.category_name == tode['category_name']:
                    if tode['ring'] > 0:
                        SJUtils.ring()
                        name = CONFIG['RESULT_IMAGE_PATH'] + datetime.now().strftime("%Y-%m-%d_%H%M%S_") + tode['category_name']
                        cv2.imwrite(name + '.jpg', image)
                        SJUtils.saveBoundingBox(detection.bounding_box, category, name + ".json")

    timer.milestone("Checked result")




    if (time.time() - timerstart > CONFIG["DIAGNOSTIC_IMAGE_INTERVAL"]):
      timerstart = time.time()

      # Draw keypoints and edges on input image
      image_small = utils.visualize(image_small, detection_result)

      # Show the FPS
      fps_text = 'FPS = {:.1f}'.format(fps)
      text_location = (left_margin, row_size)
      cv2.putText(image_small, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,font_size, text_color, font_thickness)

      cv2.imwrite(script_path + 'out_small.jpg', image_small)
      cv2.imwrite(script_path + 'out_big.jpg', image)

      timer.milestone("Done post processing")

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break

    # This is so we have an easy way of stopping the script while running.
    if os.path.exists(script_path + "stop.txt"):
      break 

    if SJUtils.getCaptureFolderSize(CONFIG['RESULT_IMAGE_PATH']) > 5:
      print("We're not doing this because the capture folder has too much data in it.")
      break  

    timer.done()   
      
