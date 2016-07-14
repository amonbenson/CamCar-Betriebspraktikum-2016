# Import the remote ev3 and the servo control
from RemoteEV3 import EV3
from ServoControl import Servo
import time
import _thread as thread

# This program will return the degrees of an object realative to a camcar
def objectAngle(camcar, px, py, camW, camH):
    # Calculate the degrees of the object realative to the camera
    xFact = 2 * px / camW - 1;
    yFact = 2 * py / camH - 1;
    xDegRel = -xFact * 54 / 4   # Why do we divide by 3 and not by 2?! Well,
    yDegRel = yFact * 41 / 4    # it reduces the robot's head-shaking movement.

    # Now add the existing rotation of the servo motors and return the values
    xDeg = xDegRel + camcar.getXServoRotation()
    yDeg = yDegRel + camcar.getYServoRotation()

    return xDeg, yDeg

# This class is en extension of the remote ev3 to control the cam car
class CamCar(EV3):

    # Motor and sensor constants
    MOTOR_EYES = 'outA'
    MOTOR_CAMERA = 'outB'
    MOTOR_RIGHT = 'outC'
    MOTOR_LEFT = 'outD'
    EYE_LEFT = 'in3'
    EYE_RIGHT = 'in4'

    def __init__(self):
        # Initialize the ev3 with the ev3dev hostname
        super().__init__('ev3dev.local')

        # Creat the servos and reset
        self.xServo = Servo(18)
        self.yServo = Servo(12)
        self.xServo.setMinAngle(45)
        self.xServo.setMaxAngle(135)
        self.yServo.setMinAngle(45)
        self.yServo.setMaxAngle(135)
        self.resetServos()

        # Start the servo control thread
        thread.start_new_thread(self.servoControl, ())

        # Set the motor stop modes
        self.changeMotorStopMode(CamCar.MOTOR_EYES, 'brake')
        self.changeMotorStopMode(CamCar.MOTOR_CAMERA, 'hold')
        self.changeMotorStopMode(CamCar.MOTOR_LEFT, 'brake')
        self.changeMotorStopMode(CamCar.MOTOR_RIGHT, 'brake')

        # Change to normal mood
        self.mood = ''
        self.moodAngry()
        self.moodNormal()

    # Changes the eyybrows and the eye color to match the corresponding
    # mood of the robot.
    def moodNormal(self):
        if self.mood == 'normal': return
        self.changeSensorMode(CamCar.EYE_LEFT, 'COL-COLOR')
        self.changeSensorMode(CamCar.EYE_RIGHT, 'COL-COLOR')
        self.runMotorTimed(CamCar.MOTOR_EYES, -50, 400)
        self.runMotorRelative(CamCar.MOTOR_EYES, 35, 50)
        self.mood = 'normal'

    def moodAngry(self):
        if self.mood == 'angry': return
        self.changeSensorMode(CamCar.EYE_LEFT, 'COL-REFLECT')
        self.changeSensorMode(CamCar.EYE_RIGHT, 'COL-REFLECT')
        self.runMotorTimed(CamCar.MOTOR_EYES, 50, 400)
        self.mood = 'angry'

    def moodSad(self):
        if self.mood == 'sad': return
        self.changeSensorMode(CamCar.EYE_LEFT, 'COL-AMBIENT')
        self.changeSensorMode(CamCar.EYE_RIGHT, 'COL-AMBIENT')
        self.runMotorTimed(CamCar.MOTOR_EYES, -50, 400)
        self.mood = 'sad'

    # Changes the smoothness of the servos
    def setServoSmoothness(self, smoothness):
        self.smoothness = smoothness

    # Continously sets the servo angle by the servo rotaitno variable including
    # the smoothness
    def servoControl(self):
        self.setServoSmoothness(0)
        while 1:
            self.xServo.setAngle(self.xServo.getAngle() * self.smoothness
                    + self.xServoRotation * (1 - self.smoothness))
            self.yServo.setAngle(self.yServo.getAngle() * self.smoothness
                    + self.yServoRotation * (1 - self.smoothness))
            time.sleep(.01)

    # Sets the x servo rotation
    def setXServoRotation(self, rot):
        self.xServoRotation = rot + 90;
        if self.xServoRotation < self.xServo.minAngle: self.xServoRotation = self.xServo.minAngle;
        if self.xServoRotation > self.xServo.maxAngle: self.xServoRotation = self.xServo.maxAngle;

    # Sets the y servo rotation
    def setYServoRotation(self, rot):
        self.yServoRotation = rot + 90;
        if self.yServoRotation < self.yServo.minAngle: self.yServoRotation = self.yServo.minAngle;
        if self.yServoRotation > self.yServo.maxAngle: self.yServoRotation = self.yServo.maxAngle;

    # Returns the absolute rotation of the x servo
    def getXServoRotation(self):
        return self.xServoRotation - 90;

    # Returns the absolute rotation of the y servo
    def getYServoRotation(self):
        return self.yServoRotation - 90;

    # Rotates the servos to position 0 (or 90 degrees)
    def resetServos(self):
        self.xServo.setAngle(90)
        self.yServo.setAngle(90)
        self.setXServoRotation(0)
        self.setYServoRotation(0)
        self.sleep(300)

    def sleep(self, millis):
        time.sleep(float(millis) / 1000.0)

# Small test program
if __name__=='__main__':
    car = CamCar()
