In this project, I'm using Arducam on a RPi3 and TensorFlow.

The installation was complicated. 

First - Installing Arducam
--------------------------
This was complicated. The ardu_setup.sh script might help, but 
I think you need to do something else to make it all work. The 
first step is to get an image with 
	
	libcamera-still -n -o out.jpg --autofocus
	
The way to make this happen is to get the imx519 driver installed properly.
Something that must be in place for libcamera to work is that in the file 
/boot/config.txt there must be a line 'dtoverlay=imx519'. Mine said
'dtoverlay=arducam' to start with. 

Second - Gstreamer
------------------
The signal from the imx519 is in some sort of Raw format that can't be 
read by lots of things. The way to get the video from imx519 to OpenCV 
is to use Gstreamer, which is part of libcamera. 

	gst-launch-1.0 videotestsrc ! ximagesink
	
The above should get you test pop-up window with some colours and some
static. This is a good start. The below should get you a video stream 
from the arducam

	gst-launch-1.0 libcamerasrc ! videoconvert ! ximagesink
	

Third - OpenCV
--------------
The version of OpenCV that you install when you use pip or apt-get doesn't 
work. Mine didn't have Gstreamer support built in. The tricky thing here 
is that you can build OpenCV from source but python might still be using 
the other/old version. This shows you the version python3 will actually 
be using. Gstreamer needs to say "ON"

	python3 -c "import cv2; print(cv2.getBuildInformation())"
	
opencv_build_from_source.sh runs through the guide 
https://linuxize.com/post/how-to-install-opencv-on-raspberry-pi/
You just have to set the swapfile size to 1024 before you run the 
script. Make sure you remember to switch back afterwards. See the guide
for how to do it.

Fourth - TFLite
---------------
There's another script for this. I don't remember if it works.

The FirstPlayFiles and Surveillance is based on 	
https://github.com/tensorflow/examples.git
examples/lite/examples/object_detection/raspberry_pi/
	
