# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# The current frame
image = None

# The mainloop will be called whenever a new frame is read from the camera
def mainloop():
    # Get the global image
    global image

    # Start manipulating the color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([60, 150, 100], dtype=np.uint8)
    upper = np.array([85, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    image = cv2.bitwise_and(image, image, mask=mask)

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
    #image = frame.array
    image = currentFrame.array

    # mainloop
    mainloop()
 
    # show the frame and close on 'q'
    cv2.imshow('Frame', image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    # clear the stream for the next frame
    rawCapture.truncate(0)
