#!/usr/bin/python3

# install pigpio and run its daemon in the background
# sudo pip3 install pigpio
# sudo pigpiod

import pigpio
import time
import numpy as np

SERVO_PIN = 18

class Servo():
    
    def __init__(self, pin):
        self.pin = pin
        
        self.pi = pigpio.pi()
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
            
    def calibrate(self):
        
        # set min/mid/max pulse width to calibrate servo control for 0-180 degree sweep
        # typical pulse width range: (700, 1500, 2000)

        MIN_PW = 550   #  0 deg, changing MIN_PW first as it impacts the max servo movement
        MID_PW = 1375  # 90 deg
        MAX_PW = 2150  #180 deg
        
        # just some test positions
        pws = (MID_PW, MAX_PW, MIN_PW)
        degs = (90, 180, 0)
        
        # move servo to test positions
        for i in range(len(pws)):
            self.pi.set_servo_pulsewidth(self.pin, pws[i])
            print("move degree = {:3d} pw = {:4d}".format(degs[i], pws[i]))
            time.sleep(1)

    def move(self, degree):
        pw = np.interp(degree, (0, 180), (MIN_PW, MAX_PW))
        self.pi.set_servo_pulsewidth(self.pin, pw)
        print("move degree = {:3d} pw = {:4d}".format(degree, self.pi.get_servo_pulsewidth(self.pin)))
        time.sleep(1)
        
    def stop(self):
        self.pi.stop()

#===========

servo = Servo(SERVO_PIN)
servo.calibrate()
servo.stop()