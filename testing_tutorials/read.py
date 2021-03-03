import cv2 as cv

# img = cv.imread('Photos/rhytides.jpg')

# cv.imshow('Rhytides', img)
capture = cv.VideoCapture('Videos/noice.mp4')

while True:
    isTrue, frame = capture.read()
    cv.imshow('Video', frame)

    # if letter d is pressed we break out
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()

cv.waitKey(0)
