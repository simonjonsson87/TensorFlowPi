This is a simple obejct detection project based on the sample code provided by the TensorFlow project. The code is written for a Rasperry Pi 3 with an Arducam camera.

## Folder: FirstPlayFiles
This is simply some initial experimentation to get to know the code

## Folder: Surveillance
This is the project I made (though still based on the TensorFlow sample code). You can tell the code what sort of objects you are interested in (using Surveillance/toDetect.txt), and when it detects one, it saves an image of it. 

There is also a Surveillance/config.txt file where the output path for the images can be configured.

## File: Simons_Setup_Guide.txt
This project used a Rasperry Pi 3 with an Arducam. The Arducam was difficulty to setup to work with TensorFlow. Hence, I wrote this guide to how it's done. 

## File: on_boot.sh
This is simple the script which is run from crontab to make Surveillance start with the Raspberry Pi boots up. 