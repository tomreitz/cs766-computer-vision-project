#!/bin/bash

# install Python dependencies:
pip3 install opencv-contrib-python

# download some testing photos:
wget https://tomreitz.github.io/cs766-computer-vision-project/data/pexels-photo-638196.jpeg
wget https://upload.wikimedia.org/wikipedia/commons/a/a3/Elderly_Gambian_woman_face_portrait.jpg
wget https://upload.wikimedia.org/wikipedia/commons/1/1f/Gardengnome_face.jpg
wget https://upload.wikimedia.org/wikipedia/commons/1/1c/Ami_Bera_wearing_face_mask_-_May_15_2020.jpg
wget https://upload.wikimedia.org/wikipedia/commons/8/81/Michael_Shapiro_NYTF.jpg

# download Haar Cascade and facial landmark model:
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt2.xml
wget https://github.com/kurnianggoro/GSOC2017/raw/master/data/lbfmodel.yaml

