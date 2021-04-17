import cv2
import numpy as np
import math
from shapely.geometry import Polygon
#import matplotlib.pyplot as plt
import os

def poly_mask_eval(image, np_polygon_array, blockSize = 5, weightedMean = 8, name='test'):
    """Evaluates an image inside of a polygon.

    Keyword arguments:
    img_path -- relative path to image
    np_polygon_arry -- polygon points to use for masking (np.array with dtype=np.int32)
    blockSize -- number to determine how large a block to use in thresholding (default == 5)
    weightedMean -- number used to determine what to subtract from mean in thresholding (default == 8)
    """
    if(not isinstance(np_polygon_array, np.ndarray)): return "please provide polygon as (np.array with dtype=np.int32)"
    if(not np_polygon_array.dtype == np.int32): return "polygon provided does not type conform to (np.array with dtype=np.int32)"
    
    mask = np.zeros(image.shape, dtype=np.uint8)
    channel_count = image.shape[2]
    ignore_mask_color = (255,)*channel_count

    #should use cv2.fillConvexPoly if we know it's convex
    cv2.fillPoly(mask, np_polygon_array, ignore_mask_color)

    #apply mask
    masked_image = cv2.bitwise_and(image, mask)

    #convert to grayscale
    gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)

    #TODO determine evaluation method for value(s) to return from function

    # from https://www.sicara.ai/blog/2019-03-12-edge-detection-in-opencv
    gray = cv2.GaussianBlur(gray,(5,5),0)

    h,w = gray.shape;
    polygon = Polygon(np.vstack([np_polygon_array[0], np_polygon_array[0][0]]))
    polygon_image = np.zeros((h,w), np.uint8)
    cv2.polylines(polygon_image, np.int32(np_polygon_array), True, (255,255,255), 2)

    # We do canny edge detection at 4 different thresholds, so a weigthed sum can estimate the intensity/depth of wrinkles:
    steps = 4
    edge_pixel_counts = np.zeros(steps)
    #cv2.imwrite(os.getcwd()+'/annotated/'+name+'.jpg', gray)
    for i in range(1,steps+1):
        low = 20*(i-1) + 15 # from 15 to 75
        high = low + 20 # from 35 to 95
        edges_filtered = cv2.Canny(gray, low, high)
        edges_filtered -= polygon_image
        #cv2.imwrite(os.getcwd()+'/annotated/'+name+'-'+str(low)+'-'+str(high)+'.jpg', edges_filtered)
        edge_pixel_counts[i-1] = cv2.countNonZero(edges_filtered)
    edge_pixel_weights = [0.05, 0.15, 0.3, 0.5] # lower thresholds give many more edge pixels, so we weight them lower
    # intuition here is high thresholds will detect large/deep/defined rhytides; lower thresholds wil detect (many more) small ones

    # return weighted edge pixel counts, normalized by polygon area: "wrinkle intensity density"
    return np.dot(edge_pixel_counts, edge_pixel_weights)/polygon.area


def add_name(path, name):
    """Return the updated path when adding name to the filename"""
    head, tail = os.path.split(path)
    name_space, data_sgn = tail.split('.')
    name_space += name
    name_space += '.' + data_sgn
    return os.path.join(head, name_space)

#print(add_name("Photos/Michael_Shapiro.jpg", "_masked"))

#test_poly = np.array([[(10,10), (300,300), (10,300), (30,200)]], dtype=np.int32)
#print(poly_mask_eval(cv2.imread("Photos/Michael_Shapiro.jpg"), test_poly))

#cv2.waitKey(0)
