This directory contains our code for processing face images. To use it, install the required Python dependencies:
```
pip install cv2 numpy matplotlib shapely
```
Next, download the required face-detection models to this directory:
```
wget https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt2.xml
wget https://github.com/kurnianggoro/GSOC2017/raw/master/data/lbfmodel.yaml
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```
Then specify your input directory at line 77 and run main_2.py:
```
python main_2.py > output.csv
```
This produces a CSV file with rhytide measurements for each input image. The file is interspersed with lines beginning "XXXXXXXXXX" for debugging purposes - you can remove these lines with a command like
```
grep -v "XXXXXX" output.csv > output-clean.csv
```
You may also need to remove the final line of the output, which is a system message from lbfmodel.

Finally, you can post-process the output CSV file using the two "data exploration" Python Notebooks in this directory.
