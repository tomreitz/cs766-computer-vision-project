import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

def poly_mask_eval(img_path, np_polygon_array, blockSize = 5, weightedMean = 8):
    """Evaluates an image inside of a polygon.

    Keyword arguments:
    img_path -- relative path to image
    np_polygon_arry -- polygon points to use for masking (np.array with dtype=np.int32)
    """
    #check to see if img_path exists (guard)
    if(not os.path.exists(img_path)): return "img_path must be provided"
    #check to see if np_polygon_arry exists (guard)
    if(not isinstance(np_polygon_array, np.ndarray)): return "please provide polygon as (np.array with dtype=np.int32)"
    if(not np_polygon_array.dtype == np.int32): return "polygon provided does not type conform to (np.array with dtype=np.int32)"
    
    image = cv.imread(img_path)

    mask = np.zeros(image.shape, dtype=np.uint8)
    
    channel_count = image.shape[2]
    ignore_mask_color = (255,)*channel_count

    #should use cv.fillConvexPoly if we know it's convex
    cv.fillPoly(mask, np_polygon_array, ignore_mask_color)

    #apply mask
    masked_image = cv.bitwise_and(image, mask)

    #save the result
    cv.imwrite(add_name(img_path, "_masked"), masked_image)

    #convert to grayscale
    gray = cv.cvtColor(masked_image, cv.COLOR_BGR2GRAY)

    #Show the current 3 channel histogram
    plt.figure()
    plt.title('Color Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of pixels')
    colors = ('b', 'g', 'r')
    for i,col in enumerate(colors):
        hist = cv.calcHist([masked_image], [i], None, [256], [0,256])
        plt.plot(hist, color=col)
        plt.xlim([0,256])

    plt.show()

    #TODO determine evaluation method for value(s) to return from function
    
    #Adaptive Thresholding
    # adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, 
    #                         cv.THRESH_BINARY_INV, 11, 9)
    adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                        cv.THRESH_BINARY_INV, blockSize, weightedMean)
    
    cv.imshow('Adaptive Thresholding', adaptive_thresh)

    #contours
    contours, hierarchies = cv.findContours(adaptive_thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    # print(f'{len(contours)} contour(s) found')

    blank = np.zeros(image.shape, dtype='uint8')

    cv.drawContours(blank, contours, -1, (0,0,255), 1)
    cv.imshow('Contours Drawn', blank)

    return len(contours)

def add_name(path, name):
    """Return the updated path when adding name to the filename"""
    head, tail = os.path.split(path)
    name_space, data_sgn = tail.split('.')
    name_space += name
    name_space += '.' + data_sgn
    return os.path.join(head, name_space)

print(add_name("Photos/Michael_Shapiro.jpg", "_masked"))

test_poly = np.array([[(10,10), (300,300), (10,300), (30,200)]], dtype=np.int32)
print(poly_mask_eval("Photos/Michael_Shapiro.jpg", test_poly))

cv.waitKey(0)