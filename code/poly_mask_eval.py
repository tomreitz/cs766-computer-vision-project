import cv2
import numpy as np
#import matplotlib.pyplot as plt
#import os

def poly_mask_eval(image, np_polygon_array, blockSize = 5, weightedMean = 8):
    """Evaluates an image inside of a polygon.

    Keyword arguments:
    img_path -- relative path to image
    np_polygon_arry -- polygon points to use for masking (np.array with dtype=np.int32)
    blockSize -- number to determine how large a block to use in thresholding (default == 5)
    weightedMean -- number used to determine what to subtract from mean in thresholding (default == 8)
    """
    #check to see if img_path exists (guard)
    #commented out to change for cv(image obj) rather than path
    # if(not os.path.exists(img_path)): return "img_path must be provided"
    #check to see if np_polygon_arry exists (guard)
    if(not isinstance(np_polygon_array, np.ndarray)): return "please provide polygon as (np.array with dtype=np.int32)"
    if(not np_polygon_array.dtype == np.int32): return "polygon provided does not type conform to (np.array with dtype=np.int32)"
    
    #commented out to change for cv(image obj) rather than path
    # image = cv2.imread(img_path)


    mask = np.zeros(image.shape, dtype=np.uint8)
    
    channel_count = image.shape[2]
    ignore_mask_color = (255,)*channel_count

    #should use cv2.fillConvexPoly if we know it's convex
    cv2.fillPoly(mask, np_polygon_array, ignore_mask_color)

    #apply mask
    masked_image = cv2.bitwise_and(image, mask)

    #commented out to change for cv(image obj) rather than path
    #save the result
    # cv2.imwrite(add_name(img_path, "_masked"), masked_image)

    #convert to grayscale
    gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)

    #Show the current 3 channel histogram
    #plt.figure()
    #plt.title('Color Histogram')
    #plt.xlabel('Bins')
    #plt.ylabel('# of pixels')
    #colors = ('b', 'g', 'r')
    #for i,col in enumerate(colors):
    #    hist = cv2.calcHist([masked_image], [i], None, [256], [0,256])
    #    plt.plot(hist, color=col)
    #    plt.xlim([0,256])

    #plt.show()

    #TODO determine evaluation method for value(s) to return from function

    #Adaptive Thresholding
    # adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
    #                         cv2.THRESH_BINARY_INV, 11, 9)
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                        cv2.THRESH_BINARY_INV, blockSize, weightedMean)
    
    #cv2.imshow('Adaptive Thresholding', adaptive_thresh)

    #contours
    contours, hierarchies = cv2.findContours(adaptive_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # print(f'{len(contours)} contour(s) found')

    blank = np.zeros(image.shape, dtype='uint8')

    cv2.drawContours(blank, contours, -1, (0,0,255), 1)
    #cv2.imshow('Contours Drawn', blank)

    return len(contours)

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
