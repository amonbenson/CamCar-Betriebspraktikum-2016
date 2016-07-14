from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 180
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for currentFrame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = currentFrame.array
    #bmask = cv2.compare((img),np.uint8([128]), cv2.CMP_GE)
    #smask = cv2.bitwise_not(bmask)
    #x = np.uint8([90])
    #big = cv2.add(img, x, mask = bmask)
    #small = cv2.add(img, x, mask = smask)
    #img = cv2.add(big, small)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 128, 255, 0)
    _, contours, hierarchy = cv2.findContours(thresh, 1, 2)

    # Show the contours
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow('Frame', img)
    key = cv2.waitKey(1) & 0xFF

    # Clear the buffer
    rawCapture.truncate()
    rawCapture.seek(0)

    # Check if key was 'q'
    if key == ord('q'):
        break
