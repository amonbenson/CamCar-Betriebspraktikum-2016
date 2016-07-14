from picamera.array import PiRGBArray
from picamera import PiCamera
import ImageUtils
import cv2
import numpy as np
import time
from CamCar import *
import math

def detectColor(color):
    return ImageUtils.detectColor(image, color, 15, 75)

twist = 0
def getMotorSpeed(angle, speed):
    global twist
    add_twist = twist
    if (angle > 0) != (twist > 0):
        add_twist = 0
        
    lf = math.cos(math.radians(angle + 45 + add_twist))
    rf = math.cos(math.radians(angle - 45 + add_twist))
    return lf * speed, rf * speed

if __name__=='__main__':
    # The mode will control the action of the cam car
    MODE_SEARCH = 0
    MODE_FOLLOW = 1
    MODE_AGGRSV = 2
    mode = MODE_SEARCH

    # The different colors
    h_ball = 240
    h_cup = 100

    # The robot will prefer to drive to one side if this value is not 0
    twist = 0
    twist_abs = 30

    # Create the camcar
    camcar = CamCar()
    camcar.setServoSmoothness(0.9)

    # initialize the camera and grab a reference to the raw camera capture
    camSize = (320, 240)
    camera = PiCamera()
    camera.resolution = camSize
    camera.rotation = 180
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=camSize)

    # allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    counter = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Get the image
        image = frame.array



        # Get the ball, cup1 and cup2 position
        bx, by = detectColor(h_ball)
        cx, cy = detectColor(h_cup)

        # Change the mode
        if cx > -1 and cy > -1:
            # We have a cup! Go aggressive
            mode = MODE_AGGRSV
        elif bx > -1 and by > -1:
            # We have a ball and no cups. Go follow
            mode = MODE_FOLLOW
        else:
            # There's no object. Go search mode
            mode = MODE_SEARCH



        # SEARCH
        if mode == MODE_SEARCH:
            # Rotate the servos in a sine wave to search the ball
            camcar.setXServoRotation(math.sin(counter * 0.11) * 45)
            camcar.setYServoRotation(math.sin(counter * 0.2) * 45)
            # Stop the motors
            camcar.stopMotor(CamCar.MOTOR_LEFT)
            camcar.stopMotor(CamCar.MOTOR_RIGHT)
            # Change to sad mood
            camcar.moodSad()

        # FOLLOW
        elif mode == MODE_FOLLOW:
            # Get the angle of the ball and rotate the servos to these angles
            camW, camH = camSize
            xDeg, yDeg = objectAngle(camcar, bx, by, camW, camH)
            camcar.setXServoRotation(xDeg)
            camcar.setYServoRotation(yDeg)
            # Move the motors to the x angle
            ls, rs = getMotorSpeed(xDeg, -40)
            camcar.runMotor(CamCar.MOTOR_LEFT, ls)
            camcar.runMotor(CamCar.MOTOR_RIGHT, rs)
            # Set the mood to normal
            camcar.moodNormal()

        # AGGRESSIVE
        elif mode == MODE_AGGRSV:
            # Get the angle of the cup and rotate the servos to these angles
            camW, camH = camSize
            xDeg, yDeg = objectAngle(camcar, cx, cy, camW, camH)
            camcar.setXServoRotation(xDeg)
            camcar.setYServoRotation(yDeg)
            # Drive away (add 180 to the angle)
            ls, rs = getMotorSpeed(xDeg + 180, -60)
            camcar.runMotor(CamCar.MOTOR_LEFT, ls)
            camcar.runMotor(CamCar.MOTOR_RIGHT, rs)
            # Set the mood to angry
            camcar.moodAngry()



        # Clear the buffer and increase the counter
        rawCapture.truncate()
        rawCapture.seek(0)
        counter += 1
