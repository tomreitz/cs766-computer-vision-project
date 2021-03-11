import cv2 as cv

img = cv.imread('Photos/rhytides.jpg')
cv.imshow('Rhytides', img)

def rescaleFrame(frame, scale=0.75):
    #Images Videos and Live Videos
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

resized_image = rescaleFrame(img, 0.4)
cv.imshow('Image', resized_image)

def changeRes(width, height):
    #Live Video
    capture.set(3,width)
    capture.set(4,height)

# capture = cv.VideoCapture('Videos/noice.mp4')

# while True:
#     isTrue, frame = capture.read()

#     frame_resized = rescaleFrame(frame)

#     cv.imshow('Video', frame)
#     cv.imshow('Video Resized', frame_resized)

#     # if letter d is pressed we break out
#     if cv.waitKey(20) & 0xFF == ord('d'):
#         break

# capture.release()
# cv.destroyAllWindows()

cv.waitKey(0)