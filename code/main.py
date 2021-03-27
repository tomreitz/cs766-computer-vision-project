import os
#import OpenCV library
import cv2
#import dlib facial landmark detection library
#import dlib
#import NumPy for processing facial landmarks
import numpy as np
#import matplotlib library
import matplotlib.pyplot as plt
from poly_mask_eval import poly_mask_eval

def convertToRGB(img): 
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# code borrowed from https://github.com/nlhkh/face-alignment-dlib
LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]

def rect_to_tuple(rect):
    left = rect.left()
    right = rect.right()
    top = rect.top()
    bottom = rect.bottom()
    return left, top, right, bottom

def extract_eye(shape, eye_indices):
    points = shape[[x for x in eye_indices]]
    return list(points)

def extract_eye_center(shape, eye_indices):
    points = extract_eye(shape, eye_indices)
    xs = map(lambda p: p[0], points)
    ys = map(lambda p: p[1], points)
    return sum(xs) // 6, sum(ys) // 6

def extract_left_eye_center(shape):
    return extract_eye_center(shape, LEFT_EYE_INDICES)

def extract_right_eye_center(shape):
    return extract_eye_center(shape, RIGHT_EYE_INDICES)

def angle_between_2_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    tan = (y2 - y1) / (x2 - x1)
    return np.degrees(np.arctan(tan))

def get_rotation_matrix(p1, p2):
    angle = angle_between_2_points(p1, p2)
    x1, y1 = p1
    x2, y2 = p2
    xc = (x1 + x2) // 2
    yc = (y1 + y2) // 2
    M = cv2.getRotationMatrix2D((xc, yc), angle, 1)
    return M

def crop_image(image, det):
    #left, top, right, bottom = rect_to_tuple(det)
    height, width = image.shape[:2]
    (x,y,w,d) = det
    wpadding = 0.1*w
    dpadding = 0.1*d
    top = int(max(0, round(y-dpadding)))
    bottom = int(min(height, round(y+d+dpadding)))
    left = int(max(0, round(x-wpadding)))
    right = int(min(width, round(x+w+wpadding)))
    return image[top:bottom, left:right]

# code borrowed from https://medium.com/analytics-vidhya/facial-landmarks-and-face-detection-in-python-with-opencv-73979391f30e
haarcascade = "haarcascade_frontalface_alt2.xml"
detector = cv2.CascadeClassifier(haarcascade)
LBFmodel = "lbfmodel.yaml"
landmark_detector  = cv2.face.createFacemarkLBF()
landmark_detector.loadModel(LBFmodel)

#input_dir = "./"
#input_dir = "/Users/tom/Projects/School/UW-Masters/Spring-2021/cs766/project/datasets/UTKFace/"
#input_dir = "/Users/tom/Projects/School/UW-Masters/Spring-2021/cs766/project/datasets/wiki_crop/00/"
#input_dir = "/Users/tom/Projects/School/UW-Masters/Spring-2021/cs766/project/datasets/imdb_crop/00/"
#output_dir = './annotated/'
#output_dir = './UTKFace-annotated/'
#output_dir = './wiki_crop_annotated/'
#output_dir = './imdb_crop_annotated/'
#files = os.listdir( input_dir )
num_processed = 0
num_faces = 0

images = []
with open('meta.csv', 'r') as f:
    lines = f.readlines()
    for l in lines:
        images.append(l.strip())

