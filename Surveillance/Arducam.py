import sys

import cv2

class Arducam:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self): 
        # Start capturing video input from the camera 
        #cmd = "libcamerasrc ! videoconvert ! appsink "
        # 4656×3496, 2328x1748
        #cmd = "libcamerasrc ! videoconvert ! appsink max-buffers=1 drop=True"
        
        #Works cmd = "libcamerasrc ! video/x-raw,width=1920,height=1080 ! videoconvert ! appsink max-buffers=1 drop=True"
        cmd = "libcamerasrc ! video/x-raw,width=4640,height=3488,framerate=5/1 ! videoconvert ! appsink max-buffers=1 drop=True"
        self.cam = cv2.VideoCapture(cmd, cv2.CAP_GSTREAMER)

    def isOpened(self):
        return self.cam.isOpened()

    def getFrame(self):
        success, image = self.cam.read()
        if not success:
            sys.exit('ERROR: Unable to read from camera')
        #image = cv2.flip(image, 1)    
        return image        

    def __del__(self):
        print("In del!")
        self.cam.release()
        cv2.destroyAllWindows()
