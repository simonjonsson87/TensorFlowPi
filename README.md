This is a simple object detection project based on the sample code provided by the TensorFlow project. The code is written for a Raspberry Pi 3 with an Arducam camera.

## FirstPlayFiles
This is simply some initial experimentation to get to know the code and the functionality of TensorFlow.

## Surveillance
This is the project I made (though still based on the TensorFlow sample code). The purpose of the project is that a Raspberry Pi with a camera can be placed somewhere and record images of objects that are of interest.

Interesting object categories can be configured in Surveillance/toDetect.txt. The file contains JSON and there are three keys:
- category_name: This is the name of the object category. E.g. 'Cat'.
- score: This is the level of certainty the model must have for the script to save the picture. A value between 0 and 1.
- ring: Whether or not an alarm should go off when the type of object is detected. This is not implemented now, but might be in the future.

There is also a Surveillance/config.txt file where the output path for the images can be configured.

To stop execution of the script, just create a file called 'stop.txt' in the same directory as the script. This is useful when the script has been started using crontab.

The main script is Surveillance/detect.py

## File: Simons_Setup_Guide.txt
This project used a Raspberry Pi 3 with an Arducam. The Arducam was difficult to set up to work with TensorFlow. Hence, I wrote this guide on how it’s done.

## File: on_boot.sh
This is simply the script which is run from crontab to make Surveillance start when the Raspberry Pi boots up.
