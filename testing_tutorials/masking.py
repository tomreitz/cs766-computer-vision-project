import cv2 as cv
import numpy as np

img = cv.imread('Photos/cats.jpg')
cv.imshow('Cats', img)

blank = np.zeros(img.shape[:2], dtype='uint8')
cv.imshow('Blank Image', blank)

mask = cv.circle(blank, (img.shape[1]//2 + 45, img.shape[0]//2), 100, 255, -1)
cv.imshow('Mask', mask)

# rectangle = cv.rectangle(blank.copy(), (30,30), (570,570), 255, -1)

# weird_shape = cv.bitwise_and(circle, rectangle)
# cv.imshow('Weird Shape', weird_shape)

masked = cv.bitwise_and(img, img, mask=mask)
cv.imshow('Masked Image', masked)

cv.waitKey(0)