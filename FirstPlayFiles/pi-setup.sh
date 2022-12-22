sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install python3-pip

mkdir -p Projects/Python/tflite
cd Projects/Python/tflite
python3 -m pip3 install virtualenv
python3 -m venv tflite-env
source tflite-env/bin/activate

sudo apt-get install python3-pip

sudo apt -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev

sudo apt -y install qt4-dev-tools libatlas-base-dev libhdf5-103 

python3 -m pip3 install opencv-contrib-python

uname -m
python --version
