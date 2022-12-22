
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