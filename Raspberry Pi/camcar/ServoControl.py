import RPi.GPIO as GPIO
import time
import random

class Servo:

    def __init__(self, pin):
        # Setup GPIO mode and the pin as an output
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        
        # Set min and my angle
        self.setMinAngle(0)
        self.setMaxAngle(180)

        # Create pwm control on this pin
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(7)
        self.angle = 90

    def setMinAngle(self, minAngle):
        if minAngle < 0:
            minAngle = 0
        self.minAngle = minAngle

    def setMaxAngle(self, maxAngle):
        if maxAngle > 180:
            maxAngle = 180
        self.maxAngle = maxAngle

    def setAngle(self, angle):
        if angle > self.maxAngle: angle = self.maxAngle
        if angle < self.minAngle: angle = self.minAngle
        self.angle = angle
        # Calculate the duty and send it to the pwm
        duty = float(angle) / 20.0 + 2.5
        self.pwm.ChangeDutyCycle(duty)

    def getAngle(self):
        return self.angle

if __name__=='__main__':
    servo1 = Servo(18)
    servo2 = Servo(12)
    time.sleep(1)
    while 1:
        servo1.setAngle(random.randint(80, 100))
        servo2.setAngle(random.randint(80, 100))
        time.sleep(0.5)
