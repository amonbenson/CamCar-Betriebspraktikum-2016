from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time

def detectColor(image, color, col_abs, min_s):
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range of magenta in HSV
    lower = np.array([(color - col_abs) / 360.0 * 256, min_s / 100.0 * 255, 20])
    upper = np.array([(color + col_abs) / 360.0 * 256, 255, 255])

    # Threshold the HSV image to a mask
    mask = cv2.inRange(hsv, lower, upper)

    # Get the histogram and calculate the x and y position
    s0 = mask[:,:].sum(0)
    s1 = mask[:,:].sum(1)
    x = -1
    y = -1
    if np.max(s0) > 5000:
        x = np.argmax(s0)
    if np.max(s1) > 5000:
        y = np.argmax(s1)

    # Return the x and y coordinates
    return x, y

if __name__ == '__main__':

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.rotation = 180
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # Detect a color
        image = frame.array
        x, y = detectColor(image, 100, 15, 75)
        if (x >= 0 and y >= 0):
            cv2.circle(image, (x, y), 5, (255, 255, 255))

        # Show the frame
        cv2.imshow('Frame', image)
        key = cv2.waitKey(1) & 0xFF

        # Clear the buffer
        rawCapture.truncate()
        rawCapture.seek(0)

        # Check if key was 'q'
        if key == ord('q'):
            break
