#
# Simon:
# Note that before this is executed, the swapfile size should be increased to 1024.
# Don't forget to turn it back to 100 after you're done.
#
#



echo "##################### All the sudo apt installs #################################"
sudo apt update
sudo apt install build-essential cmake git pkg-config libgtk-3-dev "libcanberra-gtk*"
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
sudo apt install libjpeg-dev libpng-dev libtiff-dev gfortran openexr libatlas-base-dev opencl-headers
sudo apt install python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev


echo "##################### Create folder and download the repos #################################"
rm ~/opencv_build -rf
mkdir ~/opencv_build && cd ~/opencv_build
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
mkdir -p ~/opencv_build/opencv/build && cd ~/opencv_build/opencv/build

echo "##################### cmake #################################"
cmake --clean-first -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D ENABLE_NEON=ON \
    -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D WITH_GSTREAMER=ON \
    -D WITH_GSTREAMER_0_10=OFF \
    -D VIDEOIO_PLUGIN_LIST=gstreamer \
    -D BUILD_EXAMPLES=OFF ..
# The GSTREAMER_0_10=OFF and VIDEOIO_PLUGIN_LIST=gstreamer lines were key in making this work.

echo "##################### make #################################"
make -j1 PLATTFORM='rpi3'

echo "##################### make install #################################"
sudo make install

echo "##################### Python check #################################"
python3 -c "import cv2; print(cv2.__version__)"