print('image,bytes,width,height,age,gender,forehead,frown,upper_eye_hood_left,upper_eye_hood_right,crows_feet_left,crows_feet_right,crows_feet_right,bunny_lines_left,bunny_lines_right,bags_left,bags_right,laugh_lines_left,laugh_lines_right,jowls_left,jowls_right,lip_lines,mental_crease')
for row in images:
    tmp = row.split(',')
    file = '/Users/tom/Projects/School/UW-Masters/Spring-2021/cs766/project/datasets/'+tmp[2]
    if(file.endswith(".jpg")):
        img = cv2.imread(file)
        #print('processing '+file)
        num_processed += 1
        height, width = img.shape[:2]
        # scale every image to max 1000 pixels in either dimension
        if height>width: scale = 1000/height
        else: scale = 1000/width
        s_height, s_width = round(height*scale), round(width*scale)
        img = cv2.resize(img, (s_width, s_height))
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = detector.detectMultiScale(gray_img)
        if len(faces)>0:
            _, landmarks = landmark_detector.fit(gray_img, faces)
            shape = landmarks[0][0]
    
            left_eye = extract_left_eye_center(shape)
            right_eye = extract_right_eye_center(shape)
            M = get_rotation_matrix(left_eye, right_eye)
            rotated = cv2.warpAffine(img, M, (s_width, s_height), flags=cv2.INTER_CUBIC)
            cropped = crop_image(rotated, faces[0])
    
            # re-extract landmarks in aligned face and annotate them
            gray_img = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray_img)
            if len(faces)>0:
                #landmark_detector  = cv2.face.createFacemarkLBF()
                #landmark_detector.loadModel(LBFmodel)

                _, landmarks = landmark_detector.fit(gray_img, faces)
                rhytide_polygon_index = {
                    'forehead': [1, 18, 19, 20, 21, 24, 25, 26, 27],
                    'frown': [21, 22, 28, 23, 24],
                    'upper_eye_hood_left': [18, 19, 20, 21, 40, 39, 38, 37],
                    'upper_eye_hood_right': [24, 25, 26, 27, 46, 45, 44, 43],
                    'crows_feet_left': [1, 2, 37, 18],
                    'crows_feet_right': [17, 16, 46, 27],
                    'bunny_lines_left': [22, 28, 29, 30, 40], # include 30?
                    'bunny_lines_right': [23, 28, 29, 30, 43], # include 30?
                    'bags_left': [2, 3, 40, 41, 42, 37], # remove 29?
                    'bags_right': [16, 15, 43, 48, 47, 46], # remove 29?
                    'laugh_lines_left': [3, 4, 5, 49, 32, 30],
                    'laugh_lines_right': [15, 14, 13, 55, 36, 30],
                    'jowls_left': [5, 6, 7, 60, 49],
                    'jowls_right': [13, 12, 11, 56, 55],
                    'lip_lines': [36, 35, 34, 33, 32, 49, 50, 51, 52, 53, 54, 55],
                    'mental_crease': [7, 8, 9, 10, 11, 56, 57, 58, 59, 60]
                }
                this_row = [tmp[2], str(os.path.getsize(file)), str(width), str(height), str(tmp[0]), str(tmp[1])]
                for key in rhytide_polygon_index:
                    polygon = np.array(landmarks[0][0][[x-1 for x in rhytide_polygon_index[key]]])
                    if key=='forehead':
                        (x,y,w,d) = faces[0]
                        polygon = np.append(polygon, [[x+w,y], [x,y]], axis=0)
                    polygon_centroid = np.average(polygon, axis=0)
                    edges = poly_mask_eval(cropped, np.int32([polygon]), blockSize = 5, weightedMean = 8)
                    this_row.append(str(edges))
                    #color = tuple([int(x) for x in list(np.random.choice(range(256), size=3))])
                    #cv2.putText(cropped,str(edges), (int(polygon_centroid[0]),int(polygon_centroid[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, color)
                    #cv2.polylines(cropped, np.int32([polygon]), True, color, 2)
                #plt.axis("off")
                #plt.figure(figsize = (4,4))
                #plt.imshow(convertToRGB(cropped))
                #plt.show()
                #cv2.imwrite(output_dir+file, cropped)
                print(','.join(this_row))
                num_faces += 1
                if num_faces > 10000: break
            else:
                print('XXXXXXXXX No faces found :( ['+file+']')
        else:
            print('XXXXXXXXXX No faces found :( ['+file+']')
        print('XXXXXXXXXX '+str(num_processed)+' files processed; '+str(num_faces)+' faces found ['+str(round(100*num_faces/num_processed,2))+'%]')
