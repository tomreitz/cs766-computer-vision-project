import cv2 as cv

img = cv.imread('Photos/cats.jpg')
cv.imshow('Cats', img)

#Averaging
average = cv.blur(img, (7,7))
cv.imshow('Average Blur', average)

#Gaussian Blur
gauss = cv.GaussianBlur(img, (7,7), 0)
cv.imshow('Gaussian Blur', gauss)

#Median Blur
median = cv.medianBlur(img, 7)
cv.imshow('Median Blur', median)

#Bilateral
bilat = cv.bilateralFilter(img, 10, 15, 15)
cv.imshow('Bilateral', bilat)

cv.waitKey(0)