from CamCar import CamCar
import time
import random

# Create a cam car
car = CamCar()

while 1:
    # Loop through the emotions and show each one
    car.moodNormal()
    time.sleep(2)
    car.moodAngry()
    time.sleep(2)
    car.moodSad()
    time.sleep(2)
